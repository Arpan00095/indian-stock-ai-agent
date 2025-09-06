#!/usr/bin/env python3
"""
TradingView Alert Script for Advanced Intraday Trading
Receives webhook alerts from TradingView and executes trades on DHAN/GROWW/SENSIBULL
"""

import json
import requests
import logging
import time
from datetime import datetime
from typing import Dict, Optional
from flask import Flask, request, jsonify
import threading
from queue import Queue
import hmac
import hashlib
import base64

# Import our trading engine
from advanced_trading_engine import AdvancedTradingEngine, TradingSignal, OrderSide, OrderType, BrokerType
from advanced_config import CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app for webhook
app = Flask(__name__)

# Trading engine instance
trading_engine = None
alert_queue = Queue()

class TradingViewAlertHandler:
    """Handle TradingView alerts and convert to trading signals"""
    
    def __init__(self, trading_engine: AdvancedTradingEngine):
        self.trading_engine = trading_engine
        self.webhook_secret = CONFIG.get('webhook_secret', 'your_webhook_secret')
        
    def process_alert(self, alert_data: Dict) -> Optional[TradingSignal]:
        """Process TradingView alert and convert to trading signal"""
        try:
            # Extract alert information
            symbol = alert_data.get('symbol', '').upper()
            strategy = alert_data.get('strategy', 'TradingView')
            action = alert_data.get('action', '').upper()
            price = float(alert_data.get('price', 0))
            quantity = int(alert_data.get('quantity', 100))
            stop_loss = float(alert_data.get('stop_loss', 0))
            take_profit = float(alert_data.get('take_profit', 0))
            confidence = float(alert_data.get('confidence', 0.7))
            broker = alert_data.get('broker', 'dhan').lower()
            
            # Validate required fields
            if not symbol or not action or price <= 0:
                logger.error(f"Invalid alert data: {alert_data}")
                return None
            
            # Convert action to order side
            if action in ['BUY', 'LONG', 'CALL']:
                side = OrderSide.BUY
            elif action in ['SELL', 'SHORT', 'PUT']:
                side = OrderSide.SELL
            else:
                logger.error(f"Invalid action: {action}")
                return None
            
            # Convert broker string to enum
            broker_enum = {
                'dhan': BrokerType.DHAN,
                'groww': BrokerType.GROWW,
                'sensibull': BrokerType.SENSIBULL
            }.get(broker, BrokerType.DHAN)
            
            # Calculate default SL/TP if not provided
            if stop_loss <= 0:
                if side == OrderSide.BUY:
                    stop_loss = price * (1 - CONFIG.DEFAULT_STOP_LOSS_PERCENTAGE)
                else:
                    stop_loss = price * (1 + CONFIG.DEFAULT_STOP_LOSS_PERCENTAGE)
            
            if take_profit <= 0:
                if side == OrderSide.BUY:
                    take_profit = price * (1 + CONFIG.DEFAULT_TAKE_PROFIT_PERCENTAGE)
                else:
                    take_profit = price * (1 - CONFIG.DEFAULT_TAKE_PROFIT_PERCENTAGE)
            
            # Create trading signal
            signal = TradingSignal(
                symbol=symbol,
                side=side,
                order_type=OrderType.MARKET,
                quantity=quantity,
                price=price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                strategy=strategy,
                confidence=confidence,
                timestamp=datetime.now(),
                broker=broker_enum
            )
            
            logger.info(f"✅ TradingView alert processed: {symbol} {action} {quantity} @ {price}")
            return signal
            
        except Exception as e:
            logger.error(f"Error processing TradingView alert: {e}")
            return None
    
    def validate_webhook_signature(self, payload: str, signature: str) -> bool:
        """Validate TradingView webhook signature"""
        try:
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Error validating webhook signature: {e}")
            return False

# Webhook endpoints
@app.route('/webhook/tradingview', methods=['POST'])
def tradingview_webhook():
    """Handle TradingView webhook alerts"""
    try:
        # Get request data
        payload = request.get_data(as_text=True)
        signature = request.headers.get('X-Signature', '')
        
        # Validate signature (if configured)
        if CONFIG.get('webhook_secret'):
            if not TradingViewAlertHandler.validate_webhook_signature(payload, signature):
                logger.warning("Invalid webhook signature")
                return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse JSON data
        alert_data = json.loads(payload)
        logger.info(f"📨 Received TradingView alert: {alert_data}")
        
        # Process alert
        if trading_engine:
            handler = TradingViewAlertHandler(trading_engine)
            signal = handler.process_alert(alert_data)
            
            if signal:
                # Add to trading engine signal queue
                trading_engine.signal_queue.put(signal)
                logger.info(f"🚀 Signal queued for execution: {signal.symbol} {signal.side.value}")
                
                return jsonify({
                    'status': 'success',
                    'message': f'Signal processed: {signal.symbol} {signal.side.value}',
                    'signal_id': id(signal)
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to process alert'
                }), 400
        else:
            return jsonify({
                'status': 'error',
                'message': 'Trading engine not initialized'
            }), 500
            
    except Exception as e:
        logger.error(f"Error handling TradingView webhook: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/webhook/custom', methods=['POST'])
def custom_webhook():
    """Handle custom webhook alerts"""
    try:
        data = request.json
        
        # Extract custom alert data
        symbol = data.get('symbol', '').upper()
        action = data.get('action', '').upper()
        price = float(data.get('price', 0))
        quantity = int(data.get('quantity', 100))
        broker = data.get('broker', 'dhan').lower()
        
        # Create alert data
        alert_data = {
            'symbol': symbol,
            'action': action,
            'price': price,
            'quantity': quantity,
            'broker': broker,
            'strategy': 'Custom',
            'confidence': 0.8
        }
        
        # Process using TradingView handler
        if trading_engine:
            handler = TradingViewAlertHandler(trading_engine)
            signal = handler.process_alert(alert_data)
            
            if signal:
                trading_engine.signal_queue.put(signal)
                return jsonify({
                    'status': 'success',
                    'message': f'Custom signal processed: {symbol} {action}'
                })
        
        return jsonify({
            'status': 'error',
            'message': 'Failed to process custom alert'
        }), 400
        
    except Exception as e:
        logger.error(f"Error handling custom webhook: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """Get trading engine status"""
    if trading_engine:
        portfolio = trading_engine.get_portfolio_summary()
        return jsonify({
            'status': 'running',
            'total_positions': portfolio['total_positions'],
            'total_pnl': portfolio['total_pnl'],
            'total_exposure': portfolio['total_exposure'],
            'positions': portfolio['positions']
        })
    else:
        return jsonify({
            'status': 'stopped',
            'message': 'Trading engine not running'
        })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

def start_webhook_server(host='0.0.0.0', port=5000):
    """Start the webhook server"""
    logger.info(f"🌐 Starting webhook server on {host}:{port}")
    app.run(host=host, port=port, debug=False)

def create_tradingview_alert_example():
    """Create example TradingView alert configuration"""
    example_alert = {
        "webhook_url": "http://your-server:5000/webhook/tradingview",
        "alert_message": """
        {
            "symbol": "NIFTY50",
            "action": "BUY",
            "price": {{close}},
            "quantity": 100,
            "stop_loss": {{close * 0.98}},
            "take_profit": {{close * 1.02}},
            "strategy": "Momentum",
            "confidence": 0.8,
            "broker": "dhan"
        }
        """,
        "tradingview_pine_script": """
        //@version=5
        strategy("Advanced Intraday Trading", overlay=true)
        
        // Strategy parameters
        rsi_length = input(14, "RSI Length")
        rsi_overbought = input(70, "RSI Overbought")
        rsi_oversold = input(30, "RSI Oversold")
        
        // Calculate RSI
        rsi = ta.rsi(close, rsi_length)
        
        // Entry conditions
        long_condition = rsi < rsi_oversold and close > close[1]
        short_condition = rsi > rsi_overbought and close < close[1]
        
        // Strategy entries
        if long_condition
            strategy.entry("Long", strategy.long)
            alert("BUY Signal", alert.freq_once_per_bar)
        
        if short_condition
            strategy.entry("Short", strategy.short)
            alert("SELL Signal", alert.freq_once_per_bar)
        
        // Plot signals
        plotshape(long_condition, "Buy Signal", shape.triangleup, location.belowbar, color.green, size=size.small)
        plotshape(short_condition, "Sell Signal", shape.triangledown, location.abovebar, color.red, size=size.small)
        """
    }
    
    return example_alert

def main():
    """Main function to run the TradingView alert handler"""
    global trading_engine
    
    logger.info("🚀 Starting TradingView Alert Handler")
    
    # Initialize trading engine
    try:
        trading_engine = AdvancedTradingEngine(CONFIG.__dict__)
        logger.info("✅ Trading engine initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize trading engine: {e}")
        return
    
    # Start trading engine in background
    def run_trading_engine():
        import asyncio
        asyncio.run(trading_engine.start_trading())
    
    trading_thread = threading.Thread(target=run_trading_engine, daemon=True)
    trading_thread.start()
    
    # Start webhook server
    try:
        start_webhook_server()
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down TradingView Alert Handler")
    except Exception as e:
        logger.error(f"❌ Error running webhook server: {e}")

if __name__ == "__main__":
    # Print example configuration
    print("📋 TradingView Alert Configuration Example:")
    print("=" * 50)
    example = create_tradingview_alert_example()
    print(f"Webhook URL: {example['webhook_url']}")
    print("\nAlert Message (JSON):")
    print(example['alert_message'])
    print("\nTradingView Pine Script:")
    print(example['tradingview_pine_script'])
    print("\n" + "=" * 50)
    
    # Start the application
    main()
