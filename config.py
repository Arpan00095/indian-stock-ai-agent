import os
from dotenv import load_dotenv

try:
    load_dotenv()
except Exception:
    # If .env file is corrupted or missing, continue without it
    pass

class Config:
    # API Keys
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Trading Parameters
    DEFAULT_CAPITAL = 100000  # Default capital in INR
    MAX_RISK_PER_TRADE = 0.02  # 2% risk per trade
    DEFAULT_STOP_LOSS_PERCENTAGE = 0.05  # 5% stop loss
    DEFAULT_TAKE_PROFIT_PERCENTAGE = 0.15  # 15% take profit
    
    # Technical Analysis Parameters
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    MA_SHORT = 20
    MA_LONG = 50
    VOLUME_MA_PERIOD = 20
    
    # OI Analysis Parameters
    MIN_OI_THRESHOLD = 1000
    PCR_THRESHOLD_HIGH = 1.5
    PCR_THRESHOLD_LOW = 0.5
    
    # Support/Resistance Parameters
    PIVOT_LOOKBACK = 20
    MIN_TOUCHES = 2
    PRICE_TOLERANCE = 0.02  # 2% tolerance for level identification
    
    # Alert Settings
    ALERT_CHECK_INTERVAL = 60  # seconds
    BREAKOUT_CONFIRMATION_CANDLES = 2
    
    # Major Indian Indices and Stocks
    MAJOR_INDICES = {
        'NIFTY50': '^NSEI',
        'BANKNIFTY': '^NSEBANK',
        'SENSEX': '^BSESN',
        'FINNIFTY': 'NIFTY_FIN_SERVICE.NS'
    }
    
    POPULAR_STOCKS = {
        # Banking & Financial Services
        'HDFC BANK': 'HDFCBANK.NS',
        'ICICI BANK': 'ICICIBANK.NS',
        'AXIS BANK': 'AXISBANK.NS',
        'KOTAK BANK': 'KOTAKBANK.NS',
        'SBI': 'SBIN.NS',
        'INDUSIND BANK': 'INDUSINDBK.NS',
        'BANDHAN BANK': 'BANDHANBNK.NS',
        'FEDERAL BANK': 'FEDERALBNK.NS',
        'IDFC FIRST BANK': 'IDFCFIRSTB.NS',
        'AU SMALL FINANCE': 'AUBANK.NS',
        
        # IT & Technology
        'TCS': 'TCS.NS',
        'INFOSYS': 'INFY.NS',
        'WIPRO': 'WIPRO.NS',
        'HCL TECH': 'HCLTECH.NS',
        'TECH MAHINDRA': 'TECHM.NS',
        'L&T INFOTECH': 'LTI.NS',
        'MINDTREE': 'MINDTREE.NS',
        'MPHASIS': 'MPHASIS.NS',
        'PERSISTENT': 'PERSISTENT.NS',
        'COFORGE': 'COFORGE.NS',
        
        # Oil & Gas
        'RELIANCE': 'RELIANCE.NS',
        'ONGC': 'ONGC.NS',
        'IOC': 'IOC.NS',
        'BPCL': 'BPCL.NS',
        'HPCL': 'HPCL.NS',
        'GAIL': 'GAIL.NS',
        'PETRONET LNG': 'PETRONET.NS',
        'ADANI PORTS': 'ADANIPORTS.NS',
        'ADANI GREEN': 'ADANIGREEN.NS',
        'ADANI TRANSMISSION': 'ADANITRANS.NS',
        
        # FMCG & Consumer
        'HINDUNILVR': 'HINDUNILVR.NS',
        'ITC': 'ITC.NS',
        'NESTLE': 'NESTLEIND.NS',
        'DABUR': 'DABUR.NS',
        'GODREJ CP': 'GODREJCP.NS',
        'MARICO': 'MARICO.NS',
        'BRITANNIA': 'BRITANNIA.NS',
        'TITAN': 'TITAN.NS',
        'TATA CONSUMER': 'TATACONSUM.NS',
        'UBL': 'UBL.NS',
        
        # Auto & Auto Ancillaries
        'MARUTI': 'MARUTI.NS',
        'TATA MOTORS': 'TATAMOTORS.NS',
        'MAHINDRA': 'M&M.NS',
        'BAJAJ AUTO': 'BAJAJ-AUTO.NS',
        'HERO MOTOCORP': 'HEROMOTOCO.NS',
        'EICHER MOTORS': 'EICHERMOT.NS',
        'ASHOK LEYLAND': 'ASHOKLEY.NS',
        'BOSCH': 'BOSCHLTD.NS',
        'EXIDE': 'EXIDEIND.NS',
        'APOLLO TYRES': 'APOLLOTYRE.NS',
        
        # Pharmaceuticals
        'SUN PHARMA': 'SUNPHARMA.NS',
        'DR. REDDYS': 'DRREDDY.NS',
        'CIPLA': 'CIPLA.NS',
        'DIVIS LAB': 'DIVISLAB.NS',
        'BIOCON': 'BIOCON.NS',
        'LUPIN': 'LUPIN.NS',
        'AUROBINDO PHARMA': 'AUROPHARMA.NS',
        'CADILA HEALTH': 'ZYDUSLIFE.NS',
        'TORRENT PHARMA': 'TORNTPHARM.NS',
        'GLENMARK': 'GLENMARK.NS',
        
        # Telecom
        'BHARTI AIRTEL': 'BHARTIARTL.NS',
        'JIO': 'RJIO.NS',
        'VODAFONE IDEA': 'IDEA.NS',
        
        # Power & Utilities
        'NTPC': 'NTPC.NS',
        'POWERGRID': 'POWERGRID.NS',
        'TATA POWER': 'TATAPOWER.NS',
        'ADANI POWER': 'ADANIPOWER.NS',
        'TORRENT POWER': 'TORNTPOWER.NS',
        'CESC': 'CESC.NS',
        'TATA CONSULTANCY': 'TCS.NS',
        
        # Metals & Mining
        'TATA STEEL': 'TATASTEEL.NS',
        'JSW STEEL': 'JSWSTEEL.NS',
        'SAIL': 'SAIL.NS',
        'HINDALCO': 'HINDALCO.NS',
        'VEDANTA': 'VEDL.NS',
        'COAL INDIA': 'COALINDIA.NS',
        'NMDC': 'NMDC.NS',
        'JINDAL STEEL': 'JINDALSTEL.NS',
        
        # Cement
        'ULTRATECH CEMENT': 'ULTRACEMCO.NS',
        'SHREE CEMENT': 'SHREECEM.NS',
        'GRASIM': 'GRASIM.NS',
        'AMBUJA CEMENT': 'AMBUJACEM.NS',
        'ACC': 'ACC.NS',
        'RAMCO CEMENT': 'RAMCOCEM.NS',
        
        # Real Estate
        'DLF': 'DLF.NS',
        'GODREJ PROPERTIES': 'GODREJPROP.NS',
        'BRIGADE': 'BRIGADE.NS',
        'SOBHA': 'SOBHA.NS',
        'MAHINDRA LIFESPACE': 'MAHLIFE.NS',
        
        # Media & Entertainment
        'ZEE ENTERTAINMENT': 'ZEEL.NS',
        'SUN TV': 'SUNTV.NS',
        'NETWORK18': 'NETWORK18.NS',
        'PVR': 'PVR.NS',
        'INOX LEISURE': 'INOXLEISUR.NS',
        
        # Aviation
        'INDIGO': 'INDIGO.NS',
        'SPICEJET': 'SPICEJET.NS',
        
        # E-commerce & Retail
        'FLIPKART': 'FLIPKART.NS',
        'NYKAA': 'NYKAA.NS',
        'ZOMATO': 'ZOMATO.NS',
        'PAYTM': 'PAYTM.NS',
        'POLICYBAZAAR': 'PBAL.NS',
        
        # Insurance
        'LIFE INSURANCE': 'LICI.NS',
        'SBI LIFE': 'SBILIFE.NS',
        'HDFC LIFE': 'HDFCLIFE.NS',
        'ICICI PRUDENTIAL': 'ICICIPRULI.NS',
        'BAJAJ FINSERV': 'BAJFINANCE.NS',
        
        # NBFC
        'BAJAJ FINANCE': 'BAJFINANCE.NS',
        'CHOLAMANDALAM': 'CHOLAFIN.NS',
        'M&M FINANCIAL': 'M&MFIN.NS',
        'L&T FINANCE': 'LTFH.NS',
        'POWER FINANCE': 'PFC.NS',
        
        # Infrastructure
        'L&T': 'LT.NS',
        'ADANI PORTS': 'ADANIPORTS.NS',
        'CONTAINER CORP': 'CONCOR.NS',
        'IRCTC': 'IRCTC.NS',
        'RVNL': 'RVNL.NS',
        
        # Textiles
        'WELSPUN': 'WELSPUNIND.NS',
        'ARVIND': 'ARVIND.NS',
        'TRIDENT': 'TRIDENT.NS',
        'RAYMOND': 'RAYMOND.NS',
        
        # Chemicals
        'UPL': 'UPL.NS',
        'RALLIS': 'RALLIS.NS',
        'DEEPAK NITRITE': 'DEEPAKNTR.NS',
        'AARTI INDUSTRIES': 'AARTIIND.NS',
        'BALRAM CHINI': 'BALRAMCHIN.NS',
        
        # Agriculture
        'RALLIS': 'RALLIS.NS',
        'UPL': 'UPL.NS',
        'DEEPAK FERTILIZERS': 'DEEPAKFERT.NS',
        'CHAMBAL FERTILIZERS': 'CHAMBLFERT.NS',
        
        # Small & Mid Cap Gems
        'POLYCAB': 'POLYCAB.NS',
        'ASTRAL': 'ASTRAL.NS',
        'CROMPTON': 'CROMPTON.NS',
        'HAVELLS': 'HAVELLS.NS',
        'VOLTAS': 'VOLTAS.NS',
        'BLUE DART': 'BLUEDART.NS',
        'DELTA CORP': 'DELTACORP.NS',
        'JUBILANT FOOD': 'JUBLFOOD.NS',
        'PAGE INDUSTRIES': 'PAGEIND.NS',
        'RELAXO': 'RELAXO.NS'
    }
    
    # Market Hours (IST)
    MARKET_OPEN = "09:15"
    MARKET_CLOSE = "15:30"
    PRE_MARKET_OPEN = "09:00"
    POST_MARKET_CLOSE = "15:45"
    
    # Database Settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///stock_agent.db')
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'stock_agent.log'
