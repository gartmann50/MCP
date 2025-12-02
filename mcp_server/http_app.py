from __future__ import annotations

from mcp_server.core import mcp

# ASGI app exposing the MCP server over Streamable HTTP.
# You can serve this with uvicorn / gunicorn.
app = mcp.streamable_http_app()
