"""
CrewAI Autonomous Hedge Fund Screener
Runs a daily S&P 500 sector scan and generates investment memos.
Requires: pip install crewai langchain-mcp-adapters
"""
from crewai import Agent, Task, Crew
from langchain_mcp_adapters.tools import load_mcp_tools

# Load all 60 quant engines as tools
mcp_tools = load_mcp_tools(
    "https://mcp.apify.com/?actors=mcp_collector/wallstreet-hedgefund-suite-mcp"
)

# Define the analyst agent
quant_analyst = Agent(
    role="Institutional Quantitative Equity Analyst",
    goal="Identify high-conviction investment opportunities using deterministic quant metrics",
    backstory=(
        "You are a senior analyst at a multi-billion dollar hedge fund. "
        "You rely exclusively on pre-computed quantitative indicators — "
        "never estimate or hallucinate financial data."
    ),
    tools=mcp_tools,
    verbose=True,
)

# Define the screening task
daily_screen = Task(
    description=(
        "1. Run sector rotation analysis on S&P 500 (11 SPDR sectors vs SPY).\n"
        "2. Identify the top 2 sectors with strongest relative momentum.\n"
        "3. For the top holding in each sector, run a full 360° quant audit:\n"
        "   - ROIC vs WACC moat spread\n"
        "   - 9-point Piotroski F-Score\n"
        "   - TTM Squeeze state\n"
        "   - 13F whale flow & insider activity\n"
        "4. Generate a concise investment memo with 2ATR stop-loss levels."
    ),
    expected_output="Two structured investment memos in Markdown format.",
    agent=quant_analyst,
)

# Run the crew
crew = Crew(agents=[quant_analyst], tasks=[daily_screen], verbose=True)
result = crew.kickoff()
print(result)
