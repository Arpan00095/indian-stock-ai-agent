#!/usr/bin/env python3
"""
Advanced Intraday Trading System - Quick Start Demo
Demonstrates the advanced features and broker integrations
"""

import asyncio
import time
from datetime import datetime
import json

# Import our advanced components
from advanced_trading_engine import AdvancedTradingEngine, TradingSignal, OrderSide, OrderType, BrokerType
from advanced_config import CONFIG

def print_banner():
    """Print system banner"""
    print("=" * 80)
    print("🚀 ADVANCED INTRADAY TRADING SYSTEM")
    print("   Professional Trading Engine with Multi-Broker Support")
    print("=" * 80)
    print()

def demo_configuration():
    """Demonstrate configuration validation"""
    print("🔧 Configuration Validation")
    print("-" * 40)
    
    if CONFIG.validate_config():
        print("✅ Configuration is valid!")
        CONFIG.print_config_summary()
    else:
        print("❌ Configuration has errors!")
        print("Please check your .env file")
    
    print()

def demo_broker_connections():
    """Demonstrate broker connections"""
    print("🏢 Broker Connection Test")
    print("-" * 40)
    
    brokers = {
        'DHAN': CONFIG.DHAN_ENABLED,
        'GROWW': CONFIG.GROWW_ENABLED,
        'SENSIBULL': CONFIG.SENSIBULL_ENABLED
    }
    
    for broker, enabled in brokers.items():
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"  {broker}: {status}")
    
    print()

def demo_trading_strategies():
    """Demonstrate trading strategies"""
    print("📊 Trading Strategies")
    print("-" * 40)
    
    strategies = [
        {
            'name': 'Momentum Strategy',
            'description': 'Trade with strong price momentum',
            'entry': 'Price momentum > 0.5%',
            'exit': 'Momentum reversal or target hit',
            'risk': '2% SL, 4% TP'
        },
        {
            'name': 'Mean Reversion Strategy',
            'description': 'Trade price reversals from extremes',
            'entry': 'Price near daily high/low (80% range)',
            'exit': 'Return to mean or stop loss',
            'risk': '1% SL, 1% TP'
        },
        {
            'name': 'Breakout Strategy',
            'description': 'Trade breakouts from resistance/support',
            'entry': 'Price breaking above resistance',
            'exit': 'False breakout or target hit',
            'risk': '2% SL, 4% TP'
        },
        {
            'name': 'OI Analysis Strategy',
            'description': 'Trade based on options flow',
            'entry': 'High volume + price movement',
            'exit': 'OI unwinding or target hit',
            'risk': '2% SL, 4% TP'
        }
    ]
    
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy['name']}")
        print(f"   Description: {strategy['description']}")
        print(f"   Entry: {strategy['entry']}")
        print(f"   Exit: {strategy['exit']}")
        print(f"   Risk: {strategy['risk']}")
        print()
    
    print()

def demo_index_trading():
    """Demonstrate index trading capabilities"""
    print("📈 Index Trading Capabilities")
    print("-" * 40)
    
    print("Supported Indices:")
    for index, config in CONFIG.INDEX_SYMBOLS.items():
        print(f"  {index}:")
        print(f"    Symbol: {config['symbol']}")
        print(f"    Lot Size: {config['lot_size']}")
        print(f"    Tick Size: {config['tick_size']}")
        print(f"    Max Quantity: {config['max_quantity']}")
        print(f"    Margin Required: {config['margin_required']*100:.1f}%")
        print()
    
    print()

def demo_risk_management():
    """Demonstrate risk management features"""
    print("🛡️ Risk Management Features")
    print("-" * 40)
    
    risk_features = [
        f"Capital: ₹{CONFIG.CAPITAL:,.2f}",
        f"Max Risk per Trade: {CONFIG.MAX_RISK_PER_TRADE*100:.1f}%",
        f"Max Daily Loss: {CONFIG.MAX_DAILY_LOSS*100:.1f}%",
        f"Max Positions: {CONFIG.MAX_POSITIONS}",
        f"Max Exposure: ₹{CONFIG.MAX_EXPOSURE:,.2f}",
        f"Default Stop Loss: {CONFIG.DEFAULT_STOP_LOSS_PERCENTAGE*100:.1f}%",
        f"Default Take Profit: {CONFIG.DEFAULT_TAKE_PROFIT_PERCENTAGE*100:.1f}%",
        f"Trailing Stop: {CONFIG.TRAILING_STOP*100:.1f}%",
        f"Square Off Time: {CONFIG.SQUARE_OFF_TIME}"
    ]
    
    for feature in risk_features:
        print(f"  {feature}")
    
    print()

def demo_alert_system():
    """Demonstrate alert system capabilities"""
    print("🔔 Alert System Capabilities")
    print("-" * 40)
    
    alert_types = [
        "Breakout Alerts - Price breaking support/resistance",
        "PCR Alerts - Put-Call ratio extremes",
        "Volume Alerts - Unusual volume spikes",
        "Technical Alerts - RSI, MACD signals",
        "Risk Alerts - Portfolio limits reached"
    ]
    
    notification_channels = [
        f"SMS: {'✅ Enabled' if CONFIG.ALERTS['enable_sms'] else '❌ Disabled'}",
        f"Email: {'✅ Enabled' if CONFIG.ALERTS['enable_email'] else '❌ Disabled'}",
        f"Telegram: {'✅ Enabled' if CONFIG.ALERTS['enable_telegram'] else '❌ Disabled'}",
        f"Push: {'✅ Enabled' if CONFIG.ALERTS['enable_push'] else '❌ Disabled'}"
    ]
    
    print("Alert Types:")
    for alert_type in alert_types:
        print(f"  • {alert_type}")
    
    print("\nNotification Channels:")
    for channel in notification_channels:
        print(f"  {channel}")
    
    print(f"\nAlert Frequency: {CONFIG.ALERTS['alert_frequency']} seconds")
    print()

def demo_tradingview_integration():
    """Demonstrate TradingView integration"""
    print("📊 TradingView Integration")
    print("-" * 40)
    
    print("Webhook Endpoints:")
    print("  • /webhook/tradingview - TradingView alerts")
    print("  • /webhook/custom - Custom alerts")
    print("  • /status - Trading engine status")
    print("  • /health - Health check")
    
    print("\nExample TradingView Alert:")
    example_alert = {
        "symbol": "NIFTY50",
        "action": "BUY",
        "price": 19000,
        "quantity": 100,
        "stop_loss": 18620,
        "take_profit": 19380,
        "strategy": "Momentum",
        "confidence": 0.8,
        "broker": "dhan"
    }
    print(json.dumps(example_alert, indent=2))
    print()

def demo_technical_indicators():
    """Demonstrate technical indicators"""
    print("📈 Technical Indicators")
    print("-" * 40)
    
    indicators = CONFIG.TECHNICAL_INDICATORS
    
    print("RSI Settings:")
    print(f"  Period: {indicators['rsi_period']}")
    print(f"  Overbought: {indicators['rsi_overbought']}")
    print(f"  Oversold: {indicators['rsi_oversold']}")
    
    print("\nMACD Settings:")
    print(f"  Fast: {indicators['macd_fast']}")
    print(f"  Slow: {indicators['macd_slow']}")
    print(f"  Signal: {indicators['macd_signal']}")
    
    print("\nBollinger Bands:")
    print(f"  Period: {indicators['bollinger_period']}")
    print(f"  Standard Deviation: {indicators['bollinger_std']}")
    
    print("\nEMAs:")
    print(f"  Short: {indicators['ema_short']}")
    print(f"  Long: {indicators['ema_long']}")
    print()

def demo_oi_analysis():
    """Demonstrate OI analysis capabilities"""
    print("📊 OI Analysis Capabilities")
    print("-" * 40)
    
    oi_config = CONFIG.OI_ANALYSIS
    
    print("PCR Thresholds:")
    print(f"  High (Extreme Fear): {oi_config['pcr_threshold_high']}")
    print(f"  Low (Extreme Greed): {oi_config['pcr_threshold_low']}")
    
    print("\nOI Analysis Features:")
    print(f"  OI Buildup Threshold: {oi_config['oi_buildup_threshold']}")
    print(f"  Max Pain Calculation: {'✅ Enabled' if oi_config['max_pain_calculation'] else '❌ Disabled'}")
    print(f"  Gamma Exposure Threshold: {oi_config['gamma_exposure_threshold']}")
    
    print("\nTrading Signals:")
    print("  • PCR > 1.5: Buy calls (extreme fear)")
    print("  • PCR < 0.5: Buy puts (extreme greed)")
    print("  • PCR 0.8-1.2: Neutral, follow technicals")
    print()

def demo_performance_monitoring():
    """Demonstrate performance monitoring"""
    print("📊 Performance Monitoring")
    print("-" * 40)
    
    metrics = [
        "Win Rate - Percentage of profitable trades",
        "Profit Factor - Gross profit / Gross loss",
        "Sharpe Ratio - Risk-adjusted returns",
        "Max Drawdown - Maximum portfolio decline",
        "Daily P&L - Daily profit/loss tracking",
        "Total Positions - Current open positions",
        "Total Exposure - Current portfolio exposure",
        "Daily Returns - Daily percentage returns"
    ]
    
    print("Key Metrics:")
    for metric in metrics:
        print(f"  • {metric}")
    
    print("\nReporting:")
    print("  • Real-time portfolio dashboard")
    print("  • Daily performance reports")
    print("  • Trade history export")
    print("  • Risk analysis reports")
    print()

def demo_usage_instructions():
    """Show usage instructions"""
    print("🚀 Usage Instructions")
    print("-" * 40)
    
    instructions = [
        "1. Configure your .env file with broker API keys",
        "2. Test broker connections with paper trading",
        "3. Start the advanced trading engine: python advanced_trading_engine.py",
        "4. Start TradingView alert handler: python tradingview_alerts.py",
        "5. Access web interface: python main.py --web",
        "6. Monitor performance at: http://localhost:5000/status",
        "7. Set up TradingView alerts with webhook URL",
        "8. Start with small capital and gradually increase"
    ]
    
    for instruction in instructions:
        print(f"  {instruction}")
    
    print("\n⚠️  Important Notes:")
    print("  • Always test with paper trading first")
    print("  • Monitor system logs regularly")
    print("  • Set appropriate risk limits")
    print("  • Keep API keys secure")
    print("  • Regular backup of trading data")
    print()

def main():
    """Main demo function"""
    print_banner()
    
    # Run all demos
    demo_configuration()
    demo_broker_connections()
    demo_trading_strategies()
    demo_index_trading()
    demo_risk_management()
    demo_alert_system()
    demo_tradingview_integration()
    demo_technical_indicators()
    demo_oi_analysis()
    demo_performance_monitoring()
    demo_usage_instructions()
    
    print("=" * 80)
    print("🎉 Advanced Intraday Trading System Demo Complete!")
    print("   Ready to start professional trading!")
    print("=" * 80)

if __name__ == "__main__":
    main()
