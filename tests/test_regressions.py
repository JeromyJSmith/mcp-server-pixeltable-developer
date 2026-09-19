"""Regression checks carried forward to the 0.2 architecture.

The 0.1-era versions of these tests targeted `mcp_server_pixeltable_stio.core`, which the upstream 0.2
rewrite (303202c) removed; since the 0.2 merge (b0b2ebb) they could not import. Ported 2026-09-19:
- nested JSON cells keep their types: in 0.2, pixeltable_rows relays `pxt rows --json` output, so the
  contract is that the tool returns those rows unchanged (no stringifying or flattening).
- tools listing inside a running event loop: covered by test_contract.py (async Client.list_tools).
- the index option: pixeltable>=0.7.8 has only `has_default_idxs`, covered by
  test_pixeltable_integration.py; the old `create_default_idxs` signature no longer exists to support.
"""

from __future__ import annotations

from typing import Any

import pytest
from mcp import Client

from mcp_server_pixeltable_developer.runtime import ProcessResult, ServerConfig
from mcp_server_pixeltable_developer.server import create_server

NESTED = {"nested": [1, True, None, {"date": "2026-09-07", "depth": {"n": 2.5}}], "tags": ["a", "b"]}


@pytest.mark.asyncio
async def test_rows_tool_returns_nested_json_cells_unchanged(
    server_config: ServerConfig,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_pxt(self: object, arguments: list[str], *args: Any, **kwargs: Any) -> ProcessResult:
        assert arguments[:2] == ["rows", "demo/docs"] and "--json" in arguments
        return ProcessResult(exit_code=0, stdout="", stderr="", data=[{"doc_id": 1, "payload": NESTED}])

    monkeypatch.setattr("mcp_server_pixeltable_developer.runtime.CommandRunner.pxt", fake_pxt)
    async with Client(create_server(server_config), raise_exceptions=False) as client:
        result = await client.call_tool("pixeltable_rows", {"path": "demo/docs", "limit": 1})
    assert result.is_error is False, result.content
    rows = result.structured_content["rows"]
    assert rows == [{"doc_id": 1, "payload": NESTED}]
    payload = rows[0]["payload"]
    assert payload["nested"][1] is True and payload["nested"][2] is None
    assert isinstance(payload["nested"][0], int) and isinstance(payload["nested"][3]["depth"]["n"], float)
