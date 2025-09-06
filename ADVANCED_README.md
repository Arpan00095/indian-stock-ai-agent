# 🚀 Advanced Intraday Trading System

**Professional-grade automated trading system for Indian indices with DHAN, GROWW, and SENSIBULL broker integrations**

## 🎯 Features

### 🔥 **Advanced Trading Engine**
- **Multi-Strategy Trading**: Momentum, Mean Reversion, Breakout, OI Analysis
- **Real-time Market Data**: Live streaming from multiple sources
- **Risk Management**: Advanced position sizing and portfolio management
- **Auto SL/TP**: Automatic stop-loss and take-profit execution
- **Trailing Stops**: Dynamic stop-loss adjustment

### 🏢 **Broker Integrations**
- **DHAN**: Full API integration with authentication
- **GROWW**: Complete order management and portfolio tracking
- **SENSIBULL**: Advanced options trading capabilities
- **Multi-Broker Support**: Execute trades across multiple brokers simultaneously

### 📊 **Technical Analysis**
- **Advanced Indicators**: RSI, MACD, Bollinger Bands, EMAs
- **OI Analysis**: Put-Call Ratio, Max Pain, Gamma Exposure
- **Volume Analysis**: Volume profile and breakout confirmation
- **Pattern Recognition**: Support/Resistance, Breakout/Breakdown detection

### 🔔 **Alert System**
- **TradingView Integration**: Webhook-based alert processing
- **Multi-Channel Notifications**: SMS, Email, Telegram, Push
- **Custom Alerts**: Breakout, PCR, Volume, Technical signals
- **Real-time Monitoring**: 24/7 market surveillance

### 🛡️ **Risk Management**
- **Position Sizing**: Dynamic based on capital and risk
- **Portfolio Limits**: Maximum exposure and position limits
- **Daily Loss Limits**: Automatic trading halt on losses
- **Correlation Analysis**: Diversification across indices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TradingView   │    │   Market Data   │    │   Web Interface  │
│     Alerts      │    │     Sources     │    │   (Streamlit)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Advanced Trading Engine │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Signal Processor  │  │
                    │  └─────────────────────┘  │
                    │  ┌─────────────────────┐  │
                    │  │   Risk Manager      │  │
                    │  └─────────────────────┘  │
                    │  ┌─────────────────────┐  │
                    │  │   Strategy Manager  │  │
                    │  └─────────────────────┘  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     Broker Layer          │
                    │                           │
                    │  ┌─────┐  ┌─────┐  ┌─────┐│
                    │  │DHAN │  │GROWW│  │SENSI││
                    │  └─────┘  └─────┘  └─────┘│
                    └───────────────────────────┘
```

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone the repository
git clone <repository-url>
cd advanced-trading-system

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp advanced_env_example.txt .env

# Edit configuration
nano .env
```

### 2. **Configuration**

Edit `.env` file with your broker credentials:

```bash
# DHAN Configuration
DHAN_ENABLED=true
DHAN_API_KEY=your_dhan_api_key
DHAN_API_SECRET=your_dhan_api_secret
DHAN_USER_ID=your_user_id
DHAN_PASSWORD=your_password
DHAN_TOTP_KEY=your_totp_key

# GROWW Configuration
GROWW_ENABLED=true
GROWW_API_KEY=your_groww_api_key
GROWW_API_SECRET=your_groww_api_secret

# SENSIBULL Configuration
SENSIBULL_ENABLED=true
SENSIBULL_API_KEY=your_sensibull_api_key
SENSIBULL_API_SECRET=your_sensibull_api_secret

# Trading Parameters
TRADING_CAPITAL=100000
MAX_RISK_PER_TRADE=0.02
MAX_DAILY_LOSS=0.05
```

### 3. **Run the System**

```bash
# Start advanced trading engine
python advanced_trading_engine.py

# Start TradingView alert handler
python tradingview_alerts.py

# Start web interface
python main.py --web
```

## 📊 Trading Strategies

### 1. **Momentum Strategy**
- **Entry**: Strong price momentum (>0.5% move)
- **Exit**: Momentum reversal or target hit
- **Risk**: 2% stop loss, 4% take profit

### 2. **Mean Reversion Strategy**
- **Entry**: Price near daily high/low (80% range)
- **Exit**: Return to mean or stop loss
- **Risk**: 1% stop loss, 1% take profit

### 3. **Breakout Strategy**
- **Entry**: Price breaking above resistance
- **Exit**: False breakout or target hit
- **Risk**: 2% stop loss, 4% take profit

### 4. **OI Analysis Strategy**
- **Entry**: High volume + price movement
- **Exit**: OI unwinding or target hit
- **Risk**: 2% stop loss, 4% take profit

## 🔗 TradingView Integration

### 1. **Webhook Setup**

```javascript
// TradingView Alert Message
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
```

### 2. **Pine Script Example**

```pinescript
//@version=5
strategy("Advanced Intraday Trading", overlay=true)

// RSI Strategy
rsi = ta.rsi(close, 14)
long_condition = rsi < 30 and close > close[1]
short_condition = rsi > 70 and close < close[1]

if long_condition
    strategy.entry("Long", strategy.long)
    alert("BUY Signal", alert.freq_once_per_bar)

if short_condition
    strategy.entry("Short", strategy.short)
    alert("SELL Signal", alert.freq_once_per_bar)
```

## 🏢 Broker Setup

### **DHAN Broker**

1. **API Access**: Contact DHAN for API credentials
2. **Authentication**: Use API key, secret, and TOTP
3. **Permissions**: Enable trading permissions
4. **Testing**: Test with paper trading first

### **GROWW Broker**

1. **Developer Account**: Register as developer
2. **API Keys**: Generate API key and secret
3. **Webhook Setup**: Configure webhook endpoints
4. **Permissions**: Enable trading access

### **SENSIBULL Broker**

1. **Partner Account**: Register as trading partner
2. **API Integration**: Get API credentials
3. **Options Trading**: Enable options permissions
4. **Testing**: Use demo environment first

## 📈 Index Trading

### **Supported Indices**

| Index | Symbol | Lot Size | Tick Size | Max Quantity |
|-------|--------|----------|-----------|--------------|
| NIFTY50 | ^NSEI | 50 | 0.05 | 1000 |
| BANKNIFTY | ^NSEBANK | 25 | 0.05 | 500 |
| FINNIFTY | NIFTY_FIN_SERVICE.NS | 40 | 0.05 | 800 |
| MIDCPNIFTY | NIFTY_MIDCAP_100.NS | 75 | 0.05 | 600 |

### **Trading Parameters**

- **Margin Required**: 20% for intraday
- **Square Off Time**: 3:15 PM
- **Order Types**: Market, Limit, SL, SL-M
- **Product Type**: Intraday

## 🛡️ Risk Management

### **Position Sizing**

```python
# Dynamic position sizing based on risk
risk_amount = capital * max_risk_per_trade
position_size = risk_amount / (entry_price - stop_loss)
```

### **Portfolio Limits**

- **Max Positions**: 5 concurrent positions
- **Max Exposure**: ₹100,000 total exposure
- **Daily Loss Limit**: 5% of capital
- **Correlation Limit**: Max 2 positions in same direction

### **Stop Loss Management**

- **Fixed SL**: 2% from entry price
- **Trailing SL**: 1% trailing stop
- **Time-based SL**: Square off at 3:15 PM
- **Volatility SL**: Adjust based on ATR

## 📊 Performance Monitoring

### **Key Metrics**

- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / Gross loss
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Maximum portfolio decline
- **Daily P&L**: Daily profit/loss tracking

### **Reporting**

```bash
# Get portfolio summary
curl http://localhost:5000/status

# Get trading history
python -c "from advanced_trading_engine import *; print(get_trading_history())"

# Export performance report
python generate_report.py
```

## 🔧 Configuration Options

### **Trading Parameters**

```python
# Risk Management
MAX_RISK_PER_TRADE = 0.02      # 2% risk per trade
MAX_DAILY_LOSS = 0.05          # 5% daily loss limit
MAX_POSITIONS = 5              # Max concurrent positions
MAX_EXPOSURE = 100000          # Max portfolio exposure

# Strategy Parameters
MOMENTUM_THRESHOLD = 0.5       # 0.5% momentum threshold
MEAN_REVERSION_THRESHOLD = 0.8 # 80% range threshold
BREAKOUT_CONFIRMATION = 3      # 3 candle confirmation
VOLUME_THRESHOLD = 1000000     # Volume threshold

# Stop Loss & Take Profit
DEFAULT_STOP_LOSS = 0.02       # 2% stop loss
DEFAULT_TAKE_PROFIT = 0.04     # 4% take profit
TRAILING_STOP = 0.01           # 1% trailing stop
```

### **Technical Indicators**

```python
# RSI Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD Settings
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# EMAs
EMA_SHORT = 9
EMA_LONG = 21
```

## 🚨 Alert System

### **Alert Types**

1. **Breakout Alerts**: Price breaking support/resistance
2. **PCR Alerts**: Put-Call ratio extremes
3. **Volume Alerts**: Unusual volume spikes
4. **Technical Alerts**: RSI, MACD signals
5. **Risk Alerts**: Portfolio limits reached

### **Notification Channels**

- **SMS**: Via Twilio
- **Email**: SMTP configuration
- **Telegram**: Bot notifications
- **Push**: In-app notifications

### **Alert Configuration**

```python
# Alert Settings
ENABLE_SMS = false
ENABLE_EMAIL = false
ENABLE_TELEGRAM = false
ENABLE_PUSH = true
ALERT_FREQUENCY = 30  # seconds
```

## 🔍 Troubleshooting

### **Common Issues**

1. **API Connection Failed**
   - Check API credentials
   - Verify network connectivity
   - Test with broker's test environment

2. **Orders Not Executing**
   - Check account balance
   - Verify trading permissions
   - Check market hours

3. **Webhook Not Receiving Alerts**
   - Verify webhook URL
   - Check firewall settings
   - Test webhook endpoint

4. **High Latency**
   - Optimize market data frequency
   - Use local server deployment
   - Check internet connection

### **Debug Mode**

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python advanced_trading_engine.py --debug

# Check logs
tail -f trading_engine.log
```

## 📚 API Reference

### **Trading Engine API**

```python
# Initialize engine
engine = AdvancedTradingEngine(config)

# Start trading
await engine.start_trading()

# Get portfolio
portfolio = engine.get_portfolio_summary()

# Place manual order
signal = TradingSignal(
    symbol="NIFTY50",
    side=OrderSide.BUY,
    quantity=100,
    price=19000,
    stop_loss=18620,
    take_profit=19380
)
engine.signal_queue.put(signal)
```

### **Webhook API**

```bash
# TradingView webhook
POST /webhook/tradingview
{
    "symbol": "NIFTY50",
    "action": "BUY",
    "price": 19000,
    "quantity": 100
}

# Custom webhook
POST /webhook/custom
{
    "symbol": "BANKNIFTY",
    "action": "SELL",
    "price": 44000,
    "quantity": 25
}

# Status check
GET /status

# Health check
GET /health
```

## 🔒 Security

### **Best Practices**

1. **API Security**
   - Use strong API keys
   - Enable 2FA on all accounts
   - Rotate keys regularly
   - Use IP whitelisting

2. **Data Security**
   - Encrypt sensitive data
   - Use secure connections
   - Regular backups
   - Access logging

3. **Trading Security**
   - Start with paper trading
   - Use small capital initially
   - Monitor all trades
   - Set strict limits

## 📞 Support

### **Documentation**
- [API Documentation](docs/api.md)
- [Strategy Guide](docs/strategies.md)
- [Broker Setup](docs/brokers.md)
- [Troubleshooting](docs/troubleshooting.md)

### **Community**
- [Discord Server](https://discord.gg/trading)
- [Telegram Group](https://t.me/tradingcommunity)
- [GitHub Issues](https://github.com/your-repo/issues)

### **Professional Support**
- Email: support@trading-system.com
- Phone: +91-XXXXXXXXXX
- Hours: 9:00 AM - 6:00 PM IST

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always test thoroughly before using with real money.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🚀 Ready to start advanced intraday trading? Follow the setup guide and begin with paper trading!**
