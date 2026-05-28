# Data Access

Every data source the project touched, with access windows. Reviewers will use
this to judge whether the AI workflow could in principle be reproduced.

## Data sources

| Source | Type | Access method | Credentials scope | First accessed | Last accessed |
|---|---|---|---|---|---|

## Data access at initial prompt

Record what the AI system could access when the investigation began.

| Item | Value |
|---|---|
| Files attached to initial prompt |  |
| APIs or MCP servers enabled at initial prompt |  |
| Credentials available to AI at initial prompt |  |
| Data sources intentionally withheld from AI |  |
| Human-only data access tasks, if any |  |

## Notes on access

For each source list:
- What the AI was permitted to do (read only, query budget, write back).
- Whether the AI accessed the source directly via tools, or whether the human
  pulled data and handed files to the agent.
- Any credentials that were proxied or wrapped (e.g., `.pgpass`, environment
  variables, OAuth tokens).

## Data files produced

If the project produced intermediate data files (parquet, csv, etc.), list the
paths in the repo and the source query or script that built them. Link to the
relevant conversation in `conversations/` where the AI produced the extraction
script.

## Licensing

Note the license for each source and confirm that the submission can include or
reference the data without violating its terms.

## Reproducibility limits

Document any limits a reviewer should know: proprietary data that cannot be
redistributed, credentials that expire, API rate limits, query windows, or data
versions that may change after the submission deadline.

## Example rows

These examples are illustrative. Do not leave them as project records.

- `| Corbis | literature | MCP HTTP | personal API key | 2026-06-01 | 2026-08-31 |`
- `| WRDS / CRSP | market | PostgreSQL via SSH | institutional | 2026-06-10 | 2026-07-15 |`
- `| FRED | macro | REST API | public | 2026-06-10 | 2026-07-15 |`
