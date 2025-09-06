#!/usr/bin/env python3
"""
AI Chat Component for Live Market Analysis
Provides real-time trading recommendations and market insights
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional, Tuple
import ta
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MarketAnalysis:
    symbol: str
    current_price: float
    trend: str
    strength: str
    support_levels: List[float]
    resistance_levels: List[float]
    rsi: float
    macd_signal: str
    volume_trend: str
    volatility: float
    recommendation: str
    confidence: float
    reasoning: str
    risk_level: str

class AIChatComponent:
    def __init__(self):
        self.chat_history = []
        self.analysis_cache = {}
        
    def get_live_market_data(self, symbol: str, period: str = "1d", interval: str = "5m") -> pd.DataFrame:
        """Fetch live market data"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate technical indicators"""
        if data.empty:
            return {}
        
        indicators = {}
        
        # RSI
        indicators['rsi'] = ta.momentum.RSIIndicator(data['Close']).rsi().iloc[-1]
        
        # MACD
        macd = ta.trend.MACD(data['Close'])
        indicators['macd'] = macd.macd().iloc[-1]
        indicators['macd_signal'] = macd.macd_signal().iloc[-1]
        indicators['macd_histogram'] = macd.macd_diff().iloc[-1]
        
        # Moving Averages
        indicators['sma_20'] = ta.trend.SMAIndicator(data['Close'], window=20).sma_indicator().iloc[-1]
        indicators['sma_50'] = ta.trend.SMAIndicator(data['Close'], window=50).sma_indicator().iloc[-1]
        indicators['ema_12'] = ta.trend.EMAIndicator(data['Close'], window=12).ema_indicator().iloc[-1]
        indicators['ema_26'] = ta.trend.EMAIndicator(data['Close'], window=26).ema_indicator().iloc[-1]
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(data['Close'])
        indicators['bb_upper'] = bb.bollinger_hband().iloc[-1]
        indicators['bb_middle'] = bb.bollinger_mavg().iloc[-1]
        indicators['bb_lower'] = bb.bollinger_lband().iloc[-1]
        
        # Volume indicators
        indicators['volume_sma'] = data['Volume'].rolling(window=20).mean().iloc[-1]
        indicators['current_volume'] = data['Volume'].iloc[-1]
        
        # Volatility
        indicators['atr'] = ta.volatility.AverageTrueRange(data['High'], data['Low'], data['Close']).average_true_range().iloc[-1]
        
        return indicators
    
    def identify_support_resistance(self, data: pd.DataFrame) -> Tuple[List[float], List[float]]:
        """Identify support and resistance levels"""
        if data.empty:
            return [], []
        
        highs = data['High'].rolling(window=20).max()
        lows = data['Low'].rolling(window=20).min()
        
        # Find recent highs and lows
        recent_highs = data[data['High'] == highs]['High'].unique()
        recent_lows = data[data['Low'] == lows]['Low'].unique()
        
        current_price = data['Close'].iloc[-1]
        
        # Filter levels near current price
        resistance_levels = [h for h in recent_highs if h > current_price][:3]
        support_levels = [l for l in recent_lows if l < current_price][:3]
        
        return support_levels, resistance_levels
    
    def analyze_market_sentiment(self, data: pd.DataFrame, indicators: Dict) -> Dict:
        """Analyze market sentiment and trend"""
        if data.empty:
            return {}
        
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
        
        # Trend analysis
        price_change = ((current_price - prev_price) / prev_price) * 100
        sma_20 = indicators.get('sma_20', current_price)
        sma_50 = indicators.get('sma_50', current_price)
        
        # Determine trend
        if current_price > sma_20 > sma_50:
            trend = "STRONG_UPTREND"
            trend_strength = "Strong"
        elif current_price > sma_20:
            trend = "UPTREND"
            trend_strength = "Moderate"
        elif current_price < sma_20 < sma_50:
            trend = "STRONG_DOWNTREND"
            trend_strength = "Strong"
        elif current_price < sma_20:
            trend = "DOWNTREND"
            trend_strength = "Moderate"
        else:
            trend = "SIDEWAYS"
            trend_strength = "Weak"
        
        # RSI analysis
        rsi = indicators.get('rsi', 50)
        if rsi > 70:
            rsi_signal = "OVERBOUGHT"
        elif rsi < 30:
            rsi_signal = "OVERSOLD"
        else:
            rsi_signal = "NEUTRAL"
        
        # MACD analysis
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        if macd > macd_signal:
            macd_trend = "BULLISH"
        else:
            macd_trend = "BEARISH"
        
        # Volume analysis
        current_volume = indicators.get('current_volume', 0)
        avg_volume = indicators.get('volume_sma', current_volume)
        if current_volume > avg_volume * 1.5:
            volume_trend = "HIGH_VOLUME"
        elif current_volume < avg_volume * 0.5:
            volume_trend = "LOW_VOLUME"
        else:
            volume_trend = "NORMAL_VOLUME"
        
        return {
            'trend': trend,
            'trend_strength': trend_strength,
            'price_change': price_change,
            'rsi_signal': rsi_signal,
            'macd_trend': macd_trend,
            'volume_trend': volume_trend
        }
    
    def generate_trading_recommendation(self, symbol: str, data: pd.DataFrame, indicators: Dict, sentiment: Dict) -> MarketAnalysis:
        """Generate comprehensive trading recommendation"""
        if data.empty:
            return None
        
        current_price = data['Close'].iloc[-1]
        support_levels, resistance_levels = self.identify_support_resistance(data)
        
        # Analyze for options trading
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        atr = indicators.get('atr', 0)
        
        # Determine recommendation
        recommendation = ""
        confidence = 0.0
        reasoning = []
        risk_level = "MEDIUM"
        
        # Trend-based analysis
        if sentiment['trend'] == "STRONG_UPTREND":
            if rsi < 70:  # Not overbought
                recommendation = "BUY_CALL"
                confidence = 0.8
                reasoning.append("Strong uptrend with momentum")
                risk_level = "LOW"
            else:
                recommendation = "WAIT"
                confidence = 0.6
                reasoning.append("Strong uptrend but RSI overbought")
        
        elif sentiment['trend'] == "STRONG_DOWNTREND":
            if rsi > 30:  # Not oversold
                recommendation = "BUY_PUT"
                confidence = 0.8
                reasoning.append("Strong downtrend with momentum")
                risk_level = "LOW"
            else:
                recommendation = "WAIT"
                confidence = 0.6
                reasoning.append("Strong downtrend but RSI oversold")
        
        elif sentiment['trend'] == "UPTREND":
            if macd > macd_signal and rsi < 65:
                recommendation = "BUY_CALL"
                confidence = 0.7
                reasoning.append("Moderate uptrend with MACD confirmation")
                risk_level = "MEDIUM"
            else:
                recommendation = "WAIT"
                confidence = 0.5
                reasoning.append("Moderate uptrend but mixed signals")
        
        elif sentiment['trend'] == "DOWNTREND":
            if macd < macd_signal and rsi > 35:
                recommendation = "BUY_PUT"
                confidence = 0.7
                reasoning.append("Moderate downtrend with MACD confirmation")
                risk_level = "MEDIUM"
            else:
                recommendation = "WAIT"
                confidence = 0.5
                reasoning.append("Moderate downtrend but mixed signals")
        
        else:  # SIDEWAYS
            recommendation = "WAIT"
            confidence = 0.4
            reasoning.append("Sideways market - wait for breakout")
            risk_level = "HIGH"
        
        # Volume confirmation
        if sentiment['volume_trend'] == "HIGH_VOLUME":
            confidence += 0.1
            reasoning.append("High volume confirms trend")
        
        # Volatility consideration
        if atr > current_price * 0.02:  # High volatility
            risk_level = "HIGH"
            reasoning.append("High volatility - use proper position sizing")
        
        # Cap confidence at 0.95
        confidence = min(confidence, 0.95)
        
        return MarketAnalysis(
            symbol=symbol,
            current_price=current_price,
            trend=sentiment['trend'],
            strength=sentiment['trend_strength'],
            support_levels=support_levels,
            resistance_levels=resistance_levels,
            rsi=rsi,
            macd_signal=sentiment['macd_trend'],
            volume_trend=sentiment['volume_trend'],
            volatility=atr,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=" | ".join(reasoning),
            risk_level=risk_level
        )
    
    def create_live_chart(self, data: pd.DataFrame, analysis: MarketAnalysis) -> go.Figure:
        """Create live trading chart with indicators - Groww Terminal Style"""
        if data.empty:
            return go.Figure()
        
        # Create subplots with volume
        fig = go.Figure()
        
        # Main candlestick chart with professional styling
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price',
            increasing_line_color='#00D4AA',  # Green like Groww
            decreasing_line_color='#FF6B6B',  # Red like Groww
            increasing_fillcolor='#00D4AA',
            decreasing_fillcolor='#FF6B6B',
            line=dict(width=1)
        ))
        
        # Add moving averages with professional styling
        if len(data) >= 20:
            sma_20 = ta.trend.SMAIndicator(data['Close'], window=20).sma_indicator()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma_20,
                mode='lines',
                name='SMA 20',
                line=dict(color='#4ECDC4', width=2, dash='solid'),
                opacity=0.8
            ))
        
        if len(data) >= 50:
            sma_50 = ta.trend.SMAIndicator(data['Close'], window=50).sma_indicator()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma_50,
                mode='lines',
                name='SMA 50',
                line=dict(color='#FFA726', width=2, dash='solid'),
                opacity=0.8
            ))
        
        # Add Bollinger Bands with subtle styling
        if len(data) >= 20:
            bb = ta.volatility.BollingerBands(data['Close'])
            bb_upper = bb.bollinger_hband()
            bb_lower = bb.bollinger_lband()
            bb_middle = bb.bollinger_mavg()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=bb_upper,
                mode='lines',
                name='BB Upper',
                line=dict(color='rgba(255,255,255,0.2)', width=1),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=bb_lower,
                mode='lines',
                name='BB Lower',
                line=dict(color='rgba(255,255,255,0.2)', width=1),
                fill='tonexty',
                fillcolor='rgba(255,255,255,0.05)',
                showlegend=False
            ))
        
        # Add support and resistance levels with professional styling
        for i, level in enumerate(analysis.support_levels):
            fig.add_hline(
                y=level,
                line_dash="dash",
                line_color="#00D4AA",
                line_width=1.5,
                opacity=0.7,
                annotation_text=f"Support {i+1}: ₹{level:.2f}",
                annotation_position="bottom right",
                annotation=dict(
                    font=dict(size=10, color="#00D4AA"),
                    bgcolor="rgba(0,0,0,0.8)",
                    bordercolor="#00D4AA",
                    borderwidth=1
                )
            )
        
        for i, level in enumerate(analysis.resistance_levels):
            fig.add_hline(
                y=level,
                line_dash="dash",
                line_color="#FF6B6B",
                line_width=1.5,
                opacity=0.7,
                annotation_text=f"Resistance {i+1}: ₹{level:.2f}",
                annotation_position="top right",
                annotation=dict(
                    font=dict(size=10, color="#FF6B6B"),
                    bgcolor="rgba(0,0,0,0.8)",
                    bordercolor="#FF6B6B",
                    borderwidth=1
                )
            )
        
        # Add current price line
        current_price = data['Close'].iloc[-1]
        fig.add_hline(
            y=current_price,
            line_dash="dot",
            line_color="#FF6B6B",
            line_width=2,
            opacity=0.8,
            annotation_text=f"Current: ₹{current_price:.2f}",
            annotation_position="right",
            annotation=dict(
                font=dict(size=12, color="#FF6B6B"),
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#FF6B6B",
                borderwidth=1
            )
        )
        
        # Professional layout like Groww Terminal
        fig.update_layout(
            title=dict(
                text=f"{analysis.symbol} • Live Chart",
                font=dict(size=18, color="#FFFFFF"),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="",
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1
            ),
            yaxis=dict(
                title="",
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1,
                side='right'
            ),
            template="plotly_dark",
            height=500,
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='rgba(0,0,0,0.9)',
                bordercolor='rgba(255,255,255,0.2)',
                font=dict(size=11)
            )
        )
        
        return fig
    
    def create_volume_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create volume chart - Groww Terminal Style"""
        if data.empty:
            return go.Figure()
        
        # Create volume bars with professional styling
        colors = ['#00D4AA' if close >= open else '#FF6B6B' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7,
            marker_line_width=0
        ))
        
        # Add volume SMA line
        if len(data) >= 20:
            volume_sma = data['Volume'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=volume_sma,
                mode='lines',
                name='Volume SMA 20',
                line=dict(color='#FFA726', width=2),
                opacity=0.8
            ))
        
        # Professional layout like Groww Terminal
        fig.update_layout(
            title=dict(
                text="Volume Analysis",
                font=dict(size=16, color="#FFFFFF"),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="",
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1
            ),
            yaxis=dict(
                title="",
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1,
                side='right'
            ),
            template="plotly_dark",
            height=200,
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=60, b=50),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='rgba(0,0,0,0.9)',
                bordercolor='rgba(255,255,255,0.2)',
                font=dict(size=11)
            )
        )
        
        return fig
    
    def create_technical_indicators_chart(self, data: pd.DataFrame) -> go.Figure:
        """Create technical indicators subplot - Groww Terminal Style"""
        if data.empty:
            return go.Figure()
        
        # Create subplots for RSI and MACD
        fig = go.Figure()
        
        # RSI with professional styling
        if len(data) >= 14:
            rsi = ta.momentum.RSIIndicator(data['Close']).rsi()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=rsi,
                mode='lines',
                name='RSI',
                line=dict(color='#9C27B0', width=2),
                opacity=0.9
            ))
            
            # Add RSI overbought/oversold lines with professional styling
            fig.add_hline(
                y=70, 
                line_dash="dash", 
                line_color="#FF6B6B", 
                line_width=1,
                opacity=0.7,
                annotation_text="Overbought (70)",
                annotation=dict(
                    font=dict(size=10, color="#FF6B6B"),
                    bgcolor="rgba(0,0,0,0.8)",
                    bordercolor="#FF6B6B",
                    borderwidth=1
                )
            )
            fig.add_hline(
                y=30, 
                line_dash="dash", 
                line_color="#00D4AA", 
                line_width=1,
                opacity=0.7,
                annotation_text="Oversold (30)",
                annotation=dict(
                    font=dict(size=10, color="#00D4AA"),
                    bgcolor="rgba(0,0,0,0.8)",
                    bordercolor="#00D4AA",
                    borderwidth=1
                )
            )
            fig.add_hline(
                y=50, 
                line_dash="dot", 
                line_color="#FFFFFF", 
                line_width=1,
                opacity=0.5,
                annotation_text="Neutral (50)",
                annotation=dict(
                    font=dict(size=10, color="#FFFFFF"),
                    bgcolor="rgba(0,0,0,0.8)",
                    bordercolor="#FFFFFF",
                    borderwidth=1
                )
            )
        
        # MACD with professional styling
        if len(data) >= 26:
            macd = ta.trend.MACD(data['Close'])
            macd_line = macd.macd()
            macd_signal = macd.macd_signal()
            macd_histogram = macd.macd_diff()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=macd_line,
                mode='lines',
                name='MACD',
                line=dict(color='#2196F3', width=2),
                opacity=0.9
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=macd_signal,
                mode='lines',
                name='MACD Signal',
                line=dict(color='#FF9800', width=2),
                opacity=0.9
            ))
            
            # MACD histogram with professional colors
            colors = ['#00D4AA' if val >= 0 else '#FF6B6B' for val in macd_histogram]
            fig.add_trace(go.Bar(
                x=data.index,
                y=macd_histogram,
                name='MACD Histogram',
                marker_color=colors,
                opacity=0.7,
                marker_line_width=0
            ))
        
        # Professional layout like Groww Terminal
        fig.update_layout(
            title=dict(
                text="Technical Indicators",
                font=dict(size=16, color="#FFFFFF"),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="",
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1
            ),
            yaxis=dict(
                title="",
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.3)',
                linewidth=1,
                side='right'
            ),
            template="plotly_dark",
            height=300,
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=60, b=50),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='rgba(0,0,0,0.9)',
                bordercolor='rgba(255,255,255,0.2)',
                font=dict(size=11)
            )
        )
        
        return fig
    
    def create_ai_response(self, user_message: str, symbol: str = None) -> str:
        """Generate AI response based on user message and market data"""
        if not symbol:
            return "Please provide a symbol to analyze the market."
        
        # Get live market data
        data = self.get_live_market_data(symbol)
        if data.empty:
            return f"Unable to fetch data for {symbol}. Please check the symbol and try again."
        
        # Calculate indicators
        indicators = self.calculate_technical_indicators(data)
        if not indicators:
            return f"Unable to calculate indicators for {symbol}."
        
        # Analyze sentiment
        sentiment = self.analyze_market_sentiment(data, indicators)
        if not sentiment:
            return f"Unable to analyze sentiment for {symbol}."
        
        # Generate recommendation
        analysis = self.generate_trading_recommendation(symbol, data, indicators, sentiment)
        if not analysis:
            return f"Unable to generate recommendation for {symbol}."
        
        # Enhanced response with options-specific analysis
        response = f"""
🤖 **AI Market Analysis for {symbol}**

📊 **Current Status:**
- Price: ₹{analysis.current_price:.2f}
- Trend: {analysis.trend} ({analysis.strength})
- RSI: {analysis.rsi:.1f} ({'Overbought' if analysis.rsi > 70 else 'Oversold' if analysis.rsi < 30 else 'Neutral'})
- MACD: {analysis.macd_signal}
- Volume: {analysis.volume_trend}
- Volatility (ATR): ₹{analysis.volatility:.2f}

🎯 **Options Trading Recommendation:**
- Action: {analysis.recommendation.replace('_', ' ')}
- Confidence: {analysis.confidence:.1%}
- Risk Level: {analysis.risk_level}
- Reasoning: {analysis.reasoning}

📈 **Key Levels for Options:**
- Support: {', '.join([f'₹{s:.2f}' for s in analysis.support_levels]) if analysis.support_levels else 'None identified'}
- Resistance: {', '.join([f'₹{r:.2f}' for r in analysis.resistance_levels]) if analysis.resistance_levels else 'None identified'}

💡 **Options Strategy Suggestions:**
{self._get_options_strategy_suggestions(analysis)}

⚠️ **Risk Management for Options:**
- Use proper position sizing (1-2% risk per trade)
- Set stop loss based on support/resistance levels
- Monitor implied volatility before entry
- Consider time decay for short-term options
- Use spreads to reduce risk

🔄 **Next Steps:**
{self._get_next_steps(analysis)}
        """
        
        return response.strip()
    
    def _get_options_strategy_suggestions(self, analysis: MarketAnalysis) -> str:
        """Get options strategy suggestions based on analysis"""
        suggestions = []
        
        if analysis.recommendation == "BUY_CALL":
            if analysis.confidence > 0.7:
                suggestions.append("• Consider ATM or slightly ITM call options")
                suggestions.append("• Look for options with 7-14 days expiry")
                suggestions.append("• Monitor for breakout above resistance levels")
            else:
                suggestions.append("• Consider OTM call options for lower cost")
                suggestions.append("• Use call spreads to reduce risk")
                suggestions.append("• Wait for stronger confirmation signals")
        
        elif analysis.recommendation == "BUY_PUT":
            if analysis.confidence > 0.7:
                suggestions.append("• Consider ATM or slightly ITM put options")
                suggestions.append("• Look for options with 7-14 days expiry")
                suggestions.append("• Monitor for breakdown below support levels")
            else:
                suggestions.append("• Consider OTM put options for lower cost")
                suggestions.append("• Use put spreads to reduce risk")
                suggestions.append("• Wait for stronger confirmation signals")
        
        else:  # WAIT
            suggestions.append("• Wait for clearer trend direction")
            suggestions.append("• Consider iron condor for sideways market")
            suggestions.append("• Monitor for breakout/breakdown signals")
        
        return "\n".join(suggestions)
    
    def _get_next_steps(self, analysis: MarketAnalysis) -> str:
        """Get next steps based on analysis"""
        steps = []
        
        if analysis.recommendation in ["BUY_CALL", "BUY_PUT"]:
            steps.append("1. Check current options chain for best strikes")
            steps.append("2. Verify implied volatility levels")
            steps.append("3. Set entry price and stop loss")
            steps.append("4. Monitor for confirmation signals")
            steps.append("5. Plan exit strategy based on targets")
        else:
            steps.append("1. Monitor support/resistance levels")
            steps.append("2. Wait for breakout/breakdown signals")
            steps.append("3. Prepare for next trading opportunity")
            steps.append("4. Keep track of key levels")
        
        return "\n".join(steps)
    
    def _extract_symbol_from_message(self, message: str) -> str:
        """Extract symbol from user message with enhanced detection"""
        message_lower = message.lower()
        
        # Comprehensive symbols mapping
        symbol_mapping = {
            # Major Indices
            "nifty": "^NSEI",
            "nifty50": "^NSEI",
            "nifty 50": "^NSEI",
            "banknifty": "^NSEBANK",
            "bank nifty": "^NSEBANK",
            "sensex": "^BSESN",
            "finnifty": "NIFTY_FIN_SERVICE.NS",
            
            # Banking & Financial Services
            "hdfc bank": "HDFCBANK.NS",
            "hdfc": "HDFC.NS",
            "icici bank": "ICICIBANK.NS",
            "icici": "ICICIBANK.NS",
            "axis bank": "AXISBANK.NS",
            "axis": "AXISBANK.NS",
            "kotak bank": "KOTAKBANK.NS",
            "kotak": "KOTAKBANK.NS",
            "sbi": "SBIN.NS",
            "state bank": "SBIN.NS",
            "indusind bank": "INDUSINDBK.NS",
            "indusind": "INDUSINDBK.NS",
            "bandhan bank": "BANDHANBNK.NS",
            "federal bank": "FEDERALBNK.NS",
            "idfc first bank": "IDFCFIRSTB.NS",
            "au small finance": "AUBANK.NS",
            "bajaj finance": "BAJFINANCE.NS",
            "bajaj finserv": "BAJFINANCE.NS",
            "hdfc life": "HDFCLIFE.NS",
            "sbi life": "SBILIFE.NS",
            "lici": "LICI.NS",
            "life insurance": "LICI.NS",
            
            # IT & Technology
            "tcs": "TCS.NS",
            "infosys": "INFY.NS",
            "infy": "INFY.NS",
            "wipro": "WIPRO.NS",
            "hcl tech": "HCLTECH.NS",
            "hcl": "HCLTECH.NS",
            "tech mahindra": "TECHM.NS",
            "techm": "TECHM.NS",
            "l&t infotech": "LTI.NS",
            "lti": "LTI.NS",
            "mindtree": "MINDTREE.NS",
            "mphasis": "MPHASIS.NS",
            "persistent": "PERSISTENT.NS",
            "coforge": "COFORGE.NS",
            
            # Oil & Gas
            "reliance": "RELIANCE.NS",
            "ongc": "ONGC.NS",
            "ioc": "IOC.NS",
            "bpcl": "BPCL.NS",
            "hpcl": "HPCL.NS",
            "gail": "GAIL.NS",
            "petronet lng": "PETRONET.NS",
            "petronet": "PETRONET.NS",
            "adani ports": "ADANIPORTS.NS",
            "adani green": "ADANIGREEN.NS",
            "adani transmission": "ADANITRANS.NS",
            "adani power": "ADANIPOWER.NS",
            
            # FMCG & Consumer
            "hindunilvr": "HINDUNILVR.NS",
            "hul": "HINDUNILVR.NS",
            "itc": "ITC.NS",
            "nestle": "NESTLEIND.NS",
            "dabur": "DABUR.NS",
            "godrej cp": "GODREJCP.NS",
            "marico": "MARICO.NS",
            "britannia": "BRITANNIA.NS",
            "titan": "TITAN.NS",
            "tata consumer": "TATACONSUM.NS",
            "ubl": "UBL.NS",
            
            # Auto & Auto Ancillaries
            "maruti": "MARUTI.NS",
            "maruti suzuki": "MARUTI.NS",
            "tata motors": "TATAMOTORS.NS",
            "tata": "TATAMOTORS.NS",
            "mahindra": "M&M.NS",
            "m&m": "M&M.NS",
            "bajaj auto": "BAJAJ-AUTO.NS",
            "bajaj": "BAJAJ-AUTO.NS",
            "hero motocorp": "HEROMOTOCO.NS",
            "hero": "HEROMOTOCO.NS",
            "eicher motors": "EICHERMOT.NS",
            "eicher": "EICHERMOT.NS",
            "ashok leyland": "ASHOKLEY.NS",
            "bosch": "BOSCHLTD.NS",
            "exide": "EXIDEIND.NS",
            "apollo tyres": "APOLLOTYRE.NS",
            
            # Pharmaceuticals
            "sun pharma": "SUNPHARMA.NS",
            "sun": "SUNPHARMA.NS",
            "dr. reddys": "DRREDDY.NS",
            "dr reddys": "DRREDDY.NS",
            "cipla": "CIPLA.NS",
            "divis lab": "DIVISLAB.NS",
            "divis": "DIVISLAB.NS",
            "biocon": "BIOCON.NS",
            "lupin": "LUPIN.NS",
            "aurobindo pharma": "AUROPHARMA.NS",
            "aurobindo": "AUROPHARMA.NS",
            "cadila health": "ZYDUSLIFE.NS",
            "zydus": "ZYDUSLIFE.NS",
            "torrent pharma": "TORNTPHARM.NS",
            "torrent": "TORNTPHARM.NS",
            "glenmark": "GLENMARK.NS",
            
            # Telecom
            "bharti airtel": "BHARTIARTL.NS",
            "airtel": "BHARTIARTL.NS",
            "bharti": "BHARTIARTL.NS",
            "jio": "RJIO.NS",
            "vodafone idea": "IDEA.NS",
            "idea": "IDEA.NS",
            
            # Power & Utilities
            "ntpc": "NTPC.NS",
            "powergrid": "POWERGRID.NS",
            "tata power": "TATAPOWER.NS",
            "torrent power": "TORNTPOWER.NS",
            "cesc": "CESC.NS",
            
            # Metals & Mining
            "tata steel": "TATASTEEL.NS",
            "jsw steel": "JSWSTEEL.NS",
            "sail": "SAIL.NS",
            "hindalco": "HINDALCO.NS",
            "vedanta": "VEDL.NS",
            "coal india": "COALINDIA.NS",
            "coil": "COALINDIA.NS",
            "nmdc": "NMDC.NS",
            "jindal steel": "JINDALSTEL.NS",
            "jindal": "JINDALSTEL.NS",
            
            # Cement
            "ultratech cement": "ULTRACEMCO.NS",
            "ultratech": "ULTRACEMCO.NS",
            "shree cement": "SHREECEM.NS",
            "shree": "SHREECEM.NS",
            "grasim": "GRASIM.NS",
            "ambuja cement": "AMBUJACEM.NS",
            "ambuja": "AMBUJACEM.NS",
            "acc": "ACC.NS",
            "ramco cement": "RAMCOCEM.NS",
            "ramco": "RAMCOCEM.NS",
            
            # Real Estate
            "dlf": "DLF.NS",
            "godrej properties": "GODREJPROP.NS",
            "brigade": "BRIGADE.NS",
            "sobha": "SOBHA.NS",
            "mahindra lifespace": "MAHLIFE.NS",
            
            # Media & Entertainment
            "zee entertainment": "ZEEL.NS",
            "zee": "ZEEL.NS",
            "sun tv": "SUNTV.NS",
            "network18": "NETWORK18.NS",
            "pvr": "PVR.NS",
            "inox leisure": "INOXLEISUR.NS",
            "inox": "INOXLEISUR.NS",
            
            # Aviation
            "indigo": "INDIGO.NS",
            "spicejet": "SPICEJET.NS",
            
            # E-commerce & Retail
            "flipkart": "FLIPKART.NS",
            "nykaa": "NYKAA.NS",
            "zomato": "ZOMATO.NS",
            "paytm": "PAYTM.NS",
            "policybazaar": "PBAL.NS",
            
            # Infrastructure
            "l&t": "LT.NS",
            "lt": "LT.NS",
            "container corp": "CONCOR.NS",
            "concor": "CONCOR.NS",
            "irctc": "IRCTC.NS",
            "rvnl": "RVNL.NS",
            
            # Small & Mid Cap Gems
            "polycab": "POLYCAB.NS",
            "astral": "ASTRAL.NS",
            "crompton": "CROMPTON.NS",
            "havells": "HAVELLS.NS",
            "voltas": "VOLTAS.NS",
            "blue dart": "BLUEDART.NS",
            "delta corp": "DELTACORP.NS",
            "jubilant food": "JUBLFOOD.NS",
            "jubilant": "JUBLFOOD.NS",
            "page industries": "PAGEIND.NS",
            "page": "PAGEIND.NS",
            "relaxo": "RELAXO.NS"
        }
        
        # Check for exact matches first
        for key, value in symbol_mapping.items():
            if key in message_lower:
                return value
        
        # Check for partial matches
        for key, value in symbol_mapping.items():
            if any(word in message_lower for word in key.split()):
                return value
        
        # Check for options-related keywords
        if any(word in message_lower for word in ["call", "put", "option", "options"]):
            # Default to NIFTY50 for options queries without specific symbol
            return "^NSEI"
        
        return None
    
    def render_chat_interface(self):
        """Render the AI chat interface"""
        st.header("🤖 AI Trading Assistant")
        st.markdown("Ask me anything about market analysis, trading strategies, or get live recommendations!")
        
        # Initialize chat history
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        
        # Chat input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask me about trading:",
                placeholder="e.g., Analyze NIFTY50, Should I buy calls for RELIANCE?, What's the trend for BANKNIFTY?",
                key="chat_input"
            )
        
        with col2:
            if st.button("Send", key="send_chat"):
                if user_input:
                    # Add user message
                    st.session_state.chat_messages.append({"role": "user", "content": user_input})
                    
                    # Extract symbol from message (enhanced extraction)
                    symbol = self._extract_symbol_from_message(user_input)
                    
                    # Generate AI response
                    ai_response = self.create_ai_response(user_input, symbol)
                    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                    
                    # Clear input by rerunning
                    st.rerun()
        
        # Display chat history
        st.subheader("💬 Chat History")
        
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI Assistant:** {message['content']}")
        
        # Quick action buttons
        st.subheader("⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Analyze NIFTY50"):
                response = self.create_ai_response("Analyze NIFTY50", "^NSEI")
                st.session_state.chat_messages.append({"role": "user", "content": "Analyze NIFTY50"})
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col2:
            if st.button("Analyze BANKNIFTY"):
                response = self.create_ai_response("Analyze BANKNIFTY", "^NSEBANK")
                st.session_state.chat_messages.append({"role": "user", "content": "Analyze BANKNIFTY"})
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col3:
            if st.button("Clear Chat"):
                st.session_state.chat_messages = []
                st.rerun()
    
    def render_live_chart(self, symbol: str):
        """Render live trading chart - Groww Terminal Style"""
        st.header(f"📈 Live Chart - {symbol}")
        
        # Get live data
        data = self.get_live_market_data(symbol, period="5d", interval="15m")
        
        if data.empty:
            st.error(f"Unable to fetch data for {symbol}")
            return
        
        # Calculate indicators and analysis
        indicators = self.calculate_technical_indicators(data)
        sentiment = self.analyze_market_sentiment(data, indicators)
        analysis = self.generate_trading_recommendation(symbol, data, indicators, sentiment)
        
        if analysis:
            # Create main chart
            chart = self.create_live_chart(data, analysis)
            st.plotly_chart(chart, width='stretch')
            
            # Create volume chart
            volume_chart = self.create_volume_chart(data)
            st.plotly_chart(volume_chart, width='stretch')
            
            # Create technical indicators chart
            indicators_chart = self.create_technical_indicators_chart(data)
            st.plotly_chart(indicators_chart, width='stretch')
            
            # Display analysis summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Price", f"₹{analysis.current_price:.2f}")
                st.metric("Trend", analysis.trend)
                st.metric("RSI", f"{analysis.rsi:.1f}")
            
            with col2:
                st.metric("Recommendation", analysis.recommendation.replace('_', ' '))
                st.metric("Confidence", f"{analysis.confidence:.1%}")
                st.metric("Risk Level", analysis.risk_level)
            
            with col3:
                st.metric("Volume Trend", analysis.volume_trend)
                st.metric("MACD Signal", analysis.macd_signal)
                st.metric("Volatility (ATR)", f"{analysis.volatility:.2f}")
            
            # Detailed analysis
            st.subheader("📊 Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Support Levels:**")
                for i, level in enumerate(analysis.support_levels):
                    st.write(f"  {i+1}. ₹{level:.2f}")
                
                st.write("**Resistance Levels:**")
                for i, level in enumerate(analysis.resistance_levels):
                    st.write(f"  {i+1}. ₹{level:.2f}")
            
            with col2:
                st.write("**Trading Signals:**")
                st.write(f"  • Trend: {analysis.trend}")
                st.write(f"  • Strength: {analysis.strength}")
                st.write(f"  • Recommendation: {analysis.recommendation}")
                st.write(f"  • Reasoning: {analysis.reasoning}")
        
        # Auto-refresh
        if st.button("🔄 Refresh Data"):
            st.rerun()
        
        # Auto-refresh every 30 seconds
        st.markdown("""
        <script>
        setTimeout(function(){
            window.location.reload();
        }, 30000);
        </script>
        """, unsafe_allow_html=True)
