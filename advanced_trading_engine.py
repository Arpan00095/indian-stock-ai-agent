#!/usr/bin/env python3
"""
Advanced Intraday Trading Engine for Indian Indices
Integrated with DHAN, GROWW, and SENSIBULL brokers
"""

import asyncio
import websockets
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading
from queue import Queue
import hmac
import hashlib
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrokerType(Enum):
    DHAN = "dhan"
    GROWW = "groww"
    SENSIBULL = "sensibull"

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"
    SL_M = "SL_M"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class TradingSignal:
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: float
    stop_loss: float
    take_profit: float
    strategy: str
    confidence: float
    timestamp: datetime
    broker: BrokerType

@dataclass
class Position:
    symbol: str
    quantity: int
    side: OrderSide
    entry_price: float
    current_price: float
    pnl: float
    stop_loss: float
    take_profit: float
    broker: BrokerType

class AdvancedTradingEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.brokers = {}
        self.positions = {}
        self.signal_queue = Queue()
        self.is_running = False
        self.risk_manager = RiskManager(config)
        self.strategy_manager = StrategyManager(config)
        
        # Initialize brokers
        self._initialize_brokers()
        
    def _initialize_brokers(self):
        """Initialize broker connections"""
        if self.config.get('dhan_enabled'):
            self.brokers[BrokerType.DHAN] = DhanBroker(self.config['dhan_config'])
            
        if self.config.get('groww_enabled'):
            self.brokers[BrokerType.GROWW] = GrowwBroker(self.config['groww_config'])
            
        if self.config.get('sensibull_enabled'):
            self.brokers[BrokerType.SENSIBULL] = SensibullBroker(self.config['sensibull_config'])
    
    async def start_trading(self):
        """Start the advanced trading engine"""
        self.is_running = True
        logger.info("🚀 Starting Advanced Intraday Trading Engine")
        
        # Start multiple threads
        threads = [
            threading.Thread(target=self._signal_processor, daemon=True),
            threading.Thread(target=self._position_monitor, daemon=True),
            threading.Thread(target=self._risk_monitor, daemon=True),
            threading.Thread(target=self._market_data_stream, daemon=True)
        ]
        
        for thread in threads:
            thread.start()
        
        # Main trading loop
        while self.is_running:
            try:
                await self._trading_cycle()
                await asyncio.sleep(1)  # 1-second cycle
            except Exception as e:
                logger.error(f"Error in trading cycle: {e}")
                await asyncio.sleep(5)
    
    async def _trading_cycle(self):
        """Main trading cycle for intraday trading"""
        current_time = datetime.now()
        
        # Check if market is open
        if not self._is_market_open(current_time):
            return
        
        # Get market data
        market_data = await self._get_market_data()
        
        # Generate trading signals
        signals = self.strategy_manager.generate_signals(market_data)
        
        # Process signals
        for signal in signals:
            if self.risk_manager.validate_signal(signal):
                self.signal_queue.put(signal)
    
    def _signal_processor(self):
        """Process trading signals and execute orders"""
        while self.is_running:
            try:
                if not self.signal_queue.empty():
                    signal = self.signal_queue.get()
                    self._execute_signal(signal)
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in signal processor: {e}")
    
    def _execute_signal(self, signal: TradingSignal):
        """Execute trading signal on specified broker"""
        try:
            broker = self.brokers.get(signal.broker)
            if not broker:
                logger.error(f"Broker {signal.broker} not available")
                return
            
            # Execute order
            order_id = broker.place_order(
                symbol=signal.symbol,
                side=signal.side,
                order_type=signal.order_type,
                quantity=signal.quantity,
                price=signal.price
            )
            
            if order_id:
                logger.info(f"✅ Order executed: {signal.symbol} {signal.side.value} {signal.quantity} @ {signal.price}")
                
                # Add to positions
                self.positions[order_id] = Position(
                    symbol=signal.symbol,
                    quantity=signal.quantity,
                    side=signal.side,
                    entry_price=signal.price,
                    current_price=signal.price,
                    pnl=0.0,
                    stop_loss=signal.stop_loss,
                    take_profit=signal.take_profit,
                    broker=signal.broker
                )
            
        except Exception as e:
            logger.error(f"Error executing signal: {e}")
    
    def _position_monitor(self):
        """Monitor open positions and manage SL/TP"""
        while self.is_running:
            try:
                for order_id, position in self.positions.items():
                    # Update current price
                    broker = self.brokers.get(position.broker)
                    if broker:
                        current_price = broker.get_live_price(position.symbol)
                        position.current_price = current_price
                        
                        # Calculate P&L
                        if position.side == OrderSide.BUY:
                            position.pnl = (current_price - position.entry_price) * position.quantity
                        else:
                            position.pnl = (position.entry_price - current_price) * position.quantity
                        
                        # Check SL/TP
                        self._check_sl_tp(position, broker)
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in position monitor: {e}")
    
    def _check_sl_tp(self, position: Position, broker):
        """Check and execute stop loss or take profit"""
        current_price = position.current_price
        
        # Check stop loss
        if position.side == OrderSide.BUY and current_price <= position.stop_loss:
            self._close_position(position, broker, "Stop Loss")
        elif position.side == OrderSide.SELL and current_price >= position.stop_loss:
            self._close_position(position, broker, "Stop Loss")
        
        # Check take profit
        elif position.side == OrderSide.BUY and current_price >= position.take_profit:
            self._close_position(position, broker, "Take Profit")
        elif position.side == OrderSide.SELL and current_price <= position.take_profit:
            self._close_position(position, broker, "Take Profit")
    
    def _close_position(self, position: Position, broker, reason: str):
        """Close position"""
        try:
            close_side = OrderSide.SELL if position.side == OrderSide.BUY else OrderSide.BUY
            
            order_id = broker.place_order(
                symbol=position.symbol,
                side=close_side,
                order_type=OrderType.MARKET,
                quantity=position.quantity,
                price=0  # Market order
            )
            
            if order_id:
                logger.info(f"🔄 Position closed: {position.symbol} - {reason} - P&L: ₹{position.pnl:.2f}")
                # Remove from positions
                for key, pos in list(self.positions.items()):
                    if pos == position:
                        del self.positions[key]
                        break
                        
        except Exception as e:
            logger.error(f"Error closing position: {e}")
    
    def _risk_monitor(self):
        """Monitor risk limits and portfolio exposure"""
        while self.is_running:
            try:
                total_exposure = sum(abs(pos.quantity * pos.current_price) for pos in self.positions.values())
                max_exposure = self.config.get('max_exposure', 100000)
                
                if total_exposure > max_exposure:
                    logger.warning(f"⚠️ Risk limit exceeded: ₹{total_exposure:,.2f} > ₹{max_exposure:,.2f}")
                    self._reduce_exposure()
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error in risk monitor: {e}")
    
    def _reduce_exposure(self):
        """Reduce portfolio exposure by closing some positions"""
        # Close positions with lowest P&L first
        sorted_positions = sorted(self.positions.values(), key=lambda x: x.pnl)
        
        for position in sorted_positions[:2]:  # Close 2 positions
            broker = self.brokers.get(position.broker)
            if broker:
                self._close_position(position, broker, "Risk Management")
    
    async def _market_data_stream(self):
        """Stream real-time market data"""
        while self.is_running:
            try:
                # Get live data for major indices
                indices = ['^NSEI', '^NSEBANK', 'NIFTY_FIN_SERVICE.NS']
                
                for index in indices:
                    data = await self._get_index_data(index)
                    if data:
                        self.strategy_manager.update_market_data(index, data)
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in market data stream: {e}")
                await asyncio.sleep(5)
    
    async def _get_index_data(self, symbol: str) -> Optional[Dict]:
        """Get real-time index data"""
        try:
            import yfinance as yf
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
            logger.error(f"Error getting index data for {symbol}: {e}")
            return None
    
    def _is_market_open(self, current_time: datetime) -> bool:
        """Check if market is open for intraday trading"""
        # Market hours: 9:15 AM to 3:30 PM IST
        market_open = current_time.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_open <= current_time <= market_close
    
    async def _get_market_data(self) -> Dict:
        """Get comprehensive market data"""
        data = {}
        
        # Get major indices
        indices = ['^NSEI', '^NSEBANK', 'NIFTY_FIN_SERVICE.NS']
        
        for index in indices:
            index_data = await self._get_index_data(index)
            if index_data:
                data[index] = index_data
        
        return data
    
    def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary"""
        total_pnl = sum(pos.pnl for pos in self.positions.values())
        total_exposure = sum(abs(pos.quantity * pos.current_price) for pos in self.positions.values())
        
        return {
            'total_positions': len(self.positions),
            'total_pnl': total_pnl,
            'total_exposure': total_exposure,
            'positions': [
                {
                    'symbol': pos.symbol,
                    'side': pos.side.value,
                    'quantity': pos.quantity,
                    'entry_price': pos.entry_price,
                    'current_price': pos.current_price,
                    'pnl': pos.pnl,
                    'broker': pos.broker.value
                }
                for pos in self.positions.values()
            ]
        }

class RiskManager:
    def __init__(self, config: Dict):
        self.config = config
        self.max_risk_per_trade = config.get('max_risk_per_trade', 0.02)  # 2%
        self.max_daily_loss = config.get('max_daily_loss', 0.05)  # 5%
        self.max_positions = config.get('max_positions', 5)
        self.daily_pnl = 0.0
    
    def validate_signal(self, signal: TradingSignal) -> bool:
        """Validate trading signal against risk parameters"""
        # Check position limit
        if len(self.get_current_positions()) >= self.max_positions:
            logger.warning("Maximum positions limit reached")
            return False
        
        # Check daily loss limit
        if self.daily_pnl < -(self.config.get('capital', 100000) * self.max_daily_loss):
            logger.warning("Daily loss limit reached")
            return False
        
        # Check risk per trade
        risk_amount = abs(signal.price - signal.stop_loss) * signal.quantity
        capital = self.config.get('capital', 100000)
        
        if risk_amount > (capital * self.max_risk_per_trade):
            logger.warning("Risk per trade limit exceeded")
            return False
        
        return True
    
    def get_current_positions(self) -> List:
        """Get current positions (placeholder)"""
        return []

class StrategyManager:
    def __init__(self, config: Dict):
        self.config = config
        self.market_data = {}
        self.strategies = {
            'momentum': MomentumStrategy(),
            'mean_reversion': MeanReversionStrategy(),
            'breakout': BreakoutStrategy(),
            'oi_analysis': OIAnalysisStrategy()
        }
    
    def update_market_data(self, symbol: str, data: Dict):
        """Update market data"""
        self.market_data[symbol] = data
    
    def generate_signals(self, market_data: Dict) -> List[TradingSignal]:
        """Generate trading signals using multiple strategies"""
        signals = []
        
        for symbol, data in market_data.items():
            for strategy_name, strategy in self.strategies.items():
                try:
                    signal = strategy.generate_signal(symbol, data, self.market_data)
                    if signal:
                        signals.append(signal)
                except Exception as e:
                    logger.error(f"Error in {strategy_name} strategy: {e}")
        
        return signals

# Strategy Classes
class MomentumStrategy:
    def generate_signal(self, symbol: str, data: Dict, market_data: Dict) -> Optional[TradingSignal]:
        """Generate momentum-based signals"""
        # Simple momentum strategy
        change_percent = data.get('change_percent', 0)
        
        if change_percent > 0.5:  # Strong momentum
            return TradingSignal(
                symbol=symbol,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=100,
                price=data['price'],
                stop_loss=data['price'] * 0.98,
                take_profit=data['price'] * 1.02,
                strategy="Momentum",
                confidence=0.7,
                timestamp=datetime.now(),
                broker=BrokerType.DHAN
            )
        elif change_percent < -0.5:  # Strong downward momentum
            return TradingSignal(
                symbol=symbol,
                side=OrderSide.SELL,
                order_type=OrderType.MARKET,
                quantity=100,
                price=data['price'],
                stop_loss=data['price'] * 1.02,
                take_profit=data['price'] * 0.98,
                strategy="Momentum",
                confidence=0.7,
                timestamp=datetime.now(),
                broker=BrokerType.DHAN
            )
        
        return None

class MeanReversionStrategy:
    def generate_signal(self, symbol: str, data: Dict, market_data: Dict) -> Optional[TradingSignal]:
        """Generate mean reversion signals"""
        # Simple mean reversion based on daily range
        high = data.get('high', 0)
        low = data.get('low', 0)
        current = data.get('price', 0)
        
        if high > 0 and low > 0:
            range_high = high - low
            current_position = (current - low) / range_high
            
            if current_position > 0.8:  # Near high - sell
                return TradingSignal(
                    symbol=symbol,
                    side=OrderSide.SELL,
                    order_type=OrderType.MARKET,
                    quantity=100,
                    price=current,
                    stop_loss=current * 1.01,
                    take_profit=current * 0.99,
                    strategy="MeanReversion",
                    confidence=0.6,
                    timestamp=datetime.now(),
                    broker=BrokerType.GROWW
                )
            elif current_position < 0.2:  # Near low - buy
                return TradingSignal(
                    symbol=symbol,
                    side=OrderSide.BUY,
                    order_type=OrderType.MARKET,
                    quantity=100,
                    price=current,
                    stop_loss=current * 0.99,
                    take_profit=current * 1.01,
                    strategy="MeanReversion",
                    confidence=0.6,
                    timestamp=datetime.now(),
                    broker=BrokerType.GROWW
                )
        
        return None

class BreakoutStrategy:
    def generate_signal(self, symbol: str, data: Dict, market_data: Dict) -> Optional[TradingSignal]:
        """Generate breakout signals"""
        # Simple breakout strategy
        high = data.get('high', 0)
        current = data.get('price', 0)
        
        if current >= high * 0.99:  # Near day high
            return TradingSignal(
                symbol=symbol,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=100,
                price=current,
                stop_loss=current * 0.98,
                take_profit=current * 1.02,
                strategy="Breakout",
                confidence=0.8,
                timestamp=datetime.now(),
                broker=BrokerType.SENSIBULL
            )
        
        return None

class OIAnalysisStrategy:
    def generate_signal(self, symbol: str, data: Dict, market_data: Dict) -> Optional[TradingSignal]:
        """Generate OI-based signals"""
        # Simplified OI analysis
        volume = data.get('volume', 0)
        change_percent = data.get('change_percent', 0)
        
        # High volume + price movement = potential OI buildup
        if volume > 1000000 and abs(change_percent) > 0.3:
            side = OrderSide.BUY if change_percent > 0 else OrderSide.SELL
            return TradingSignal(
                symbol=symbol,
                side=side,
                order_type=OrderType.MARKET,
                quantity=100,
                price=data['price'],
                stop_loss=data['price'] * (0.98 if side == OrderSide.BUY else 1.02),
                take_profit=data['price'] * (1.02 if side == OrderSide.BUY else 0.98),
                strategy="OIAnalysis",
                confidence=0.75,
                timestamp=datetime.now(),
                broker=BrokerType.DHAN
            )
        
        return None

# Broker Integration Classes
class DhanBroker:
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.api_secret = config.get('api_secret')
        self.base_url = "https://api.dhan.co"
        self.session = requests.Session()
    
    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                   quantity: int, price: float) -> Optional[str]:
        """Place order on DHAN"""
        try:
            # DHAN API integration (simplified)
            payload = {
                "symbol": symbol,
                "side": side.value,
                "orderType": order_type.value,
                "quantity": quantity,
                "price": price,
                "productType": "INTRADAY"
            }
            
            # Add authentication headers
            headers = self._get_auth_headers(payload)
            
            response = self.session.post(
                f"{self.base_url}/orders",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('orderId')
            else:
                logger.error(f"DHAN order failed: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing DHAN order: {e}")
            return None
    
    def get_live_price(self, symbol: str) -> float:
        """Get live price from DHAN"""
        try:
            response = self.session.get(f"{self.base_url}/quotes/{symbol}")
            if response.status_code == 200:
                data = response.json()
                return data.get('ltp', 0)
            return 0
        except Exception as e:
            logger.error(f"Error getting DHAN price: {e}")
            return 0
    
    def _get_auth_headers(self, payload: Dict) -> Dict:
        """Generate authentication headers for DHAN"""
        timestamp = str(int(time.time() * 1000))
        message = f"{self.api_key}{timestamp}"
        
        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return {
            "X-Dhan-Api-Key": self.api_key,
            "X-Dhan-Timestamp": timestamp,
            "X-Dhan-Signature": signature,
            "Content-Type": "application/json"
        }

class GrowwBroker:
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.api_secret = config.get('api_secret')
        self.base_url = "https://api.groww.in"
        self.session = requests.Session()
    
    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                   quantity: int, price: float) -> Optional[str]:
        """Place order on GROWW"""
        try:
            # GROWW API integration (simplified)
            payload = {
                "symbol": symbol,
                "side": side.value,
                "orderType": order_type.value,
                "quantity": quantity,
                "price": price,
                "productType": "INTRADAY"
            }
            
            headers = self._get_auth_headers()
            
            response = self.session.post(
                f"{self.base_url}/orders",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('orderId')
            else:
                logger.error(f"GROWW order failed: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing GROWW order: {e}")
            return None
    
    def get_live_price(self, symbol: str) -> float:
        """Get live price from GROWW"""
        try:
            response = self.session.get(f"{self.base_url}/quotes/{symbol}")
            if response.status_code == 200:
                data = response.json()
                return data.get('ltp', 0)
            return 0
        except Exception as e:
            logger.error(f"Error getting GROWW price: {e}")
            return 0
    
    def _get_auth_headers(self) -> Dict:
        """Generate authentication headers for GROWW"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

class SensibullBroker:
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.api_secret = config.get('api_secret')
        self.base_url = "https://api.sensibull.com"
        self.session = requests.Session()
    
    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                   quantity: int, price: float) -> Optional[str]:
        """Place order on SENSIBULL"""
        try:
            # SENSIBULL API integration (simplified)
            payload = {
                "symbol": symbol,
                "side": side.value,
                "orderType": order_type.value,
                "quantity": quantity,
                "price": price,
                "productType": "INTRADAY"
            }
            
            headers = self._get_auth_headers()
            
            response = self.session.post(
                f"{self.base_url}/orders",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('orderId')
            else:
                logger.error(f"SENSIBULL order failed: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing SENSIBULL order: {e}")
            return None
    
    def get_live_price(self, symbol: str) -> float:
        """Get live price from SENSIBULL"""
        try:
            response = self.session.get(f"{self.base_url}/quotes/{symbol}")
            if response.status_code == 200:
                data = response.json()
                return data.get('ltp', 0)
            return 0
        except Exception as e:
            logger.error(f"Error getting SENSIBULL price: {e}")
            return 0
    
    def _get_auth_headers(self) -> Dict:
        """Generate authentication headers for SENSIBULL"""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

# Configuration template
ADVANCED_CONFIG = {
    "capital": 100000,
    "max_risk_per_trade": 0.02,  # 2%
    "max_daily_loss": 0.05,  # 5%
    "max_positions": 5,
    "max_exposure": 100000,
    
    # Broker configurations
    "dhan_enabled": True,
    "dhan_config": {
        "api_key": "your_dhan_api_key",
        "api_secret": "your_dhan_api_secret"
    },
    
    "groww_enabled": True,
    "groww_config": {
        "api_key": "your_groww_api_key",
        "api_secret": "your_groww_api_secret"
    },
    
    "sensibull_enabled": True,
    "sensibull_config": {
        "api_key": "your_sensibull_api_key",
        "api_secret": "your_sensibull_api_secret"
    }
}

async def main():
    """Main function to run the advanced trading engine"""
    engine = AdvancedTradingEngine(ADVANCED_CONFIG)
    await engine.start_trading()

if __name__ == "__main__":
    asyncio.run(main())
