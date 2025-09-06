#!/usr/bin/env python3
"""
Indian Stock Market AI Agent - Streamlit App
This is the main entry point for Streamlit Cloud deployment
"""

import streamlit as st
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the trading agent
from trading_agent import IndianStockTradingAgent

def main():
    """Main function for Streamlit app"""
    # Create and run the trading agent
    agent = IndianStockTradingAgent()
    agent.run_streamlit_app()

if __name__ == "__main__":
    main()
