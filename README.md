# 🇮🇳 Indian Stock Market AI Agent

Advanced AI-powered trading agent for Indian stock markets with comprehensive OI (Open Interest) analysis, PCR (Put-Call Ratio) calculator, breakout/breakdown alerts, and automated trading signals.

## 🚀 Features

### 📊 **OI Analysis & PCR Calculator**
- Real-time Put-Call Ratio calculation
- OI buildup pattern detection
- Max pain analysis
- Gamma exposure estimation
- Volatility skew analysis
- Options unwinding signals

### 🚨 **Breakout/Breakdown Alerts**
- Automated support/resistance level detection
- Real-time breakout/breakdown monitoring
- Multi-candle confirmation
- Customizable alert thresholds
- Entry, Stop Loss, and Take Profit calculations

### 📈 **Trading Signals**
- AI-generated buy/sell signals
- Risk-reward ratio optimization
- Position sizing recommendations
- Confidence scoring
- Multiple timeframe analysis

### 📋 **Master Cheatsheet**
- Complete OI trading rules
- PCR interpretation guide
- Risk management guidelines
- Quick reference cards

### 🌐 **Multiple Interfaces**
- Beautiful Streamlit web interface
- Command-line interface (CLI)
- Real-time monitoring dashboard
- Mobile-responsive design

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Stock-Agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (optional)**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
ALPHA_VANTAGE_API_KEY=your_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TELEGRAM_BOT_TOKEN=your_telegram_token
```

## 🎯 Usage

### Web Interface (Recommended)
```bash
python main.py --web
```
This opens a beautiful web interface at `http://localhost:8501`

### Command Line Interface
```bash
python main.py --cli
```

### Quick Analysis
```bash
python main.py --analyze NIFTY50
python main.py --analyze RELIANCE.NS
```

### Start Alert Monitoring
```bash
python main.py --alerts
```

## 📊 How to Use the AI Agent

### 1. **Market Overview**
- View live prices of major Indian indices (NIFTY50, BANKNIFTY, SENSEX)
- Monitor popular stocks (RELIANCE, TCS, HDFC, etc.)
- Real-time price charts and technical indicators

### 2. **OI Analysis**
- Enter any stock/index symbol
- Get comprehensive PCR analysis
- View OI patterns and buildup detection
- Analyze support/resistance levels
- Generate trading signals

### 3. **Setting Up Alerts**
- Choose symbol for monitoring
- Set breakout/breakdown alert levels
- Configure PCR threshold alerts
- Receive real-time notifications

### 4. **Master Cheatsheet**
- Complete OI trading rules
- PCR interpretation guide
- Risk management guidelines
- Quick reference for trading decisions

## 📈 OI Trading Strategy

### PCR Interpretation
- **PCR > 1.5**: Extreme fear - Buy calls
- **PCR 1.2-1.5**: Fear - Consider calls on dips
- **PCR 0.8-1.2**: Neutral - Follow technicals
- **PCR 0.5-0.8**: Greed - Consider puts
- **PCR < 0.5**: Extreme greed - Buy puts

### Breakout Trading Rules
- **Entry**: At breakout level
- **Stop Loss**: 2% below breakout (calls) / 2% above (puts)
- **Take Profit**: 2:1 risk-reward ratio
- **Confirmation**: Multiple candles above/below level

### Risk Management
- **Position Sizing**: 2% risk per trade
- **Max Positions**: 3 concurrent trades
- **Stop Loss**: 5% from entry
- **Take Profit**: 15% from entry

## 🔧 Configuration

### Trading Parameters
- Default capital: ₹100,000
- Risk per trade: 2%
- Stop loss: 5%
- Take profit: 15%

### Technical Analysis
- RSI period: 14
- Moving averages: 20 & 50
- Volume MA: 20
- Support/Resistance tolerance: 2%

### Alert Settings
- Check interval: 30 seconds
- Breakout confirmation: 2 candles
- PCR threshold: 1.5

## 📱 Supported Symbols

### Major Indices
- NIFTY50 (^NSEI)
- BANKNIFTY (^NSEBANK)
- SENSEX (^BSESN)
- FINNIFTY (NIFTY_FIN_SERVICE.NS)

### Popular Stocks
- RELIANCE.NS
- TCS.NS
- HDFC.NS
- INFY.NS
- ICICIBANK.NS
- HINDUNILVR.NS
- ITC.NS
- SBIN.NS
- BHARTIARTL.NS
- AXISBANK.NS

## 🚨 Alert Types

### 1. **Breakout Alerts**
- Price breaks above resistance
- Price breaks below support
- Multi-candle confirmation
- Automatic TP/SL calculation

### 2. **PCR Alerts**
- PCR crosses threshold
- Extreme fear/greed detection
- Options unwinding signals

### 3. **Volume Alerts**
- Unusual volume spikes
- Volume confirmation for breakouts
- Low volume warnings

## 📊 Sample Output

### OI Analysis Result
```
🔍 OI Analysis for NIFTY50

📊 PCR Analysis:
  Signal: EXTREME_FEAR
  Confidence: HIGH
  Action: Consider buying calls or covering shorts

📈 OI Patterns:
  Pattern: PUT_BUILDUP
  Interpretation: Heavy put writing/buying. Potential reversal signal.
  Risk Level: HIGH
  Timeframe: SHORT_TERM

🎯 Trading Signals:
  1. BUY_CALL: Extreme fear in market, potential reversal
  2. BUY_CALL: Heavy put buildup, potential short squeeze
```

### Breakout Alert
```
🚀 BREAKOUT ALERT - NIFTY50

📈 Action: BUY_CALL
💰 Entry: ₹19,850.00
🛑 Stop Loss: ₹19,452.00
🎯 Take Profit: ₹20,248.00

Risk: ₹398.00
Reward: ₹398.00
Risk-Reward: 1.0:1

⏰ Time: 14:30:25
```

## 🔒 Risk Disclaimer

⚠️ **IMPORTANT**: This software is for educational and research purposes only. 

- Past performance does not guarantee future results
- Always do your own research before trading
- Never invest more than you can afford to lose
- Consider consulting with a financial advisor
- The authors are not responsible for any trading losses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the cheatsheet

## 🔄 Updates

### Version 1.0.0
- Initial release
- OI analysis and PCR calculator
- Breakout/breakdown alerts
- Web and CLI interfaces
- Master cheatsheet

---

**Happy Trading! 📈💰**
