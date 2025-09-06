#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

def test_imports():
    """Test all imports"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import streamlit as st
        print("✅ streamlit imported")
        
        import pandas as pd
        print("✅ pandas imported")
        
        import numpy as np
        print("✅ numpy imported")
        
        import yfinance as yf
        print("✅ yfinance imported")
        
        import plotly.graph_objects as go
        print("✅ plotly imported")
        
        import ta
        print("✅ ta imported")
        
        # Test custom imports
        from config import Config
        print("✅ config imported")
        
        from data_fetcher import IndianMarketDataFetcher
        print("✅ data_fetcher imported")
        
        from oi_analyzer import OIAnalyzer
        print("✅ oi_analyzer imported")
        
        from alert_system import AlertSystem
        print("✅ alert_system imported")
        
        from ai_chat_component import AIChatComponent
        print("✅ ai_chat_component imported")
        
        from trading_agent import IndianStockTradingAgent
        print("✅ trading_agent imported")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
