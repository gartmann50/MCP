from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env if present (for local dev)
load_dotenv()

# Create MCP server instance
mcp = FastMCP("gartmann-mcp", json_response=True)

# --------------------------------------------------------------------
# Basic sanity-check tool
# --------------------------------------------------------------------


@mcp.tool()
def ping(message: str = "hello") -> str:
    """
    Simple health-check tool.

    Use this from Claude first to make sure the server is wired correctly.
    """
    return f"pong: {message}"


# --------------------------------------------------------------------
# Alpaca tools (read-only skeleton)
# --------------------------------------------------------------------

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")


def _alpaca_headers() -> dict[str, str]:
    """
    Build Alpaca auth headers, or raise if keys are missing.
    """
    if not ALPACA_API_KEY or not ALPACA_SECRET_KEY:
        raise RuntimeError(
            "ALPACA_API_KEY and ALPACA_SECRET_KEY must be set in environment."
        )
    return {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY,
        "Accept": "application/json",
    }


@mcp.tool()
async def alpaca_get_account() -> dict[str, Any]:
    """
    Get Alpaca account information.

    NOTE: This only reads data. No orders are placed by this tool.
    """
    url = f"{ALPACA_BASE_URL}/v2/account"
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, headers=_alpaca_headers())
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def alpaca_list_positions() -> list[dict[str, Any]]:
    """
    List current Alpaca positions.
    """
    url = f"{ALPACA_BASE_URL}/v2/positions"
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, headers=_alpaca_headers())
        resp.raise_for_status()
        return resp.json()


# --------------------------------------------------------------------
# Polygon tools (read-only skeleton)
# --------------------------------------------------------------------

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
POLYGON_BASE_URL = os.getenv("POLYGON_BASE_URL", "https://api.polygon.io")


def _polygon_params(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Base Polygon query params including the API key.
    """
    if not POLYGON_API_KEY:
        raise RuntimeError("POLYGON_API_KEY must be set in environment.")
    params: dict[str, Any] = {"apiKey": POLYGON_API_KEY}
    if extra:
        params.update(extra)
    return params


@mcp.tool()
async def polygon_last_trade(symbol: str) -> dict[str, Any]:
    """
    Get last trade for a symbol from Polygon.

    Example symbol: AAPL, TSLA, SPY
    """
    url = f"{POLYGON_BASE_URL}/v2/last/trade/{symbol.upper()}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params=_polygon_params())
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def polygon_daily_ohlc(symbol: str, date: str) -> dict[str, Any]:
    """
    Get daily OHLC data for a symbol on a given date.

    date format: YYYY-MM-DD
    """
    url = f"{POLYGON_BASE_URL}/v1/open-close/{symbol.upper()}/{date}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params=_polygon_params())
        resp.raise_for_status()
        return resp.json()
