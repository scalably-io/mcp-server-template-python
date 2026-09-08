"""Example MCP server. One tool, the reply and failure conventions every Scalably server uses."""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("example")
LOGGER = logging.getLogger(__name__)


def _reply(status: str, operation: str, summary: str, *, result: Any = None, proof: dict | None = None,
           warnings: list[str] | None = None, recovery: dict | None = None) -> str:
    """Plain JSON reply. status is one of succeeded, partial, no_op."""
    return json.dumps({"status": status, "operation": operation, "summary": summary, "result": result,
                       "proof": proof, "warnings": warnings or [], "recovery": recovery}, indent=2)


def _fail(code: str, message: str) -> None:
    """Raise a plain error; the MCP layer reports it as a tool error."""
    raise RuntimeError(f"{code}: {message}")


@mcp.tool(annotations=ToolAnnotations(title="Echo text", readOnlyHint=True, openWorldHint=False))
def example_echo(text: str) -> str:
    """Return the text you pass in. Replace with real tools."""
    if not text:
        _fail("invalid_argument", "text must not be empty")
    return _reply("succeeded", "example_echo", "Echoed the text.", result={"text": text}, proof={"complete": True})


def main() -> None:
    level = os.environ.get("EXAMPLE_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format="%(asctime)s %(levelname)s example-mcp %(message)s")
    mcp.run()


if __name__ == "__main__":
    main()
