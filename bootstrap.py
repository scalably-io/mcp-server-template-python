#!/usr/bin/env python3
"""Rename the example server. Usage: bootstrap.py <server> "<Title>" <prod-sha> <prod-date> <prod-path>
Example: bootstrap.py gsc-mcp "Google Search Console MCP" ef174fc3 2026-08-31 container/tools/gsc-mcp/server.py
The MCP protocol name and the install alias become <server> without a trailing "-mcp" (gsc-mcp -> gsc).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {".git", ".venv", "dist", "__pycache__", ".pytest_cache"}
server, title, sha, date, path = sys.argv[1:6]
module = "scalably_" + server.replace("-", "_")
short = server[:-4] if server.endswith("-mcp") else server
repl = {
    "scalably_example_mcp": module,
    "scalably-example-mcp": "scalably-" + server,
    "example-mcp": server,
    "Example MCP": title,
    'FastMCP("example")': f'FastMCP("{short}")',
    "mcp add example ": f"mcp add {short} ",
    "EXAMPLE_LOG_LEVEL": short.upper().replace("-", "_") + "_LOG_LEVEL",
    "(production commit sha, date, path) filled by bootstrap.py": f"`{path}` at `{sha}` ({date}) in the private ScalablyAI repository",
}
for p in ROOT.rglob("*"):
    if not p.is_file() or p.name == "bootstrap.py" or SKIP_DIRS & set(p.parts):
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    new = text
    for old, rep in repl.items():
        new = new.replace(old, rep)
    if new != text:
        p.write_text(new, encoding="utf-8")
src = ROOT / "src" / "scalably_example_mcp"
if src.exists():
    src.rename(ROOT / "src" / module)
print(f"renamed to {server} / scalably-{server} / {module} / protocol name {short}")
