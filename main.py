#!/usr/bin/env python3
"""
Indian Stock Market AI Agent
Advanced OI Analysis, PCR Calculator & Breakout Alerts

Usage:
    python main.py --web          # Run web interface
    python main.py --cli          # Run command line interface
    python main.py --analyze NIFTY50  # Quick analysis
    python main.py --alerts       # Start alert monitoring
"""

import argparse
import sys
import logging
from datetime import datetime
from data_fetcher import IndianMarketDataFetcher
from oi_analyzer import OIAnalyzer
from alert_system import AlertSystem
from trading_agent import IndianStockTradingAgent
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_web_interface():
    """Run the Streamlit web interface"""
    try:
        import streamlit.web.cli as stcli
        import sys
        import os
        
        # Check if running in production environment
        port = os.environ.get('PORT', '8501')
        host = os.environ.get('HOST', '0.0.0.0')
        
        # Set up command line arguments for Streamlit
        sys.argv = [
            "streamlit", 
            "run", 
            "trading_agent.py",
            "--server.port", port,
            "--server.address", host,
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        print(f"🌐 Starting web interface on {host}:{port}")
        sys.exit(stcli.main())
    except ImportError:
        print("Streamlit not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        run_web_interface()

def run_streamlit_app():
    """Direct function to run the Streamlit app - used by Streamlit Cloud"""
    from trading_agent import IndianStockTradingAgent
    agent = IndianStockTradingAgent()
    agent.run_streamlit_app()

def run_cli_interface():
    """Run the command line interface"""
    print("🇮🇳 Indian Stock Market AI Agent - CLI Mode")
    print("=" * 50)
    
    config = Config()
    data_fetcher = IndianMarketDataFetcher()
    oi_analyzer = OIAnalyzer()
    alert_system = AlertSystem()
    
    while True:
        print("\n📊 Available Options:")
        print("1. Market Overview")
        print("2. OI Analysis")
        print("3. Setup Alerts")
        print("4. View Master Cheatsheet")
        print("5. Start Live Monitoring")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            show_market_overview(data_fetcher)
        elif choice == "2":
            run_oi_analysis(oi_analyzer)
        elif choice == "3":
            setup_alerts_cli(alert_system, data_fetcher)
        elif choice == "4":
            show_cheatsheet(oi_analyzer)
        elif choice == "5":
            start_live_monitoring(alert_system)
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def show_market_overview(data_fetcher):
    """Show market overview in CLI"""
    print("\n📊 Market Overview")
    print("-" * 30)
    
    overview = data_fetcher.get_market_overview()
    
    if overview:
        for name, data in overview.items():
            print(f"{name}:")
            print(f"  Price: ₹{data['price']:,.2f}")
            print(f"  Change: ₹{data['change']:,.2f} ({data['change_percent']:.2f}%)")
            print(f"  Volume: {data['volume']:,.0f}")
            print()
    else:
        print("❌ Unable to fetch market data")

def run_oi_analysis(oi_analyzer):
    """Run OI analysis in CLI"""
    print("\n🔍 OI Analysis")
    print("-" * 30)
    
    symbol = input("Enter symbol (e.g., ^NSEI, RELIANCE.NS): ").strip()
    
    if not symbol:
        print("❌ Please enter a valid symbol")
        return
    
    print(f"Analyzing {symbol}...")
    
    analysis = oi_analyzer.analyze_oi_data(symbol)
    
    if analysis:
        print(f"\n✅ Analysis completed for {symbol}")
        
        oi_analysis = analysis.get('oi_analysis', {})
        pcr_interpretation = oi_analysis.get('pcr_interpretation', {})
        
        print(f"\n📊 PCR Analysis:")
        print(f"  Signal: {pcr_interpretation.get('signal', 'NEUTRAL')}")
        print(f"  Confidence: {pcr_interpretation.get('confidence', 'LOW')}")
        print(f"  Action: {pcr_interpretation.get('action', 'Follow technicals')}")
        
        signals = analysis.get('trading_signals', [])
        if signals:
            print(f"\n🎯 Trading Signals ({len(signals)} found):")
            for i, signal in enumerate(signals, 1):
                print(f"  {i}. {signal.get('type', 'UNKNOWN')}")
                print(f"     Reason: {signal.get('reason', 'N/A')}")
                print(f"     Confidence: {signal.get('confidence', 'N/A')}")
        else:
            print("\n⚠️ No trading signals generated")
    else:
        print("❌ Unable to analyze symbol")

def setup_alerts_cli(alert_system, data_fetcher):
    """Setup alerts in CLI"""
    print("\n🚨 Alert Setup")
    print("-" * 30)
    
    symbol = input("Enter symbol for alerts: ").strip()
    
    if not symbol:
        print("❌ Please enter a valid symbol")
        return
    
    print(f"\nSetting up alerts for {symbol}...")
    
    # Setup breakout alerts
    levels_data = data_fetcher.get_support_resistance_levels(symbol)
    if levels_data:
        alert_id = alert_system.setup_breakout_alerts(symbol, levels_data)
        if alert_id:
            print(f"✅ Breakout alerts setup (ID: {alert_id})")
        else:
            print("❌ Failed to setup breakout alerts")
    
    # Setup PCR alerts
    pcr_threshold = input("Enter PCR threshold (default 1.5): ").strip()
    try:
        pcr_threshold = float(pcr_threshold) if pcr_threshold else 1.5
        alert_id = alert_system.setup_pcr_alerts(symbol, pcr_threshold)
        if alert_id:
            print(f"✅ PCR alerts setup (ID: {alert_id})")
        else:
            print("❌ Failed to setup PCR alerts")
    except ValueError:
        print("❌ Invalid PCR threshold")

def show_cheatsheet(oi_analyzer):
    """Show master cheatsheet in CLI"""
    print("\n📋 Master OI Trading Cheatsheet")
    print("=" * 50)
    
    cheatsheet = oi_analyzer.get_oi_cheatsheet()
    
    print("\n📊 PCR Interpretation:")
    for pcr_range, action in cheatsheet['pcr_interpretation'].items():
        print(f"  {pcr_range}: {action}")
    
    print("\n📈 OI Patterns:")
    for pattern, description in cheatsheet['oi_patterns'].items():
        print(f"  {pattern}: {description}")
    
    print("\n🎯 Trading Rules:")
    print("  Buy Calls When:")
    for rule in cheatsheet['trading_rules']['Buy Calls When']:
        print(f"    • {rule}")
    
    print("  Buy Puts When:")
    for rule in cheatsheet['trading_rules']['Buy Puts When']:
        print(f"    • {rule}")
    
    print("  Avoid Trading When:")
    for rule in cheatsheet['trading_rules']['Avoid Trading When']:
        print(f"    • {rule}")
    
    print("\n🛡️ Risk Management:")
    for rule, value in cheatsheet['risk_management'].items():
        print(f"  {rule}: {value}")

def start_live_monitoring(alert_system):
    """Start live monitoring in CLI"""
    print("\n🚨 Live Monitoring")
    print("-" * 30)
    print("Starting live monitoring...")
    print("Press Ctrl+C to stop")
    
    try:
        alert_system.start_monitoring()
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring stopped")

def quick_analysis(symbol):
    """Quick analysis for a specific symbol"""
    print(f"🔍 Quick Analysis for {symbol}")
    print("-" * 40)
    
    data_fetcher = IndianMarketDataFetcher()
    oi_analyzer = OIAnalyzer()
    
    # Get live data
    live_data = data_fetcher.get_live_price(symbol)
    if live_data:
        print(f"Current Price: ₹{live_data['price']:,.2f}")
        print(f"Change: ₹{live_data['change']:,.2f} ({live_data['change_percent']:.2f}%)")
        print(f"Volume: {live_data['volume']:,.0f}")
    
    # Get OI analysis
    analysis = oi_analyzer.analyze_oi_data(symbol)
    if analysis:
        oi_analysis = analysis.get('oi_analysis', {})
        pcr_interpretation = oi_analysis.get('pcr_interpretation', {})
        
        print(f"\nPCR Signal: {pcr_interpretation.get('signal', 'NEUTRAL')}")
        print(f"Action: {pcr_interpretation.get('action', 'Follow technicals')}")
        
        signals = analysis.get('trading_signals', [])
        if signals:
            print(f"\nTrading Signals: {len(signals)} found")
            for signal in signals:
                print(f"  • {signal.get('type', 'UNKNOWN')}: {signal.get('reason', 'N/A')}")
        else:
            print("\nNo trading signals")
    else:
        print("❌ Unable to analyze symbol")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Indian Stock Market AI Agent - Advanced OI Analysis & Trading Signals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Run web interface
  python main.py --cli                    # Run command line interface
  python main.py --analyze NIFTY50        # Quick analysis for NIFTY50
  python main.py --alerts                 # Start alert monitoring
        """
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Run web interface (Streamlit)'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run command line interface'
    )
    
    parser.add_argument(
        '--analyze',
        type=str,
        help='Quick analysis for a specific symbol'
    )
    
    parser.add_argument(
        '--alerts',
        action='store_true',
        help='Start alert monitoring'
    )
    
    args = parser.parse_args()
    
    if args.web:
        print("🌐 Starting web interface...")
        run_web_interface()
    elif args.cli:
        run_cli_interface()
    elif args.analyze:
        quick_analysis(args.analyze)
    elif args.alerts:
        print("🚨 Starting alert monitoring...")
        alert_system = AlertSystem()
        start_live_monitoring(alert_system)
    else:
        # Default: show help
        parser.print_help()

if __name__ == "__main__":
    main()
