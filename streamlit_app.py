#!/usr/bin/env python3
"""
Indian Stock Market AI Agent - Streamlit App
Main entry point for Streamlit Cloud
"""

import streamlit as st
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the trading agent
from trading_agent import IndianStockTradingAgent

# Create and run the trading agent
agent = IndianStockTradingAgent()
agent.run_streamlit_app()
