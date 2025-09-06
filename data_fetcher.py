import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import time
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianMarketDataFetcher:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
    def get_live_price(self, symbol):
        """Get live price for Indian stocks/indices"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'price': info.get('regularMarketPrice', 0),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'open': info.get('regularMarketOpen', 0),
                'timestamp': datetime.now()
            }
        except Exception as e:
            logger.error(f"Error fetching live price for {symbol}: {e}")
            return None
    
    def get_historical_data(self, symbol, period="1mo", interval="1d"):
        """Get historical data for technical analysis"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            return data
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    def get_intraday_data(self, symbol, interval="5m"):
        """Get intraday data for short-term analysis"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d", interval=interval)
            return data
        except Exception as e:
            logger.error(f"Error fetching intraday data for {symbol}: {e}")
            return None
    
    def calculate_pcr(self, symbol):
        """Calculate Put-Call Ratio for options"""
        try:
            # This is a simplified PCR calculation
            # In real implementation, you'd need options data from NSE
            ticker = yf.Ticker(symbol)
            
            # Get options chain (if available)
            try:
                options = ticker.options
                if options:
                    # Get the nearest expiry
                    expiry = options[0]
                    calls = ticker.option_chain(expiry).calls
                    puts = ticker.option_chain(expiry).puts
                    
                    total_call_oi = calls['openInterest'].sum() if 'openInterest' in calls.columns else 0
                    total_put_oi = puts['openInterest'].sum() if 'openInterest' in puts.columns else 0
                    
                    pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0
                    
                    return {
                        'symbol': symbol,
                        'pcr': pcr,
                        'total_call_oi': total_call_oi,
                        'total_put_oi': total_put_oi,
                        'expiry': expiry,
                        'timestamp': datetime.now()
                    }
            except:
                pass
            
            # Fallback: Use volume-based PCR approximation
            data = self.get_historical_data(symbol, period="5d", interval="1d")
            if data is not None and len(data) > 0:
                # Simple approximation using price movement
                price_change = data['Close'].pct_change()
                up_days = (price_change > 0).sum()
                down_days = (price_change < 0).sum()
                
                pcr_approx = down_days / up_days if up_days > 0 else 1
                
                return {
                    'symbol': symbol,
                    'pcr': pcr_approx,
                    'method': 'approximation',
                    'timestamp': datetime.now()
                }
                
        except Exception as e:
            logger.error(f"Error calculating PCR for {symbol}: {e}")
        
        return None
    
    def get_market_sentiment(self, symbol):
        """Get market sentiment based on multiple indicators"""
        try:
            data = self.get_historical_data(symbol, period="1mo", interval="1d")
            if data is None or len(data) < 20:
                return None
            
            # Calculate technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
            
            current_price = data['Close'].iloc[-1]
            sma_20 = data['SMA_20'].iloc[-1]
            sma_50 = data['SMA_50'].iloc[-1]
            rsi = data['RSI'].iloc[-1]
            volume_ratio = data['Volume'].iloc[-1] / data['Volume_MA'].iloc[-1]
            
            # Sentiment scoring
            sentiment_score = 0
            
            # Price vs moving averages
            if current_price > sma_20:
                sentiment_score += 1
            if current_price > sma_50:
                sentiment_score += 1
            if sma_20 > sma_50:
                sentiment_score += 1
            
            # RSI analysis
            if rsi < 30:
                sentiment_score += 1  # Oversold
            elif rsi > 70:
                sentiment_score -= 1  # Overbought
            
            # Volume analysis
            if volume_ratio > 1.5:
                sentiment_score += 1  # High volume
            
            # Determine sentiment
            if sentiment_score >= 3:
                sentiment = "BULLISH"
            elif sentiment_score <= -1:
                sentiment = "BEARISH"
            else:
                sentiment = "NEUTRAL"
            
            return {
                'symbol': symbol,
                'sentiment': sentiment,
                'score': sentiment_score,
                'current_price': current_price,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'rsi': rsi,
                'volume_ratio': volume_ratio,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error calculating market sentiment for {symbol}: {e}")
            return None
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def get_support_resistance_levels(self, symbol):
        """Identify support and resistance levels"""
        try:
            data = self.get_historical_data(symbol, period="3mo", interval="1d")
            if data is None or len(data) < 50:
                return None
            
            highs = data['High'].values
            lows = data['Low'].values
            
            # Find pivot points
            resistance_levels = []
            support_levels = []
            
            for i in range(2, len(highs) - 2):
                # Resistance (pivot high)
                if highs[i] > highs[i-1] and highs[i] > highs[i-2] and \
                   highs[i] > highs[i+1] and highs[i] > highs[i+2]:
                    resistance_levels.append(highs[i])
                
                # Support (pivot low)
                if lows[i] < lows[i-1] and lows[i] < lows[i-2] and \
                   lows[i] < lows[i+1] and lows[i] < lows[i+2]:
                    support_levels.append(lows[i])
            
            # Cluster nearby levels
            resistance_levels = self.cluster_levels(resistance_levels)
            support_levels = self.cluster_levels(support_levels)
            
            current_price = data['Close'].iloc[-1]
            
            return {
                'symbol': symbol,
                'resistance_levels': sorted(resistance_levels),
                'support_levels': sorted(support_levels),
                'current_price': current_price,
                'nearest_resistance': min([r for r in resistance_levels if r > current_price], default=None),
                'nearest_support': max([s for s in support_levels if s < current_price], default=None),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error calculating support/resistance for {symbol}: {e}")
            return None
    
    def cluster_levels(self, levels, tolerance=0.02):
        """Cluster nearby price levels"""
        if not levels:
            return []
        
        levels = sorted(levels)
        clustered = []
        current_cluster = [levels[0]]
        
        for level in levels[1:]:
            if abs(level - current_cluster[-1]) / current_cluster[-1] <= tolerance:
                current_cluster.append(level)
            else:
                # Average the cluster and add to result
                clustered.append(sum(current_cluster) / len(current_cluster))
                current_cluster = [level]
        
        # Add the last cluster
        if current_cluster:
            clustered.append(sum(current_cluster) / len(current_cluster))
        
        return clustered
    
    def get_market_overview(self):
        """Get overview of major Indian indices"""
        overview = {}
        
        for name, symbol in self.config.MAJOR_INDICES.items():
            try:
                data = self.get_live_price(symbol)
                if data:
                    overview[name] = data
            except Exception as e:
                logger.error(f"Error getting overview for {name}: {e}")
        
        return overview
