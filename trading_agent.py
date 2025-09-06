import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import threading
import time
import logging
from data_fetcher import IndianMarketDataFetcher
from oi_analyzer import OIAnalyzer
from alert_system import AlertSystem
from config import Config
from ai_chat_component import AIChatComponent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianStockTradingAgent:
    def __init__(self):
        self.config = Config()
        self.data_fetcher = IndianMarketDataFetcher()
        self.oi_analyzer = OIAnalyzer()
        self.alert_system = AlertSystem()
        self.ai_chat = AIChatComponent()
        self.monitoring_thread = None
        self.is_monitoring = False
        
    def run_streamlit_app(self):
        """Run the Streamlit web application"""
        st.set_page_config(
            page_title="Indian Stock Market AI Agent",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🇮🇳 Indian Stock Market AI Agent")
        st.markdown("### Advanced OI Analysis, PCR Calculator & Breakout Alerts")
        
        # Sidebar
        self._create_sidebar()
        
        # Main content
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Market Overview", 
            "🔍 OI Analysis", 
            "🚨 Alerts & Signals", 
            "📋 Master Cheatsheet",
            "🤖 AI Chat Assistant",
            "⚙️ Settings"
        ])
        
        with tab1:
            self._market_overview_tab()
        
        with tab2:
            self._oi_analysis_tab()
        
        with tab3:
            self._alerts_tab()
        
        with tab4:
            self._cheatsheet_tab()
        
        with tab5:
            self._ai_chat_tab()
        
        with tab6:
            self._settings_tab()
    
    def _create_sidebar(self):
        """Create the sidebar with symbol selection and controls"""
        st.sidebar.header("🎯 Trading Controls")
        
        # Symbol selection
        st.sidebar.subheader("Select Symbol")
        
        # Major indices
        st.sidebar.write("**Major Indices:**")
        selected_index = st.sidebar.selectbox(
            "Choose Index:",
            list(self.config.MAJOR_INDICES.keys()),
            key="index_select"
        )
        
        # Popular stocks
        st.sidebar.write("**Popular Stocks:**")
        selected_stock = st.sidebar.selectbox(
            "Choose Stock:",
            list(self.config.POPULAR_STOCKS.keys()),
            key="stock_select"
        )
        
        # Custom symbol
        custom_symbol = st.sidebar.text_input(
            "Custom Symbol (e.g., RELIANCE.NS):",
            placeholder="Enter symbol..."
        )
        
        # Determine active symbol
        if custom_symbol:
            active_symbol = custom_symbol
        elif st.sidebar.checkbox("Use Stock instead of Index"):
            active_symbol = self.config.POPULAR_STOCKS[selected_stock]
        else:
            active_symbol = self.config.MAJOR_INDICES[selected_index]
        
        if 'active_symbol' not in st.session_state:
            st.session_state['active_symbol'] = active_symbol
        else:
            st.session_state['active_symbol'] = active_symbol
        
        # Alert controls
        st.sidebar.subheader("🚨 Alert Controls")
        
        if st.sidebar.button("Start Monitoring", key="start_monitoring"):
            self._start_monitoring(active_symbol)
        
        if st.sidebar.button("Stop Monitoring", key="stop_monitoring"):
            self._stop_monitoring()
        
        # Quick actions
        st.sidebar.subheader("⚡ Quick Actions")
        
        if st.sidebar.button("Analyze Current Symbol"):
            st.session_state['analyze_symbol'] = active_symbol
        
        if st.sidebar.button("Setup Breakout Alerts"):
            st.session_state['setup_alerts'] = active_symbol
    
    def _market_overview_tab(self):
        """Market overview tab"""
        st.header("📊 Market Overview")
        
        # Get market overview
        overview = self.data_fetcher.get_market_overview()
        
        if overview:
            # Create metrics
            col1, col2, col3, col4 = st.columns(4)
            
            for i, (name, data) in enumerate(overview.items()):
                with [col1, col2, col3, col4][i]:
                    st.metric(
                        label=name,
                        value=f"₹{data['price']:,.2f}",
                        delta=f"{data['change_percent']:.2f}%"
                    )
            
            # Market overview table
            st.subheader("Detailed Market Data")
            
            overview_df = pd.DataFrame([
                {
                    'Index': name,
                    'Price': f"₹{data['price']:,.2f}",
                    'Change': f"₹{data['change']:,.2f}",
                    'Change %': f"{data['change_percent']:.2f}%",
                    'Volume': f"{data['volume']:,.0f}",
                    'High': f"₹{data['high']:,.2f}",
                    'Low': f"₹{data['low']:,.2f}"
                }
                for name, data in overview.items()
            ])
            
            st.dataframe(overview_df, width='stretch')
        
        # Active symbol analysis
        if 'active_symbol' in st.session_state:
            active_symbol = st.session_state['active_symbol']
            
            st.subheader(f"📈 {active_symbol} Analysis")
            
            # Get live data
            live_data = self.data_fetcher.get_live_price(active_symbol)
            if live_data:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Price", f"₹{live_data['price']:,.2f}")
                
                with col2:
                    st.metric("Change", f"₹{live_data['change']:,.2f}", f"{live_data['change_percent']:.2f}%")
                
                with col3:
                    st.metric("Volume", f"{live_data['volume']:,.0f}")
                
                with col4:
                    st.metric("Day Range", f"₹{live_data['low']:,.2f} - ₹{live_data['high']:,.2f}")
                
                # Price chart
                st.subheader("Price Chart")
                hist_data = self.data_fetcher.get_historical_data(active_symbol, period="1mo")
                
                if hist_data is not None:
                    fig = go.Figure(data=[go.Candlestick(
                        x=hist_data.index,
                        open=hist_data['Open'],
                        high=hist_data['High'],
                        low=hist_data['Low'],
                        close=hist_data['Close']
                    )])
                    
                    fig.update_layout(
                        title=f"{active_symbol} - 1 Month Chart",
                        xaxis_title="Date",
                        yaxis_title="Price (₹)",
                        height=500
                    )
                    
                    st.plotly_chart(fig, width='stretch')
    
    def _oi_analysis_tab(self):
        """OI Analysis tab"""
        st.header("🔍 OI Analysis & PCR Calculator")
        
        # Symbol input
        symbol = st.text_input(
            "Enter Symbol for OI Analysis:",
            value=st.session_state.get('active_symbol', '^NSEI'),
            key="oi_symbol"
        )
        
        if st.button("Analyze OI Data", key="analyze_oi"):
            with st.spinner("Analyzing OI data..."):
                analysis = self.oi_analyzer.analyze_oi_data(symbol)
                
                if analysis:
                    st.session_state['oi_analysis'] = analysis
                    st.success("Analysis completed!")
        
        # Display analysis results
        if 'oi_analysis' in st.session_state:
            analysis = st.session_state['oi_analysis']
            
            # PCR Analysis
            st.subheader("📊 PCR (Put-Call Ratio) Analysis")
            
            oi_analysis = analysis.get('oi_analysis', {})
            pcr_interpretation = oi_analysis.get('pcr_interpretation', {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "PCR Signal",
                    pcr_interpretation.get('signal', 'NEUTRAL'),
                    help=pcr_interpretation.get('interpretation', '')
                )
            
            with col2:
                st.metric(
                    "Confidence",
                    pcr_interpretation.get('confidence', 'LOW')
                )
            
            with col3:
                st.metric(
                    "Recommended Action",
                    pcr_interpretation.get('action', 'Follow technicals')
                )
            
            # OI Patterns
            st.subheader("📈 OI Patterns")
            
            oi_buildup = oi_analysis.get('oi_buildup', {})
            st.info(f"**Pattern:** {oi_buildup.get('pattern', 'BALANCED')}")
            st.write(f"**Interpretation:** {oi_buildup.get('interpretation', 'Normal OI distribution')}")
            st.write(f"**Risk Level:** {oi_buildup.get('risk_level', 'LOW')}")
            st.write(f"**Timeframe:** {oi_buildup.get('timeframe', 'MEDIUM_TERM')}")
            
            # Trading Signals
            st.subheader("🎯 Trading Signals")
            
            signals = analysis.get('trading_signals', [])
            
            if signals:
                for i, signal in enumerate(signals):
                    with st.expander(f"Signal {i+1}: {signal.get('type', 'UNKNOWN')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Type:** {signal.get('type', 'N/A')}")
                            st.write(f"**Reason:** {signal.get('reason', 'N/A')}")
                            st.write(f"**Confidence:** {signal.get('confidence', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Timeframe:** {signal.get('timeframe', 'N/A')}")
                            st.write(f"**Risk Level:** {signal.get('risk_level', 'N/A')}")
            else:
                st.warning("No trading signals generated at this time.")
            
            # Support/Resistance Levels
            st.subheader("🏗️ Support & Resistance Levels")
            
            levels_data = self.data_fetcher.get_support_resistance_levels(symbol)
            if levels_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Resistance Levels:**")
                    for level in levels_data.get('resistance_levels', []):
                        st.write(f"₹{level:,.2f}")
                
                with col2:
                    st.write("**Support Levels:**")
                    for level in levels_data.get('support_levels', []):
                        st.write(f"₹{level:,.2f}")
                
                current_price = levels_data.get('current_price', 0)
                nearest_resistance = levels_data.get('nearest_resistance')
                nearest_support = levels_data.get('nearest_support')
                
                st.write(f"**Current Price:** ₹{current_price:,.2f}")
                if nearest_resistance:
                    st.write(f"**Nearest Resistance:** ₹{nearest_resistance:,.2f}")
                if nearest_support:
                    st.write(f"**Nearest Support:** ₹{nearest_support:,.2f}")
    
    def _alerts_tab(self):
        """Alerts and signals tab"""
        st.header("🚨 Alerts & Trading Signals")
        
        # Alert setup
        st.subheader("Setup Alerts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_symbol = st.text_input(
                "Symbol for Alerts:",
                value=st.session_state.get('active_symbol', '^NSEI'),
                key="alert_symbol"
            )
            
            if st.button("Setup Breakout Alerts"):
                levels_data = self.data_fetcher.get_support_resistance_levels(alert_symbol)
                if levels_data:
                    alert_id = self.alert_system.setup_breakout_alerts(alert_symbol, levels_data)
                    if alert_id:
                        st.success(f"Breakout alerts setup for {alert_symbol}")
                        st.session_state['alert_id'] = alert_id
        
        with col2:
            pcr_threshold = st.number_input(
                "PCR Alert Threshold:",
                min_value=0.1,
                max_value=3.0,
                value=1.5,
                step=0.1,
                key="pcr_threshold"
            )
            
            if st.button("Setup PCR Alert"):
                alert_id = self.alert_system.setup_pcr_alerts(alert_symbol, pcr_threshold)
                if alert_id:
                    st.success(f"PCR alert setup for {alert_symbol}")
        
        # Active alerts
        st.subheader("Active Alerts")
        
        active_alerts = self.alert_system.get_active_alerts()
        
        if active_alerts:
            for alert_id, alert_config in active_alerts.items():
                with st.expander(f"Alert: {alert_config['symbol']} - {alert_config.get('alert_type', 'UNKNOWN')}"):
                    st.write(f"**Status:** {alert_config['status']}")
                    st.write(f"**Created:** {alert_config['created_at']}")
                    
                    if alert_config.get('nearest_resistance'):
                        st.write(f"**Resistance:** ₹{alert_config['nearest_resistance']:,.2f}")
                    
                    if alert_config.get('nearest_support'):
                        st.write(f"**Support:** ₹{alert_config['nearest_support']:,.2f}")
                    
                    if st.button(f"Cancel Alert {alert_id}", key=f"cancel_{alert_id}"):
                        self.alert_system.cancel_alert(alert_id)
                        st.rerun()
        else:
            st.info("No active alerts.")
        
        # Alert history
        st.subheader("Alert History")
        
        alert_history = self.alert_system.get_alert_history()
        
        if alert_history:
            for alert in alert_history[-5:]:  # Show last 5 alerts
                with st.expander(f"History: {alert['symbol']} - {alert['status']}"):
                    st.write(f"**Type:** {alert.get('alert_type', 'UNKNOWN')}")
                    st.write(f"**Created:** {alert['created_at']}")
                    st.write(f"**Status:** {alert['status']}")
                    
                    if alert.get('breakout_confirmed'):
                        st.write(f"**Breakout Price:** ₹{alert.get('breakout_price', 0):,.2f}")
                        st.write(f"**Breakout Time:** {alert.get('breakout_time', 'N/A')}")
                    
                    if alert.get('breakdown_confirmed'):
                        st.write(f"**Breakdown Price:** ₹{alert.get('breakdown_price', 0):,.2f}")
                        st.write(f"**Breakdown Time:** {alert.get('breakdown_time', 'N/A')}")
        else:
            st.info("No alert history.")
    
    def _cheatsheet_tab(self):
        """Master cheatsheet tab"""
        st.header("📋 Master OI Trading Cheatsheet")
        
        cheatsheet = self.oi_analyzer.get_oi_cheatsheet()
        
        # PCR Interpretation
        st.subheader("📊 PCR Interpretation Guide")
        
        pcr_guide = cheatsheet['pcr_interpretation']
        pcr_df = pd.DataFrame([
            {'PCR Range': k, 'Action': v}
            for k, v in pcr_guide.items()
        ])
        
        st.dataframe(pcr_df, width='stretch')
        
        # OI Patterns
        st.subheader("📈 OI Pattern Recognition")
        
        patterns = cheatsheet['oi_patterns']
        for pattern, description in patterns.items():
            st.write(f"**{pattern}:** {description}")
        
        # Trading Rules
        st.subheader("🎯 Trading Rules")
        
        rules = cheatsheet['trading_rules']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Buy Calls When:**")
            for rule in rules['Buy Calls When']:
                st.write(f"• {rule}")
        
        with col2:
            st.write("**Buy Puts When:**")
            for rule in rules['Buy Puts When']:
                st.write(f"• {rule}")
        
        st.write("**Avoid Trading When:**")
        for rule in rules['Avoid Trading When']:
            st.write(f"• {rule}")
        
        # Risk Management
        st.subheader("🛡️ Risk Management")
        
        risk_mgmt = cheatsheet['risk_management']
        for rule, value in risk_mgmt.items():
            st.write(f"**{rule}:** {value}")
        
        # Quick Reference
        st.subheader("⚡ Quick Reference")
        
        st.markdown("""
        ### Key Signals:
        - **PCR > 1.5** = Extreme fear, buy calls
        - **PCR < 0.5** = Extreme greed, buy puts
        - **PCR 0.8-1.2** = Neutral, follow technicals
        
        ### Breakout Trading:
        - **Entry:** At breakout level
        - **Stop Loss:** 2% below breakout (for calls) / 2% above (for puts)
        - **Take Profit:** 2:1 risk-reward ratio
        
        ### Volume Confirmation:
        - High volume confirms breakout
        - Low volume = false breakout risk
        - Volume spike = strong move likely
        """)
    
    def _settings_tab(self):
        """Settings tab"""
        st.header("⚙️ Settings & Configuration")
        
        st.subheader("Trading Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            capital = st.number_input(
                "Trading Capital (₹):",
                min_value=10000,
                max_value=10000000,
                value=self.config.DEFAULT_CAPITAL,
                step=10000
            )
            
            risk_per_trade = st.slider(
                "Risk per Trade (%):",
                min_value=0.5,
                max_value=5.0,
                value=self.config.MAX_RISK_PER_TRADE * 100,
                step=0.1
            )
        
        with col2:
            stop_loss = st.slider(
                "Default Stop Loss (%):",
                min_value=1.0,
                max_value=10.0,
                value=self.config.DEFAULT_STOP_LOSS_PERCENTAGE * 100,
                step=0.5
            )
            
            take_profit = st.slider(
                "Default Take Profit (%):",
                min_value=5.0,
                max_value=50.0,
                value=self.config.DEFAULT_TAKE_PROFIT_PERCENTAGE * 100,
                step=1.0
            )
        
        if st.button("Save Settings"):
            # Update config (in a real app, this would save to database/file)
            st.success("Settings saved!")
        
        # Notification settings
        st.subheader("Notification Settings")
        
        st.checkbox("Enable SMS Alerts", value=False)
        st.checkbox("Enable Email Alerts", value=False)
        st.checkbox("Enable Telegram Alerts", value=False)
        
        # API Keys (for demo purposes)
        st.subheader("API Configuration")
        
        st.text_input("Alpha Vantage API Key:", type="password")
        st.text_input("Twilio Account SID:", type="password")
        st.text_input("Telegram Bot Token:", type="password")
    
    def _start_monitoring(self, symbol):
        """Start monitoring for alerts"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                args=(symbol,),
                daemon=True
            )
            self.monitoring_thread.start()
            st.success(f"Started monitoring {symbol}")
    
    def _stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        st.success("Stopped monitoring")
    
    def _monitoring_loop(self, symbol):
        """Monitoring loop for alerts"""
        while self.is_monitoring:
            try:
                # Check alerts
                self.alert_system.check_breakout_alerts()
                self.alert_system.check_pcr_alerts()
                self.alert_system.check_volume_alerts()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
    
    def _ai_chat_tab(self):
        """AI Chat Assistant tab"""
        st.header("🤖 AI Trading Assistant")
        st.markdown("### Get real-time market analysis and trading recommendations!")
        
        # Create sub-tabs for different features
        chat_tab, chart_tab = st.tabs(["💬 AI Chat", "📈 Live Charts"])
        
        with chat_tab:
            self.ai_chat.render_chat_interface()
        
        with chart_tab:
            st.subheader("📈 Live Trading Charts")
            
            # Symbol selection for charts
            col1, col2 = st.columns([2, 1])
            
            with col1:
                chart_symbol = st.selectbox(
                    "Select Symbol for Live Chart:",
                    [
                        # Major Indices
                        "^NSEI", "^NSEBANK", "^BSESN", "NIFTY_FIN_SERVICE.NS",
                        # Banking
                        "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "SBIN.NS",
                        # IT & Technology
                        "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS",
                        # Oil & Gas
                        "RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS", "HPCL.NS",
                        # FMCG
                        "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "DABUR.NS", "TITAN.NS",
                        # Auto
                        "MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS",
                        # Pharma
                        "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "BIOCON.NS",
                        # Telecom
                        "BHARTIARTL.NS", "IDEA.NS",
                        # Power
                        "NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS",
                        # Metals
                        "TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "COALINDIA.NS",
                        # Cement
                        "ULTRACEMCO.NS", "SHREECEM.NS", "GRASIM.NS", "AMBUJACEM.NS",
                        # Real Estate
                        "DLF.NS", "GODREJPROP.NS",
                        # Media
                        "ZEEL.NS", "SUNTV.NS", "PVR.NS",
                        # Aviation
                        "INDIGO.NS", "SPICEJET.NS",
                        # E-commerce
                        "NYKAA.NS", "ZOMATO.NS", "PAYTM.NS",
                        # Infrastructure
                        "LT.NS", "ADANIPORTS.NS", "IRCTC.NS",
                        # Small & Mid Cap
                        "POLYCAB.NS", "ASTRAL.NS", "CROMPTON.NS", "HAVELLS.NS", "VOLTAS.NS"
                    ],
                    key="chart_symbol"
                )
            
            with col2:
                if st.button("🔄 Update Chart", key="update_chart"):
                    st.rerun()
            
            # Render live chart
            self.ai_chat.render_live_chart(chart_symbol)
            
            # Additional chart options
            st.subheader("📊 Chart Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.checkbox("Show RSI", value=True, key="show_rsi")
                st.checkbox("Show MACD", value=True, key="show_macd")
            
            with col2:
                st.checkbox("Show Bollinger Bands", value=False, key="show_bb")
                st.checkbox("Show Volume", value=True, key="show_volume")
            
            with col3:
                st.checkbox("Show Support/Resistance", value=True, key="show_sr")
                st.checkbox("Auto-refresh", value=True, key="auto_refresh")

def main():
    """Main function to run the trading agent"""
    agent = IndianStockTradingAgent()
    agent.run_streamlit_app()

if __name__ == "__main__":
    main()
