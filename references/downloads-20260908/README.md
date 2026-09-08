# Downloads source intake, 2026-09-08

This directory belongs to the adopted Pixeltable MCP repository. Source snapshots retain original Apache licenses and exact bytes. They are reference implementations, not registered servers or replacement runtime packages. `provenance.json` binds original file locations, hashes, imported bytes and current-source comparisons.

## Developer snapshot

`developer-source/src/mcp_server_pixeltable_stio` is already represented by the live package. Byte-identical files are marked `IDENTICAL_EXISTING`. Historical differences are preserved here; current implementation has MCP v2 `MCPServer`/public asynchronous tool discovery, Pixeltable index-option compatibility and nested JSON type preservation. Replacing current files with this snapshot would undo those repairs. No missing developer capability was found in these differences.

## Multimodal capability integration work

`multimodal-source/servers` provides separate document, image, audio, video and generic SDK examples. None is automatically installed or launched by this import. Existing generic MCP primitives expose tables/views/query operations, while the domain setup/insert/query workflows below are additional reference implementations.

| Capability | Concrete source | Required implementation before registration |
|---|---|---|
| Documents | `doc-index/tools.py` setup/insert/query | Adapt FastMCP to installed MCP v2; validate namespace and bounded top_n; bind actual home/version; preserve source URI/hash and document chunk provenance; verify existing-view recovery without replacing tables. |
| Images | `image-index/tools.py` | Remove caller-supplied API key from tool arguments; resolve credentials server-side; retain source-image identity and bounded model work; test setup, restart discovery and query on actual accepted schema. |
| Audio | `audio-index/tools.py` | Adopt its existing-index recovery pattern, replace historical `get_view` with the installed table/view lookup, and validate partial pipelines; translate transcription/chunk schema to current version; server-side credentials, source/timestamp provenance and bounded user-initiated processing. |
| Video | `video-index/tools.py` | Preserve frame timestamp and source-video identity; move API key from request; bound frame/model work and query limit; validate iterator/schema compatibility before dispatch. |
| Generic SDK | `base-sdk/tools.py` | Do not register as supplied: line 65 uses `if_exists="replace"`; use fail-on-existing plus schema validation. Lines 115/150/200 evaluate input expressions and line 269 executes a function string; route expressions through existing governed query/REPL admission instead of exposing another unrestricted evaluator. Prefer existing typed primitives. |

Registering these historical tools unchanged would introduce destructive replacement, secret-bearing arguments and an incompatible MCP entrypoint. Their useful domain recipes are preserved as owned source, with the above concrete adaptation work outstanding. No Pixeltable table, home, credential or database was touched during intake.

Validation: all imported Python source parses without importing packages or invoking model/database work; copied source hashes match originals. Syntax validity does not prove MCP v2 or Pixeltable runtime compatibility.
