# Data Access

Every data source the project touched, with access windows. Reviewers will use
this to judge whether the AI workflow could in principle be reproduced.

## Data sources

| Source | Type | Access method | Credentials scope | First accessed | Last accessed |
|---|---|---|---|---|---|
| e.g., Corbis | literature | MCP HTTP | personal API key | YYYY-MM-DD | YYYY-MM-DD |
| e.g., WRDS / CRSP | market | PostgreSQL via SSH | institutional | YYYY-MM-DD | YYYY-MM-DD |
| e.g., FRED | macro | REST API | public | YYYY-MM-DD | YYYY-MM-DD |
|  |  |  |  |  |  |

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
