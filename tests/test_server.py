import asyncio, json, os, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from conftest import REPO

async def _run():
    params = StdioServerParameters(command=sys.executable, args=["-m", "scalably_example_mcp"],
                                   env={**os.environ, "PYTHONPATH": str(REPO / "src")})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()
            res = await s.call_tool("example_echo", {"text": "hi"})
            return [t.name for t in tools.tools], json.loads(next(c.text for c in res.content if c.type == "text"))

def test_stdio_lists_and_calls():
    names, reply = asyncio.run(_run())
    assert names == ["example_echo"]
    assert reply["status"] == "succeeded" and reply["result"]["text"] == "hi"

def test_fail_raises_plain_runtime_error():
    from scalably_example_mcp import server
    try:
        server._fail("api_error", "boom")
    except RuntimeError as e:
        assert str(e) == "api_error: boom"
    else:
        raise AssertionError("no error")
