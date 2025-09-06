#!/usr/bin/env python3
"""
Quick Start Script for Indian Stock Market AI Agent
Run this to test the system immediately!
"""

import sys
import time
from datetime import datetime
from data_fetcher import IndianMarketDataFetcher
from oi_analyzer import OIAnalyzer
from alert_system import AlertSystem

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🇮🇳 INDIAN STOCK MARKET AI AGENT")
    print("📊 Advanced OI Analysis & Trading Signals")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def demo_market_overview():
    """Demo market overview"""
    print("📊 DEMO: Market Overview")
    print("-" * 40)
    
    data_fetcher = IndianMarketDataFetcher()
    overview = data_fetcher.get_market_overview()
    
    if overview:
        for name, data in overview.items():
            print(f"{name:12} ₹{data['price']:8,.2f} {data['change_percent']:+6.2f}%")
    else:
        print("❌ Unable to fetch market data")
    
    print()

def demo_oi_analysis():
    """Demo OI analysis"""
    print("🔍 DEMO: OI Analysis for NIFTY50")
    print("-" * 40)
    
    oi_analyzer = OIAnalyzer()
    analysis = oi_analyzer.analyze_oi_data("^NSEI")
    
    if analysis:
        oi_analysis = analysis.get('oi_analysis', {})
        pcr_interpretation = oi_analysis.get('pcr_interpretation', {})
        
        print(f"PCR Signal:     {pcr_interpretation.get('signal', 'NEUTRAL')}")
        print(f"Confidence:     {pcr_interpretation.get('confidence', 'LOW')}")
        print(f"Action:         {pcr_interpretation.get('action', 'Follow technicals')}")
        
        signals = analysis.get('trading_signals', [])
        if signals:
            print(f"\nTrading Signals: {len(signals)} found")
            for signal in signals:
                print(f"  • {signal.get('type', 'UNKNOWN')}: {signal.get('reason', 'N/A')}")
        else:
            print("\nNo trading signals generated")
    else:
        print("❌ Unable to analyze NIFTY50")
    
    print()

def demo_cheatsheet():
    """Demo cheatsheet"""
    print("📋 DEMO: Master Cheatsheet Preview")
    print("-" * 40)
    
    oi_analyzer = OIAnalyzer()
    cheatsheet = oi_analyzer.get_oi_cheatsheet()
    
    print("PCR Interpretation:")
    for pcr_range, action in list(cheatsheet['pcr_interpretation'].items())[:3]:
        print(f"  {pcr_range}: {action}")
    
    print("\nTrading Rules:")
    print("  Buy Calls When:")
    for rule in cheatsheet['trading_rules']['Buy Calls When'][:2]:
        print(f"    • {rule}")
    
    print("  Buy Puts When:")
    for rule in cheatsheet['trading_rules']['Buy Puts When'][:2]:
        print(f"    • {rule}")
    
    print()

def demo_alerts():
    """Demo alert system"""
    print("🚨 DEMO: Alert System")
    print("-" * 40)
    
    alert_system = AlertSystem()
    
    # Setup a demo alert
    print("Setting up demo breakout alert for NIFTY50...")
    
    data_fetcher = IndianMarketDataFetcher()
    levels_data = data_fetcher.get_support_resistance_levels("^NSEI")
    
    if levels_data:
        alert_id = alert_system.setup_breakout_alerts("^NSEI", levels_data)
        if alert_id:
            print(f"✅ Demo alert setup (ID: {alert_id})")
            
            # Show active alerts
            active_alerts = alert_system.get_active_alerts()
            print(f"Active alerts: {len(active_alerts)}")
            
            # Clean up demo alert
            alert_system.cancel_alert(alert_id)
            print("🧹 Demo alert cleaned up")
        else:
            print("❌ Failed to setup demo alert")
    else:
        print("❌ Unable to get support/resistance levels")
    
    print()

def show_usage_instructions():
    """Show usage instructions"""
    print("🎯 HOW TO USE THE AI AGENT")
    print("=" * 40)
    print()
    print("1. 🌐 WEB INTERFACE (Recommended):")
    print("   python main.py --web")
    print("   Opens beautiful dashboard at http://localhost:8501")
    print()
    print("2. 💻 COMMAND LINE:")
    print("   python main.py --cli")
    print("   Interactive command-line interface")
    print()
    print("3. ⚡ QUICK ANALYSIS:")
    print("   python main.py --analyze NIFTY50")
    print("   python main.py --analyze RELIANCE.NS")
    print()
    print("4. 🚨 ALERT MONITORING:")
    print("   python main.py --alerts")
    print("   Start real-time alert monitoring")
    print()
    print("5. 📋 MASTER CHEATSHEET:")
    print("   Available in web interface or CLI")
    print()

def main():
    """Main demo function"""
    print_banner()
    
    print("🚀 Running quick demo...")
    print()
    
    try:
        # Run demos
        demo_market_overview()
        demo_oi_analysis()
        demo_cheatsheet()
        demo_alerts()
        
        print("✅ Demo completed successfully!")
        print()
        
        # Show usage instructions
        show_usage_instructions()
        
        print("🎉 Ready to start trading with AI!")
        print()
        print("💡 Tip: Run 'python main.py --web' for the full experience")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
