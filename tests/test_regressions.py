"""Regression checks for structured JSON cells and async public discovery."""
import asyncio
import json
from datetime import date
from types import SimpleNamespace
import pytest

@pytest.mark.parametrize("query_name", ["pixeltable_query", "pixeltable_query_table"])
def test_nested_json_cells_keep_types(monkeypatch, query_name):
    from mcp_server_pixeltable_stio.core import tables
    value = {"nested": [1, True, None, {"date": date(2026, 9, 7)}]}
    class Query:
        def select(self): return self
        def collect(self): return [{"payload": value}]
    monkeypatch.setattr(tables, "ensure_pixeltable_available", lambda: None)
    monkeypatch.setattr(tables, "pxt", SimpleNamespace(get_table=lambda path: Query()))
    result = getattr(tables, query_name)("scratch.items")
    assert result["success"]
    assert json.loads(json.dumps(result))["data"] == [[{"nested": [1, True, None, {"date": "2026-09-07"}]}]]

def test_tools_resource_inside_event_loop():
    from mcp_server_pixeltable_stio.server import tools_resource, mcp
    async def check():
        result = json.loads(await tools_resource())
        assert result["success"]
        assert result["total_tools"] == len(await mcp.list_tools())
    asyncio.run(check())

def test_index_option_supports_both_sdk_signatures():
    from mcp_server_pixeltable_stio.core.tables import _index_kwargs
    def old(*, create_default_idxs=True): pass
    def new(*, has_default_idxs=False): pass
    assert _index_kwargs(old, False) == {"create_default_idxs": False}
    assert _index_kwargs(new, True) == {"has_default_idxs": True}
