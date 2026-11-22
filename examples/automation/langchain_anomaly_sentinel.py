"""
LangChain Anomaly Sentinel: Monitors high-beta equities for forensic accounting red flags & insolvency risks.
"""

import os
import sys

try:
    from langchain_mcp_adapters.tools import load_mcp_tools
    from langchain_openai import ChatOpenAI
except ImportError:
    print("Error: Missing required packages.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def get_mcp_tools():
    url = "https://mcp.apify.com/?actors=mcp_collector/wallstreet-hedgefund-suite-mcp"
    if APIFY_TOKEN:
        url += f"&token={APIFY_TOKEN}"
    return load_mcp_tools(url)

def run_anomaly_check(tickers=["TSLA", "NVDA", "AAPL"]):
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY is not set.")
        return

    print("Loading Wall Street MCP tools...")
    tools = get_mcp_tools()
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = llm.bind_tools(tools)

    for ticker in tickers:
        print(f"\nScanning {ticker} for accounting anomalies & insolvency risk...")
        prompt = (
            f"Perform a forensic audit on {ticker} using the Wall Street MCP tools.\n"
            "Specifically check:\n"
            "1. Altman Z-Score: Is it in the Distress Zone (<1.81) or Grey Zone (1.81-2.99)?\n"
            "2. Beneish M-Score: Is there any earnings manipulation flag (M > -1.78)?\n"
            "3. Piotroski F-Score: Are there any fundamental deterioration points?\n"
            "Provide a definitive Sentinel Alert Level: [GREEN - Normal], [YELLOW - Caution], or [RED - Immediate Review]."
        )
        response = agent.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        print(f"--- RESULT FOR {ticker} ---")
        print(content)

if __name__ == "__main__":
    run_anomaly_check()
