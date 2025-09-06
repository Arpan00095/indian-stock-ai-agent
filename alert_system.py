import asyncio
import schedule
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import json
from data_fetcher import IndianMarketDataFetcher
from oi_analyzer import OIAnalyzer
from config import Config

logger = logging.getLogger(__name__)

class AlertSystem:
    def __init__(self):
        self.config = Config()
        self.data_fetcher = IndianMarketDataFetcher()
        self.oi_analyzer = OIAnalyzer()
        self.active_alerts = {}
        self.alert_history = []
        
    def setup_breakout_alerts(self, symbol: str, levels: Dict, alert_type: str = "both"):
        """Setup breakout/breakdown alerts for a symbol"""
        try:
            current_data = self.data_fetcher.get_live_price(symbol)
            if not current_data:
                return False
            
            current_price = current_data['price']
            resistance_levels = levels.get('resistance_levels', [])
            support_levels = levels.get('support_levels', [])
            
            # Find nearest levels
            nearest_resistance = min([r for r in resistance_levels if r > current_price], default=None)
            nearest_support = max([s for s in support_levels if s < current_price], default=None)
            
            alert_id = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            alert_config = {
                'symbol': symbol,
                'current_price': current_price,
                'nearest_resistance': nearest_resistance,
                'nearest_support': nearest_support,
                'alert_type': alert_type,
                'created_at': datetime.now(),
                'status': 'ACTIVE',
                'breakout_confirmed': False,
                'breakdown_confirmed': False
            }
            
            self.active_alerts[alert_id] = alert_config
            logger.info(f"Alert setup for {symbol}: Resistance {nearest_resistance}, Support {nearest_support}")
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Error setting up alerts for {symbol}: {e}")
            return None
    
    def check_breakout_alerts(self):
        """Check all active alerts for breakouts/breakdowns"""
        alerts_to_remove = []
        
        for alert_id, alert_config in self.active_alerts.items():
            if alert_config['status'] != 'ACTIVE':
                continue
                
            try:
                symbol = alert_config['symbol']
                current_data = self.data_fetcher.get_live_price(symbol)
                
                if not current_data:
                    continue
                
                current_price = current_data['price']
                nearest_resistance = alert_config['nearest_resistance']
                nearest_support = alert_config['nearest_support']
                
                # Check for breakout
                if nearest_resistance and current_price > nearest_resistance:
                    if not alert_config['breakout_confirmed']:
                        alert_config['breakout_confirmed'] = True
                        alert_config['breakout_price'] = current_price
                        alert_config['breakout_time'] = datetime.now()
                        
                        # Generate breakout signal
                        signal = self._generate_breakout_signal(symbol, 'BREAKOUT', current_price, nearest_resistance)
                        self._send_alert(signal)
                        
                        logger.info(f"BREAKOUT ALERT: {symbol} broke above {nearest_resistance} at {current_price}")
                
                # Check for breakdown
                elif nearest_support and current_price < nearest_support:
                    if not alert_config['breakdown_confirmed']:
                        alert_config['breakdown_confirmed'] = True
                        alert_config['breakdown_price'] = current_price
                        alert_config['breakdown_time'] = datetime.now()
                        
                        # Generate breakdown signal
                        signal = self._generate_breakout_signal(symbol, 'BREAKDOWN', current_price, nearest_support)
                        self._send_alert(signal)
                        
                        logger.info(f"BREAKDOWN ALERT: {symbol} broke below {nearest_support} at {current_price}")
                
                # Check for confirmation (multiple candles above/below level)
                if alert_config['breakout_confirmed'] or alert_config['breakdown_confirmed']:
                    confirmation = self._check_breakout_confirmation(symbol, alert_config)
                    if confirmation:
                        alert_config['status'] = 'CONFIRMED'
                        alerts_to_remove.append(alert_id)
                        
            except Exception as e:
                logger.error(f"Error checking alert {alert_id}: {e}")
        
        # Remove confirmed alerts
        for alert_id in alerts_to_remove:
            self.alert_history.append(self.active_alerts[alert_id])
            del self.active_alerts[alert_id]
    
    def _check_breakout_confirmation(self, symbol: str, alert_config: Dict) -> bool:
        """Check if breakout/breakdown is confirmed by multiple candles"""
        try:
            # Get recent intraday data
            data = self.data_fetcher.get_intraday_data(symbol, interval="5m")
            if data is None or len(data) < 3:
                return False
            
            recent_data = data.tail(3)
            
            if alert_config['breakout_confirmed']:
                # Check if price stayed above resistance for multiple candles
                resistance = alert_config['nearest_resistance']
                return all(recent_data['Close'] > resistance)
            
            elif alert_config['breakdown_confirmed']:
                # Check if price stayed below support for multiple candles
                support = alert_config['nearest_support']
                return all(recent_data['Close'] < support)
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking breakout confirmation: {e}")
            return False
    
    def _generate_breakout_signal(self, symbol: str, signal_type: str, current_price: float, level: float) -> Dict:
        """Generate trading signal for breakout/breakdown"""
        try:
            # Get OI analysis
            oi_analysis = self.oi_analyzer.analyze_oi_data(symbol)
            
            # Calculate entry, TP, SL
            if signal_type == 'BREAKOUT':
                entry_price = current_price
                stop_loss = level * 0.98  # 2% below breakout level
                take_profit = entry_price + (entry_price - stop_loss) * 2  # 2:1 risk-reward
                action = 'BUY_CALL'
            else:  # BREAKDOWN
                entry_price = current_price
                stop_loss = level * 1.02  # 2% above breakdown level
                take_profit = entry_price - (stop_loss - entry_price) * 2  # 2:1 risk-reward
                action = 'BUY_PUT'
            
            # Calculate position size
            risk_amount = self.config.DEFAULT_CAPITAL * self.config.MAX_RISK_PER_TRADE
            position_size = risk_amount / abs(entry_price - stop_loss)
            
            signal = {
                'symbol': symbol,
                'signal_type': signal_type,
                'action': action,
                'entry_price': round(entry_price, 2),
                'stop_loss': round(stop_loss, 2),
                'take_profit': round(take_profit, 2),
                'position_size': round(position_size, 0),
                'risk_amount': risk_amount,
                'level_broken': level,
                'current_price': current_price,
                'oi_analysis': oi_analysis.get('oi_analysis', {}) if oi_analysis else {},
                'confidence': 'HIGH' if oi_analysis else 'MEDIUM',
                'timestamp': datetime.now(),
                'alert_message': self._format_alert_message(symbol, signal_type, action, entry_price, stop_loss, take_profit)
            }
            
            return signal
            
        except Exception as e:
            logger.error(f"Error generating breakout signal: {e}")
            return {}
    
    def _format_alert_message(self, symbol: str, signal_type: str, action: str, entry: float, sl: float, tp: float) -> str:
        """Format alert message for notifications"""
        emoji_map = {
            'BREAKOUT': '🚀',
            'BREAKDOWN': '📉',
            'BUY_CALL': '📈',
            'BUY_PUT': '📉'
        }
        
        message = f"""
{emoji_map.get(signal_type, '⚠️')} {signal_type} ALERT - {symbol}

{emoji_map.get(action, '💰')} Action: {action}
💰 Entry: ₹{entry}
🛑 Stop Loss: ₹{sl}
🎯 Take Profit: ₹{tp}

Risk: ₹{abs(entry - sl):.2f}
Reward: ₹{abs(tp - entry):.2f}
Risk-Reward: {abs(tp - entry) / abs(entry - sl):.1f}:1

⏰ Time: {datetime.now().strftime('%H:%M:%S')}
        """
        
        return message.strip()
    
    def _send_alert(self, signal: Dict):
        """Send alert through configured channels"""
        if not signal:
            return
        
        message = signal.get('alert_message', '')
        
        # Log the alert
        logger.info(f"ALERT SENT: {signal['symbol']} - {signal['signal_type']}")
        
        # Here you would integrate with actual notification services
        # For now, we'll just print to console
        print("\n" + "="*50)
        print("🚨 BREAKOUT/BREAKDOWN ALERT 🚨")
        print("="*50)
        print(message)
        print("="*50 + "\n")
        
        # TODO: Integrate with Twilio, Telegram, etc.
        # self._send_sms_alert(message)
        # self._send_telegram_alert(message)
    
    def setup_pcr_alerts(self, symbol: str, pcr_threshold: float = 1.5):
        """Setup PCR-based alerts"""
        alert_id = f"PCR_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        alert_config = {
            'symbol': symbol,
            'alert_type': 'PCR',
            'pcr_threshold': pcr_threshold,
            'created_at': datetime.now(),
            'status': 'ACTIVE'
        }
        
        self.active_alerts[alert_id] = alert_config
        return alert_id
    
    def check_pcr_alerts(self):
        """Check PCR-based alerts"""
        for alert_id, alert_config in self.active_alerts.items():
            if alert_config.get('alert_type') != 'PCR':
                continue
                
            try:
                symbol = alert_config['symbol']
                pcr_data = self.data_fetcher.calculate_pcr(symbol)
                
                if pcr_data and pcr_data.get('pcr', 0) > alert_config['pcr_threshold']:
                    message = f"PCR ALERT: {symbol} PCR is {pcr_data['pcr']:.2f} (above {alert_config['pcr_threshold']})"
                    logger.info(message)
                    print(f"🚨 {message}")
                    
                    # Mark alert as triggered
                    alert_config['status'] = 'TRIGGERED'
                    
            except Exception as e:
                logger.error(f"Error checking PCR alert {alert_id}: {e}")
    
    def get_active_alerts(self) -> Dict:
        """Get all active alerts"""
        return self.active_alerts
    
    def get_alert_history(self) -> List[Dict]:
        """Get alert history"""
        return self.alert_history
    
    def cancel_alert(self, alert_id: str) -> bool:
        """Cancel an active alert"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id]['status'] = 'CANCELLED'
            self.alert_history.append(self.active_alerts[alert_id])
            del self.active_alerts[alert_id]
            return True
        return False
    
    def start_monitoring(self):
        """Start the alert monitoring system"""
        logger.info("Starting alert monitoring system...")
        
        # Schedule alert checks
        schedule.every(30).seconds.do(self.check_breakout_alerts)
        schedule.every(60).seconds.do(self.check_pcr_alerts)
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Alert monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in alert monitoring: {e}")
                time.sleep(5)
    
    def setup_volume_alert(self, symbol: str, volume_threshold: float = 2.0):
        """Setup volume-based alerts"""
        alert_id = f"VOLUME_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        alert_config = {
            'symbol': symbol,
            'alert_type': 'VOLUME',
            'volume_threshold': volume_threshold,
            'created_at': datetime.now(),
            'status': 'ACTIVE'
        }
        
        self.active_alerts[alert_id] = alert_config
        return alert_id
    
    def check_volume_alerts(self):
        """Check volume-based alerts"""
        for alert_id, alert_config in self.active_alerts.items():
            if alert_config.get('alert_type') != 'VOLUME':
                continue
                
            try:
                symbol = alert_config['symbol']
                live_data = self.data_fetcher.get_live_price(symbol)
                
                if live_data:
                    # Get historical volume data for comparison
                    hist_data = self.data_fetcher.get_historical_data(symbol, period="5d")
                    if hist_data is not None and len(hist_data) > 0:
                        avg_volume = hist_data['Volume'].mean()
                        current_volume = live_data['volume']
                        
                        if current_volume > avg_volume * alert_config['volume_threshold']:
                            message = f"VOLUME ALERT: {symbol} volume is {current_volume:,.0f} ({(current_volume/avg_volume):.1f}x average)"
                            logger.info(message)
                            print(f"📊 {message}")
                            
                            alert_config['status'] = 'TRIGGERED'
                            
            except Exception as e:
                logger.error(f"Error checking volume alert {alert_id}: {e}")
