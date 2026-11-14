# 🤖 ChatGPT Integration: Custom GPTs & OpenAI Actions

Connect the **Wall Street Hedge Fund Suite** directly into ChatGPT using OpenAI Custom GPT Actions.
No local MCP server required — executes natively via OpenAI cloud actions.

---

## ⚡ 60-Second Setup Guide (ChatGPT Plus / Team / Enterprise)

1. Go to **[ChatGPT](https://chatgpt.com)** and click **Explore GPTs** in the sidebar.
2. Click **+ Create** (top right) and switch to the **Configure** tab.
3. Fill in the basic info:
   - **Name**: `Wall Street Hedge Fund Analyst`
   - **Description**: `Institutional 360° Quant, Buffett Moat, Piotroski & TTM Squeeze Investment Memo Engine`
   - **Instructions**: Copy and paste the contents of [`custom-gpt-instructions.md`](custom-gpt-instructions.md).
4. Scroll down to **Actions** and click **Create new action**:
   - In the **Schema** box, copy and paste the contents of [`openapi-actions-schema.yaml`](openapi-actions-schema.yaml).
5. Click **Publish** (top right):
   - Choose **Everyone** (public on GPT Store) or **Anyone with a link** (private team link).
6. Done! Test by typing: *"Run a full 360° quant audit on NVDA"*.

---

## 💡 How Free ChatGPT Users Can Monitize & Share

- **Free users** can freely use any published public Custom GPT.
- By deploying this Custom GPT as public (**Everyone**), any user worldwide can interact with your institutional investment memo bot.
- All underlying API executions route directly through your Apify Actor endpoint, generating Pay-Per-Event (PPE) revenue automatically!
