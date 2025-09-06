import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from data_fetcher import IndianMarketDataFetcher
from config import Config

logger = logging.getLogger(__name__)

class OIAnalyzer:
    def __init__(self):
        self.config = Config()
        self.data_fetcher = IndianMarketDataFetcher()
        
    def analyze_oi_data(self, symbol):
        """Comprehensive OI analysis for options trading"""
        try:
            # Get PCR data
            pcr_data = self.data_fetcher.calculate_pcr(symbol)
            
            # Get market sentiment
            sentiment_data = self.data_fetcher.get_market_sentiment(symbol)
            
            # Get support/resistance levels
            levels_data = self.data_fetcher.get_support_resistance_levels(symbol)
            
            # Get live price
            live_data = self.data_fetcher.get_live_price(symbol)
            
            if not all([pcr_data, sentiment_data, levels_data, live_data]):
                return None
            
            # Analyze OI patterns
            oi_analysis = self._analyze_oi_patterns(pcr_data, sentiment_data, levels_data, live_data)
            
            # Generate trading signals
            signals = self._generate_trading_signals(oi_analysis)
            
            return {
                'symbol': symbol,
                'oi_analysis': oi_analysis,
                'trading_signals': signals,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error in OI analysis for {symbol}: {e}")
            return None
    
    def _analyze_oi_patterns(self, pcr_data, sentiment_data, levels_data, live_data):
        """Analyze OI patterns and market structure"""
        current_price = live_data['price']
        pcr = pcr_data.get('pcr', 1.0)
        sentiment = sentiment_data.get('sentiment', 'NEUTRAL')
        rsi = sentiment_data.get('rsi', 50)
        
        # OI Analysis Rules
        analysis = {
            'pcr_interpretation': self._interpret_pcr(pcr),
            'oi_buildup': self._detect_oi_buildup(pcr, sentiment),
            'max_pain_analysis': self._calculate_max_pain(current_price, levels_data),
            'gamma_exposure': self._estimate_gamma_exposure(pcr, current_price),
            'volatility_skew': self._analyze_volatility_skew(pcr, sentiment),
            'unwinding_signals': self._detect_unwinding_signals(pcr, sentiment),
            'rollover_analysis': self._analyze_rollover_patterns(pcr, sentiment)
        }
        
        return analysis
    
    def _interpret_pcr(self, pcr):
        """Interpret Put-Call Ratio"""
        if pcr > 1.5:
            return {
                'signal': 'EXTREME_FEAR',
                'interpretation': 'High put buying indicates fear. Market may be oversold.',
                'confidence': 'HIGH',
                'action': 'Consider buying calls or covering shorts'
            }
        elif pcr > 1.2:
            return {
                'signal': 'FEAR',
                'interpretation': 'Moderate put buying. Bearish sentiment.',
                'confidence': 'MEDIUM',
                'action': 'Wait for confirmation or buy calls on dips'
            }
        elif pcr > 0.8:
            return {
                'signal': 'NEUTRAL',
                'interpretation': 'Balanced options activity.',
                'confidence': 'LOW',
                'action': 'Follow technical analysis'
            }
        elif pcr > 0.5:
            return {
                'signal': 'GREED',
                'interpretation': 'Moderate call buying. Bullish sentiment.',
                'confidence': 'MEDIUM',
                'action': 'Consider buying puts or selling calls'
            }
        else:
            return {
                'signal': 'EXTREME_GREED',
                'interpretation': 'High call buying indicates greed. Market may be overbought.',
                'confidence': 'HIGH',
                'action': 'Consider buying puts or selling calls'
            }
    
    def _detect_oi_buildup(self, pcr, sentiment):
        """Detect OI buildup patterns"""
        if pcr > 1.2 and sentiment == 'BEARISH':
            return {
                'pattern': 'PUT_BUILDUP',
                'interpretation': 'Heavy put writing/buying. Potential reversal signal.',
                'risk_level': 'HIGH',
                'timeframe': 'SHORT_TERM'
            }
        elif pcr < 0.8 and sentiment == 'BULLISH':
            return {
                'pattern': 'CALL_BUILDUP',
                'interpretation': 'Heavy call writing/buying. Potential reversal signal.',
                'risk_level': 'HIGH',
                'timeframe': 'SHORT_TERM'
            }
        else:
            return {
                'pattern': 'BALANCED',
                'interpretation': 'Normal OI distribution.',
                'risk_level': 'LOW',
                'timeframe': 'MEDIUM_TERM'
            }
    
    def _calculate_max_pain(self, current_price, levels_data):
        """Calculate max pain point (simplified)"""
        if not levels_data:
            return None
        
        support_levels = levels_data.get('support_levels', [])
        resistance_levels = levels_data.get('resistance_levels', [])
        
        # Find the level with maximum options activity (simplified)
        all_levels = support_levels + resistance_levels
        if not all_levels:
            return None
        
        # Assume max pain is near current price
        max_pain = min(all_levels, key=lambda x: abs(x - current_price))
        
        return {
            'max_pain_level': max_pain,
            'distance_from_current': abs(current_price - max_pain),
            'probability': 'MEDIUM' if abs(current_price - max_pain) / current_price < 0.02 else 'LOW'
        }
    
    def _estimate_gamma_exposure(self, pcr, current_price):
        """Estimate gamma exposure (simplified)"""
        # Higher PCR = more puts = higher gamma exposure
        gamma_exposure = 'HIGH' if pcr > 1.2 else 'MEDIUM' if pcr > 0.8 else 'LOW'
        
        return {
            'exposure_level': gamma_exposure,
            'risk_implication': 'High volatility expected' if gamma_exposure == 'HIGH' else 'Normal volatility',
            'hedging_needed': gamma_exposure == 'HIGH'
        }
    
    def _analyze_volatility_skew(self, pcr, sentiment):
        """Analyze volatility skew patterns"""
        if pcr > 1.2:
            skew = 'PUT_SKEW'
            interpretation = 'Higher put premiums indicate fear'
        elif pcr < 0.8:
            skew = 'CALL_SKEW'
            interpretation = 'Higher call premiums indicate greed'
        else:
            skew = 'NORMAL'
            interpretation = 'Balanced volatility skew'
        
        return {
            'skew_type': skew,
            'interpretation': interpretation,
            'trading_implication': self._get_skew_implication(skew)
        }
    
    def _get_skew_implication(self, skew):
        """Get trading implications from volatility skew"""
        if skew == 'PUT_SKEW':
            return 'Consider selling puts or buying calls'
        elif skew == 'CALL_SKEW':
            return 'Consider selling calls or buying puts'
        else:
            return 'Follow technical analysis'
    
    def _detect_unwinding_signals(self, pcr, sentiment):
        """Detect options unwinding signals"""
        if pcr > 1.5 and sentiment == 'BULLISH':
            return {
                'signal': 'PUT_UNWINDING',
                'interpretation': 'Put unwinding may lead to short covering rally',
                'confidence': 'HIGH'
            }
        elif pcr < 0.5 and sentiment == 'BEARISH':
            return {
                'signal': 'CALL_UNWINDING',
                'interpretation': 'Call unwinding may lead to profit booking',
                'confidence': 'HIGH'
            }
        else:
            return {
                'signal': 'NO_UNWINDING',
                'interpretation': 'Normal options activity',
                'confidence': 'LOW'
            }
    
    def _analyze_rollover_patterns(self, pcr, sentiment):
        """Analyze options rollover patterns"""
        # This would typically analyze expiry-wise OI changes
        return {
            'pattern': 'NORMAL_ROLLOVER',
            'interpretation': 'Standard rollover activity',
            'impact': 'MINIMAL'
        }
    
    def _generate_trading_signals(self, oi_analysis):
        """Generate trading signals based on OI analysis"""
        signals = []
        
        pcr_interpretation = oi_analysis.get('pcr_interpretation', {})
        oi_buildup = oi_analysis.get('oi_buildup', {})
        max_pain = oi_analysis.get('max_pain_analysis', {})
        
        # Signal 1: PCR-based signals
        if pcr_interpretation.get('signal') == 'EXTREME_FEAR':
            signals.append({
                'type': 'BUY_CALL',
                'reason': 'Extreme fear in market, potential reversal',
                'confidence': pcr_interpretation.get('confidence', 'MEDIUM'),
                'timeframe': 'SHORT_TERM',
                'risk_level': 'MEDIUM'
            })
        elif pcr_interpretation.get('signal') == 'EXTREME_GREED':
            signals.append({
                'type': 'BUY_PUT',
                'reason': 'Extreme greed in market, potential reversal',
                'confidence': pcr_interpretation.get('confidence', 'MEDIUM'),
                'timeframe': 'SHORT_TERM',
                'risk_level': 'MEDIUM'
            })
        
        # Signal 2: OI buildup signals
        if oi_buildup.get('pattern') == 'PUT_BUILDUP':
            signals.append({
                'type': 'BUY_CALL',
                'reason': 'Heavy put buildup, potential short squeeze',
                'confidence': 'HIGH',
                'timeframe': 'SHORT_TERM',
                'risk_level': 'HIGH'
            })
        elif oi_buildup.get('pattern') == 'CALL_BUILDUP':
            signals.append({
                'type': 'BUY_PUT',
                'reason': 'Heavy call buildup, potential reversal',
                'confidence': 'HIGH',
                'timeframe': 'SHORT_TERM',
                'risk_level': 'HIGH'
            })
        
        # Signal 3: Max pain signals
        if max_pain and max_pain.get('probability') == 'HIGH':
            max_pain_level = max_pain.get('max_pain_level', 0)
            signals.append({
                'type': 'MAX_PAIN_TRADE',
                'reason': f'Price likely to gravitate towards {max_pain_level}',
                'confidence': 'MEDIUM',
                'timeframe': 'MEDIUM_TERM',
                'risk_level': 'LOW'
            })
        
        return signals
    
    def get_oi_cheatsheet(self):
        """Master cheatsheet for OI analysis"""
        return {
            'pcr_interpretation': {
                'PCR > 1.5': 'Extreme fear - Buy calls',
                'PCR 1.2-1.5': 'Fear - Consider calls on dips',
                'PCR 0.8-1.2': 'Neutral - Follow technicals',
                'PCR 0.5-0.8': 'Greed - Consider puts',
                'PCR < 0.5': 'Extreme greed - Buy puts'
            },
            'oi_patterns': {
                'High PCR + Bearish Sentiment': 'PUT_BUILDUP - Potential reversal',
                'Low PCR + Bullish Sentiment': 'CALL_BUILDUP - Potential reversal',
                'PCR Spike': 'Unwinding signal - High volatility expected',
                'PCR Drop': 'Covering signal - Trend continuation likely'
            },
            'trading_rules': {
                'Buy Calls When': [
                    'PCR > 1.5 (extreme fear)',
                    'Heavy put buildup detected',
                    'Price near strong support',
                    'RSI oversold (< 30)'
                ],
                'Buy Puts When': [
                    'PCR < 0.5 (extreme greed)',
                    'Heavy call buildup detected',
                    'Price near strong resistance',
                    'RSI overbought (> 70)'
                ],
                'Avoid Trading When': [
                    'PCR between 0.8-1.2 (neutral)',
                    'Low volume',
                    'Major news events pending',
                    'Expiry week (high gamma)'
                ]
            },
            'risk_management': {
                'Position Sizing': '2% risk per trade',
                'Stop Loss': '5% from entry',
                'Take Profit': '15% from entry',
                'Max Positions': '3 concurrent trades'
            }
        }
