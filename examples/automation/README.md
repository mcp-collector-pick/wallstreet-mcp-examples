# 🤖 Wall Street Autonomous Agent Automation Recipes

This folder contains ready-to-run automation recipes that turn the Wall Street MCP Suite into **24/7 automated quant research assistants**.

---

## 📦 Quick Installation

```bash
cd examples/automation
pip install -r requirements.txt
```

Set your API keys:

```bash
# Required for OpenAI reasoning models
export OPENAI_API_KEY="your-openai-api-key"

# Optional: Add your Apify token for unlimited dedicated capacity
export APIFY_TOKEN="your-apify-token"

# Optional: For Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

*(On Windows PowerShell, use `$env:OPENAI_API_KEY="your-key"`)*

---

## 🛠 Available Automation Recipes

### 1. `daily_morning_screener.py`
- **What it does**: Automatically audits an equity watchlist (NVDA, AAPL, MSFT, TSLA, etc.) before market open.
- **Output**: Generates a clean Markdown table with Piotroski F-Scores, Altman Z-Scores, TTM Squeeze states, and Institutional Verdicts.
- **Alerts**: Dispatches summary directly to your Slack channel if `SLACK_WEBHOOK_URL` is set.
- **Cron setup**:
  ```bash
  # Run every weekday at 08:30 AM EST (13:30 UTC)
  30 13 * * 1-5 /usr/bin/python3 /path/to/daily_morning_screener.py
  ```

### 2. `crewai_hedgefund_team.py`
- **What it does**: Deploys a **3-agent autonomous quant team** (Forensic Analyst, Risk Officer, and Chief Investment Officer) using CrewAI.
- **Output**: A comprehensive 1-page institutional Investment Committee Memo with final allocation ratings (STRONG BUY, BUY, HOLD, UNDERWEIGHT).

### 3. `langchain_anomaly_sentinel.py`
- **What it does**: Scans portfolio holdings for accounting anomalies and insolvency signals (Beneish M-Score and Altman Z-Score distress zones).
- **Output**: Sentinel Alert Levels: `[GREEN - Normal]`, `[YELLOW - Caution]`, or `[RED - Immediate Review]`.

---

## 💡 How MCP Powers These Agents

Traditional financial agents suffer from severe numerical hallucinations when asked to calculate valuation formulas from raw financial reports. 

The Wall Street MCP Suite solves this by injecting **pre-computed, deterministic values directly into the LLM context window**, giving you institutional-grade reliability with 94.8% fewer tokens.
