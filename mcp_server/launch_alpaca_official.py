from __future__ import annotations

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Load .env from project root
    base_dir = Path(__file__).resolve().parents[1]
    env_path = base_dir / ".env"

    if env_path.exists():
        load_dotenv(env_path)
    else:
        print(f"[launch_alpaca_official] WARNING: No .env found at {env_path}", file=os.sys.stderr)

    # Merge .env variables with current environment
    env = os.environ.copy()

    # Command to run the official Alpaca MCP server
    cmd = ["uvx", "alpaca-mcp-server", "serve"]

    try:
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[launch_alpaca_official] ERROR: exited with code {e.returncode}", file=os.sys.stderr)

if __name__ == "__main__":
    main()
