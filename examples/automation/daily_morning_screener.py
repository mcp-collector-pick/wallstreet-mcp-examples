"""
Daily S&P 500 Morning Screener using Wall Street MCP Suite.
Runs institutional 360° quantitative audit across your portfolio before market open.
"""

import os
import sys
import json
from datetime import datetime

# Check dependencies
try:
    from langchain_mcp_adapters.tools import load_mcp_tools
    from langchain_openai import ChatOpenAI
except ImportError:
    print("Error: Missing required packages.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Configuration from Environment Variables
APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Default Watchlist
WATCHLIST = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

def get_mcp_endpoint() -> str:
    base = "https://mcp.apify.com/?actors=mcp_collector/wallstreet-hedgefund-suite-mcp"
    if APIFY_TOKEN:
        return f"{base}&token={APIFY_TOKEN}"
    return base

def run_screener():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initializing Wall Street Screener...")
    
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY is not set. Please set it to run the reasoning agent.")
        return

    # 1. Connect to Wall Street MCP Suite via Apify
    mcp_endpoint = get_mcp_endpoint()
    print(f"Connecting to MCP Endpoint: {mcp_endpoint[:60]}...")
    tools = load_mcp_tools(mcp_endpoint)
    
    # 2. Initialize Reasoning Model
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = llm.bind_tools(tools)
    
    tickers_str = ", ".join(WATCHLIST)
    prompt = (
        f"You are a hedge fund portfolio manager. Audit this watchlist: {tickers_str}.\n"
        "For each ticker, call the Wall Street Suite tools to obtain:\n"
        "- 9-point Piotroski F-Score\n"
        "- Altman Z-Score\n"
        "- TTM Squeeze state\n"
        "Format the output as a clean Markdown table with columns: "
        "Ticker, Piotroski (0-9), Altman Z, TTM Squeeze, Institutional Verdict (BULLISH/NEUTRAL/BEARISH)."
    )
    
    print("Executing quantitative audit across watchlist...")
    response = agent.invoke(prompt)
    report_content = response.content if hasattr(response, "content") else str(response)
    
    print("\n" + "="*60)
    print(f"WALL STREET MORNING REPORT ({datetime.now().strftime('%Y-%m-%d')})")
    print("="*60)
    print(report_content)
    print("="*60 + "\n")
    
    # Optional Slack Webhook notification
    if SLACK_WEBHOOK_URL:
        try:
            import requests
            requests.post(SLACK_WEBHOOK_URL, json={"text": f"*Wall Street Morning Screener*\n\n{report_content}"}, timeout=10)
            print("Alert successfully sent to Slack.")
        except Exception as e:
            print(f"Failed to post to Slack: {e}")

if __name__ == "__main__":
    run_screener()
