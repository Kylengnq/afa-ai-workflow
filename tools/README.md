# Free Corbis MCP shim (`free_corbis_mcp.py`)

A **$0, no-API-key** drop-in replacement for the Corbis MCP server. It exposes the
same Tier-1 tool *names* the AFA workflow skills call, backed by free public data
sources, so `/lit-review`, `/lit-search`, `/brainstorm`, `/idea`,
`/verify-citations`, and `/lit-landscape` work without a paid Corbis key.

## Why this exists

The Corbis cloud MCP requires a `corbis_mcp_` API key — every tool call is
authenticated and metered. Testing showed Corbis is essentially a wrapper over
**OpenAlex** (its paper IDs are OpenAlex `W…` IDs) plus **FRED** and proprietary
commercial-real-estate (CRE) data. The literature + macro half is fully
replaceable for free; only the CRE market tools have no open equivalent.

## What's backed by what

| Corbis tool | Free source | Status |
|---|---|---|
| `search_papers` | OpenAlex `/works` (keyless) | ✅ full |
| `get_paper_details` / `_batch` | OpenAlex `/works/{id\|doi}` | ✅ full (no `fullText`) |
| `top_cited_articles` | OpenAlex source-ID filter + citation sort | ✅ full |
| `search_datasets` | Curated free-dataset list | ✅ curated |
| `format_citation` / `export_citations` | Local BibTeX/APA formatter | ✅ full |
| `fred_search` | Curated keyword→series map | ✅ common series |
| `fred_series_batch` | FRED `fredgraph.csv` (keyless) | ✅ full |
| `find_academic_identity` | OpenAlex `/authors` | ✅ basic |
| `get_market_data`, `compare_markets`, `search_markets`, `get_national_macro`, `get_market_trends` | proprietary CRE data | ❌ returns a clear "unavailable" message |

## Differences from real Corbis

- **Relevance ranking** uses OpenAlex's ranking (not Corbis's semantic RRF), so
  result ordering can differ. `sortBy: "citedByCount"` re-ranks the topical
  result set by citations locally to surface seminal papers.
- **`fullText`** is not available (OpenAlex provides abstracts + metadata only).
  Use the `paper-reader` agent on a PDF when you need full text.
- **`fred_search`** matches against a curated map of common macro series. If you
  already know a FRED series ID, `fred_series_batch` fetches any series.
- **CRE market tools** are unavailable; skip CRE-specific steps or get a paid key.

## How it's wired

`.mcp.json` (and `.cursor/mcp.json`) point the `corbis` server at this script:

```json
{ "mcpServers": { "corbis": { "command": "python3", "args": ["tools/free_corbis_mcp.py"] } } }
```

No pip dependencies — pure Python standard library. Claude Code launches it
automatically when you run from the repo root.

## Switching back to the paid Corbis cloud

The original cloud config is saved as `.mcp.json.corbis-cloud`. To switch back:

```bash
cp .mcp.json.corbis-cloud .mcp.json
export CORBIS_MCP_API_KEY="corbis_mcp_..."
```

## Manual test

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_papers","arguments":{"query":"momentum stock returns","sortBy":"citedByCount","matchCount":3,"compact":true}}}' \
  | python3 tools/free_corbis_mcp.py
```
