from __future__ import annotations

from mcp_server.core import mcp


if __name__ == "__main__":
    # Run the MCP server over STDIO.
    # This is what Claude Desktop / Claude Code connects to.
    mcp.run(transport="stdio")
