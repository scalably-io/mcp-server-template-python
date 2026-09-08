#!/usr/bin/env python3
"""Rename the example server. Usage: bootstrap.py <server> "<Title>" <prod-sha> <prod-date> <prod-path>
Example: bootstrap.py gsc-mcp "Google Search Console MCP" ef174fc3 2026-08-31 container/tools/gsc-mcp/server.py
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
server, title, sha, date, path = sys.argv[1:6]
module = "scalably_" + server.replace("-", "_")
repl = {
    "scalably_example_mcp": module,
    "scalably-example-mcp": "scalably-" + server,
    "example-mcp": server,
    "Example MCP": title,
    "example_echo": "example_echo",
}
for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts and p.name != "bootstrap.py":
        text = p.read_text(encoding="utf-8")
        for old, new in repl.items():
            text = text.replace(old, new)
        text = text.replace("(production commit sha, date, path) filled by bootstrap.py", f"`{path}` at `{sha}` ({date}) in the private ScalablyAI repository")
        p.write_text(text, encoding="utf-8")
src = ROOT / "src" / "scalably_example_mcp"
if src.exists():
    src.rename(ROOT / "src" / module)
print(f"renamed to {server} / scalably-{server} / {module}")
