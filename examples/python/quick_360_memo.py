"""
Quick 360° Investment Memo — 5-Line Example
Requires: pip install langchain-mcp-adapters langchain-openai
"""
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = load_mcp_tools(
    "https://mcp.apify.com/?actors=mcp_collector/wallstreet-hedgefund-suite-mcp"
)
agent = llm.bind_tools(tools)

# Change the ticker to any US stock or ETF
response = agent.invoke(
    "Run a 360° institutional quant audit on NVDA: "
    "ROIC vs WACC moat, 9-point Piotroski F-Score, Altman Z, "
    "TTM Squeeze state, and 13F whale flow."
)
print(response)
