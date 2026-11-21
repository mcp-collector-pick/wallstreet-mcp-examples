# 🤖 ChatGPT Integration: Official Plugins & Custom GPTs

Connect the **Wall Street Hedge Fund Suite** directly into ChatGPT.
Executes serverless institutional quant calculations via remote MCP and OpenAPI actions with zero local setup.

---

## ⚡ Method 1: Official 2026 ChatGPT Plugin (OAuth 2.1 Gateway) — Recommended

Uses the official Agent Plugins standard (`plugin.json` + `mcp.json` + `skills/`) with the dedicated high-speed serverless OAuth Gateway.

- **MCP Server URL**: `https://wallstreet.mcp-collector.workers.dev`
- **OAuth Authorization URL**: `https://wallstreet.mcp-collector.workers.dev/oauth/authorize`
- **OAuth Token URL**: `https://wallstreet.mcp-collector.workers.dev/oauth/token`

### How It Works for Global Users:
1. When a user invokes the plugin in ChatGPT, a secure authorization card appears.
2. The user inputs their personal Apify API Token (Free accounts include **$5/month recurring credits = ~625 quant audits/month**).
3. ChatGPT authenticates seamlessly via OAuth 2.1, executing quantitative audits on NVDA, AAPL, TSLA, and 60+ models.

---

## 🛠️ Method 2: Custom GPT Actions (OpenAPI 3.0)

For environments still utilizing legacy Custom GPT configurations:
1. Go to **[ChatGPT](https://chatgpt.com)** → **Explore GPTs** → **Create**.
2. **Instructions**: Copy and paste [`custom-gpt-instructions.md`](custom-gpt-instructions.md).
3. **Actions**: Import [`openapi-actions-schema.yaml`](openapi-actions-schema.yaml).
4. Publish to **Everyone** or **Anyone with a link**.
