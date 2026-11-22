# ⚡ wallstreet-mcp-tools (Python SDK)

Lightweight Python SDK for **Wall Street Hedge Fund Suite** on Apify via the Model Context Protocol (MCP).

---

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install wallstreet-mcp-tools
```

### With LangChain Support
```bash
pip install "wallstreet-mcp-tools[langchain]"
```

---

## 🚀 Quick Usage

### 1. Direct Python SDK Call
```python
from wallstreet_mcp import WallStreetClient

# Automatically reads APIFY_TOKEN from environment if not passed
client = WallStreetClient(token="YOUR_APIFY_TOKEN")

# Run 360° audit on any US ticker
audit = client.audit("NVDA")
print(f"Piotroski F-Score: {audit.get('piotroski_f_score')}/9")
print(f"Altman Z-Score: {audit.get('altman_z_score')}")
```

### 2. LangChain Integration
```python
from wallstreet_mcp import WallStreetClient
from langchain_openai import ChatOpenAI

client = WallStreetClient()
tools = client.load_langchain_tools()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = llm.bind_tools(tools)

res = agent.invoke("Run a 360° quant audit on NVDA")
print(res.content)
```

---

## 📄 License
MIT License.
