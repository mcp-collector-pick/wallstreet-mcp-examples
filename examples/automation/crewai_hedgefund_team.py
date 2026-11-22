"""
CrewAI Multi-Agent Hedge Fund Research Team.
Deploys 3 specialized agents (Forensic Analyst, Risk Officer, CIO) to synthesize an institutional investment memo.
"""

import os
import sys

# Check dependencies
try:
    from crewai import Agent, Task, Crew, Process
    from langchain_mcp_adapters.tools import load_mcp_tools
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

def build_hedgefund_crew(ticker: str):
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is required to run CrewAI agents.")
        print("Set it via: export OPENAI_API_KEY='your-key' (or $env:OPENAI_API_KEY in PowerShell)")
        sys.exit(1)

    tools = get_mcp_tools()
    
    # 1. Forensic Fundamental Analyst
    forensic_analyst = Agent(
        role="Forensic Fundamental Analyst",
        goal="Audit balance sheet integrity, earnings quality (Beneish M-Score), and capital returns (ROIC vs WACC).",
        backstory=(
            "You are a CFA charterholder with 15 years on Wall Street. You distrust GAAP earnings "
            "and verify all metrics using deterministic quant tools. Never hallucinate financial ratios."
        ),
        tools=tools,
        verbose=True
    )

    # 2. Downside Risk Manager
    risk_manager = Agent(
        role="Hedge Fund Chief Risk Officer",
        goal="Identify insolvency risk (Altman Z-Score), volatility compression (TTM Squeeze), and tail drawdown risk.",
        backstory=(
            "Your sole focus is capital preservation. You analyze solvency zones, liquidity buffers, "
            "and technical downside triggers to establish stop-loss thresholds."
        ),
        tools=tools,
        verbose=True
    )

    # 3. Chief Investment Officer
    cio = Agent(
        role="Chief Investment Officer (CIO)",
        goal="Synthesize forensic analysis and risk parameters into a high-conviction 1-page Investment Committee Memo.",
        backstory=(
            "You manage a $5B long/short equity book. You make final capital allocation decisions based "
            "strictly on deterministic evidence, issuing definitive ratings: STRONG BUY, BUY, HOLD, or UNDERWEIGHT."
        ),
        verbose=True
    )

    # Define Tasks
    task_forensics = Task(
        description=f"Run a forensic audit on {ticker}. Evaluate Piotroski F-Score (0-9) and economic moat.",
        expected_output="Detailed breakdown of fundamental health, moat spread, and earnings quality.",
        agent=forensic_analyst
    )

    task_risk = Task(
        description=f"Evaluate insolvency and market risk for {ticker}. Check Altman Z-Score and TTM Squeeze state.",
        expected_output="Risk assessment including distress zone classification and volatility status.",
        agent=risk_manager
    )

    task_committee_memo = Task(
        description=(
            f"Synthesize the findings for {ticker} into an executive Investment Committee Memo.\n"
            "Include: Executive Summary, Key Strengths, Tail Risks, and Final Rating."
        ),
        expected_output="1-page institutional Investment Committee Memo in Markdown format.",
        agent=cio
    )

    return Crew(
        agents=[forensic_analyst, risk_manager, cio],
        tasks=[task_forensics, task_risk, task_committee_memo],
        process=Process.sequential,
        verbose=True
    )

if __name__ == "__main__":
    target_ticker = "NVDA"
    print(f"Deploying Wall Street Multi-Agent Research Team for {target_ticker}...")
    crew = build_hedgefund_crew(target_ticker)
    result = crew.kickoff()
    print("\n" + "="*70)
    print("FINAL INVESTMENT COMMITTEE MEMO")
    print("="*70)
    print(result)
