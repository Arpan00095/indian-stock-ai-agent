#!/usr/bin/env python3
"""
Advanced Configuration for Intraday Trading System
Broker integrations: DHAN, GROWW, SENSIBULL
"""

import os
from dotenv import load_dotenv

load_dotenv()

class AdvancedTradingConfig:
    """Advanced configuration for intraday trading"""
    
    # Capital and Risk Management
    CAPITAL = int(os.getenv('TRADING_CAPITAL', 100000))
    MAX_RISK_PER_TRADE = float(os.getenv('MAX_RISK_PER_TRADE', 0.02))  # 2%
    MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 0.05))  # 5%
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', 5))
    MAX_EXPOSURE = int(os.getenv('MAX_EXPOSURE', 100000))
    
    # Intraday Trading Parameters
    INTRADAY_MARGIN = float(os.getenv('INTRADAY_MARGIN', 0.20))  # 20% margin
    SQUARE_OFF_TIME = os.getenv('SQUARE_OFF_TIME', '15:15')  # 3:15 PM
    MARKET_OPEN_TIME = '09:15'
    MARKET_CLOSE_TIME = '15:30'
    
    # Strategy Parameters
    MOMENTUM_THRESHOLD = float(os.getenv('MOMENTUM_THRESHOLD', 0.5))  # 0.5%
    MEAN_REVERSION_THRESHOLD = float(os.getenv('MEAN_REVERSION_THRESHOLD', 0.8))
    BREAKOUT_CONFIRMATION = int(os.getenv('BREAKOUT_CONFIRMATION', 3))  # candles
    VOLUME_THRESHOLD = int(os.getenv('VOLUME_THRESHOLD', 1000000))
    
    # Stop Loss and Take Profit
    DEFAULT_STOP_LOSS_PERCENTAGE = float(os.getenv('DEFAULT_STOP_LOSS', 0.02))  # 2%
    DEFAULT_TAKE_PROFIT_PERCENTAGE = float(os.getenv('DEFAULT_TAKE_PROFIT', 0.04))  # 4%
    TRAILING_STOP = float(os.getenv('TRAILING_STOP', 0.01))  # 1%
    
    # Broker Configurations
    DHAN_ENABLED = os.getenv('DHAN_ENABLED', 'true').lower() == 'true'
    DHAN_CONFIG = {
        'api_key': os.getenv('DHAN_API_KEY'),
        'api_secret': os.getenv('DHAN_API_SECRET'),
        'user_id': os.getenv('DHAN_USER_ID'),
        'password': os.getenv('DHAN_PASSWORD'),
        'totp_key': os.getenv('DHAN_TOTP_KEY'),
        'base_url': 'https://api.dhan.co',
        'websocket_url': 'wss://stream.dhan.co'
    }
    
    GROWW_ENABLED = os.getenv('GROWW_ENABLED', 'true').lower() == 'true'
    GROWW_CONFIG = {
        'api_key': os.getenv('GROWW_API_KEY'),
        'api_secret': os.getenv('GROWW_API_SECRET'),
        'user_id': os.getenv('GROWW_USER_ID'),
        'password': os.getenv('GROWW_PASSWORD'),
        'base_url': 'https://api.groww.in',
        'websocket_url': 'wss://stream.groww.in'
    }
    
    SENSIBULL_ENABLED = os.getenv('SENSIBULL_ENABLED', 'true').lower() == 'true'
    SENSIBULL_CONFIG = {
        'api_key': os.getenv('SENSIBULL_API_KEY'),
        'api_secret': os.getenv('SENSIBULL_API_SECRET'),
        'user_id': os.getenv('SENSIBULL_USER_ID'),
        'password': os.getenv('SENSIBULL_PASSWORD'),
        'base_url': 'https://api.sensibull.com',
        'websocket_url': 'wss://stream.sensibull.com'
    }
    
    # Index Trading Symbols
    INDEX_SYMBOLS = {
        'NIFTY50': {
            'symbol': '^NSEI',
            'lot_size': 50,
            'tick_size': 0.05,
            'margin_required': 0.20,
            'max_quantity': 1000
        },
        'BANKNIFTY': {
            'symbol': '^NSEBANK',
            'lot_size': 25,
            'tick_size': 0.05,
            'margin_required': 0.20,
            'max_quantity': 500
        },
        'FINNIFTY': {
            'symbol': 'NIFTY_FIN_SERVICE.NS',
            'lot_size': 40,
            'tick_size': 0.05,
            'margin_required': 0.20,
            'max_quantity': 800
        },
        'MIDCPNIFTY': {
            'symbol': 'NIFTY_MIDCAP_100.NS',
            'lot_size': 75,
            'tick_size': 0.05,
            'margin_required': 0.20,
            'max_quantity': 600
        }
    }
    
    # Advanced Technical Indicators
    TECHNICAL_INDICATORS = {
        'rsi_period': int(os.getenv('RSI_PERIOD', 14)),
        'rsi_overbought': float(os.getenv('RSI_OVERBOUGHT', 70)),
        'rsi_oversold': float(os.getenv('RSI_OVERSOLD', 30)),
        'macd_fast': int(os.getenv('MACD_FAST', 12)),
        'macd_slow': int(os.getenv('MACD_SLOW', 26)),
        'macd_signal': int(os.getenv('MACD_SIGNAL', 9)),
        'bollinger_period': int(os.getenv('BOLLINGER_PERIOD', 20)),
        'bollinger_std': float(os.getenv('BOLLINGER_STD', 2)),
        'ema_short': int(os.getenv('EMA_SHORT', 9)),
        'ema_long': int(os.getenv('EMA_LONG', 21))
    }
    
    # OI Analysis Parameters
    OI_ANALYSIS = {
        'pcr_threshold_high': float(os.getenv('PCR_THRESHOLD_HIGH', 1.5)),
        'pcr_threshold_low': float(os.getenv('PCR_THRESHOLD_LOW', 0.5)),
        'oi_buildup_threshold': float(os.getenv('OI_BUILDUP_THRESHOLD', 0.1)),
        'max_pain_calculation': bool(os.getenv('MAX_PAIN_CALCULATION', 'true').lower() == 'true'),
        'gamma_exposure_threshold': float(os.getenv('GAMMA_EXPOSURE_THRESHOLD', 0.1))
    }
    
    # Alert Settings
    ALERTS = {
        'enable_sms': os.getenv('ENABLE_SMS', 'false').lower() == 'true',
        'enable_email': os.getenv('ENABLE_EMAIL', 'false').lower() == 'true',
        'enable_telegram': os.getenv('ENABLE_TELEGRAM', 'false').lower() == 'true',
        'enable_push': os.getenv('ENABLE_PUSH', 'true').lower() == 'true',
        'alert_frequency': int(os.getenv('ALERT_FREQUENCY', 30))  # seconds
    }
    
    # Notification Settings
    TWILIO_CONFIG = {
        'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
        'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
        'from_number': os.getenv('TWILIO_FROM_NUMBER'),
        'to_number': os.getenv('TWILIO_TO_NUMBER')
    }
    
    TELEGRAM_CONFIG = {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID')
    }
    
    EMAIL_CONFIG = {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        'email': os.getenv('EMAIL_ADDRESS'),
        'password': os.getenv('EMAIL_PASSWORD')
    }
    
    # Database Settings
    DATABASE = {
        'type': os.getenv('DATABASE_TYPE', 'sqlite'),
        'url': os.getenv('DATABASE_URL', 'sqlite:///trading_data.db'),
        'backup_enabled': os.getenv('DATABASE_BACKUP', 'true').lower() == 'true',
        'backup_frequency': int(os.getenv('BACKUP_FREQUENCY', 24))  # hours
    }
    
    # Logging Settings
    LOGGING = {
        'level': os.getenv('LOG_LEVEL', 'INFO'),
        'file': os.getenv('LOG_FILE', 'trading_engine.log'),
        'max_size': int(os.getenv('LOG_MAX_SIZE', 10)) * 1024 * 1024,  # 10MB
        'backup_count': int(os.getenv('LOG_BACKUP_COUNT', 5))
    }
    
    # Performance Settings
    PERFORMANCE = {
        'enable_profiling': os.getenv('ENABLE_PROFILING', 'false').lower() == 'true',
        'cache_enabled': os.getenv('CACHE_ENABLED', 'true').lower() == 'true',
        'cache_ttl': int(os.getenv('CACHE_TTL', 300))  # 5 minutes
    }
    
    # Market Data Settings
    MARKET_DATA = {
        'provider': os.getenv('MARKET_DATA_PROVIDER', 'yfinance'),
        'update_frequency': int(os.getenv('MARKET_DATA_FREQUENCY', 1))  # seconds
    }
    
    @classmethod
    def get_broker_config(cls, broker_name: str) -> dict:
        """Get broker configuration by name"""
        broker_configs = {
            'dhan': cls.DHAN_CONFIG,
            'groww': cls.GROWW_CONFIG,
            'sensibull': cls.SENSIBULL_CONFIG
        }
        return broker_configs.get(broker_name.lower(), {})
    
    @classmethod
    def get_index_config(cls, index_name: str) -> dict:
        """Get index configuration by name"""
        return cls.INDEX_SYMBOLS.get(index_name.upper(), {})
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check capital
        if cls.CAPITAL < 10000:
            errors.append("Trading capital must be at least ₹10,000")
        
        # Check risk parameters
        if cls.MAX_RISK_PER_TRADE > 0.05:
            errors.append("Max risk per trade should not exceed 5%")
        
        if cls.MAX_DAILY_LOSS > 0.10:
            errors.append("Max daily loss should not exceed 10%")
        
        # Check broker configurations
        if cls.DHAN_ENABLED and not cls.DHAN_CONFIG.get('api_key'):
            errors.append("DHAN API key is required when DHAN is enabled")
        
        if cls.GROWW_ENABLED and not cls.GROWW_CONFIG.get('api_key'):
            errors.append("GROWW API key is required when GROWW is enabled")
        
        if cls.SENSIBULL_ENABLED and not cls.SENSIBULL_CONFIG.get('api_key'):
            errors.append("SENSIBULL API key is required when SENSIBULL is enabled")
        
        if errors:
            print("Configuration errors found:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def print_config_summary(cls):
        """Print configuration summary"""
        print("🔧 Advanced Trading Configuration Summary")
        print("=" * 50)
        print(f"💰 Capital: ₹{cls.CAPITAL:,.2f}")
        print(f"⚠️ Max Risk per Trade: {cls.MAX_RISK_PER_TRADE*100:.1f}%")
        print(f"📉 Max Daily Loss: {cls.MAX_DAILY_LOSS*100:.1f}%")
        print(f"📊 Max Positions: {cls.MAX_POSITIONS}")
        print(f"💼 Max Exposure: ₹{cls.MAX_EXPOSURE:,.2f}")
        print()
        print("🏢 Broker Status:")
        print(f"  DHAN: {'✅ Enabled' if cls.DHAN_ENABLED else '❌ Disabled'}")
        print(f"  GROWW: {'✅ Enabled' if cls.GROWW_ENABLED else '❌ Disabled'}")
        print(f"  SENSIBULL: {'✅ Enabled' if cls.SENSIBULL_ENABLED else '❌ Disabled'}")
        print()
        print("📈 Trading Indices:")
        for index, config in cls.INDEX_SYMBOLS.items():
            print(f"  {index}: Lot Size {config['lot_size']}, Max Qty {config['max_quantity']}")
        print()
        print("⚙️ Advanced Features:")
        print(f"  Intraday Margin: {cls.INTRADAY_MARGIN*100:.1f}%")
        print(f"  Square Off Time: {cls.SQUARE_OFF_TIME}")
        print(f"  Trailing Stop: {cls.TRAILING_STOP*100:.1f}%")
        print(f"  Alert Frequency: {cls.ALERTS['alert_frequency']} seconds")

# Export configuration
CONFIG = AdvancedTradingConfig()

if __name__ == "__main__":
    # Validate and print configuration
    if CONFIG.validate_config():
        print("✅ Configuration is valid!")
        CONFIG.print_config_summary()
    else:
        print("❌ Configuration has errors!")
