"""
Wall Street MCP Client: Lightweight Python SDK for calling 60+ institutional hedge fund engines.
"""

import os
import requests
from typing import Dict, Any, List, Optional

class WallStreetClient:
    """
    Python client for Wall Street Hedge Fund Suite on Apify.
    Provides direct access to deterministic valuation and quant calculation engines.
    """
    
    BASE_URL = "https://api.apify.com/v2/acts/mcp_collector~wallstreet-hedgefund-suite-mcp/run-sync-get-dataset-items"
    MCP_ENDPOINT = "https://mcp.apify.com/?actors=mcp_collector/wallstreet-hedgefund-suite-mcp"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("APIFY_TOKEN", "")
        self.headers = {"Content-Type": "application/json"}
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def get_mcp_url(self) -> str:
        """Returns the full SSE MCP URL for LangChain/CrewAI adapters."""
        if self.token:
            return f"{self.MCP_ENDPOINT}&token={self.token}"
        return self.MCP_ENDPOINT

    def audit(self, ticker: str, engines: Optional[List[str]] = None, timeout: int = 120) -> Dict[str, Any]:
        """
        Run a 360° institutional audit or specific engines for a given ticker.
        """
        if not self.token:
            raise ValueError(
                "Apify API token is required for direct REST execution. "
                "Pass token='...' or set the APIFY_TOKEN environment variable.\n"
                "Get your free token at: https://console.apify.com/account/integrations"
            )
            
        payload: Dict[str, Any] = {"ticker": ticker.strip().upper()}
        if engines:
            payload["engines"] = engines
            
        response = requests.post(self.BASE_URL, headers=self.headers, json=payload, timeout=timeout)
        response.raise_for_status()
        items = response.json()
        return items[0] if isinstance(items, list) and len(items) > 0 else (items if isinstance(items, dict) else {})

    def piotroski(self, ticker: str) -> int:
        """Fetches 9-point Piotroski F-Score for fundamental health."""
        res = self.audit(ticker, engines=["piotroski_f_score"])
        return int(res.get("piotroski_f_score", 0))

    def altman_z(self, ticker: str) -> float:
        """Fetches Altman Z-Score for insolvency risk."""
        res = self.audit(ticker, engines=["altman_z_score"])
        return float(res.get("altman_z_score", 0.0))

    def load_langchain_tools(self):
        """Helper to load tools directly into LangChain if langchain_mcp_adapters is installed."""
        try:
            from langchain_mcp_adapters.tools import load_mcp_tools
            return load_mcp_tools(self.get_mcp_url())
        except ImportError:
            raise ImportError(
                "langchain-mcp-adapters is required for this method. "
                "Install it with: pip install wallstreet-mcp-tools[langchain]"
            )
