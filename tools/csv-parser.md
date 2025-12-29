# CSV Parser Tool

Parse Screaming Frog CSV exports for SEO audit workflows.

## Location

```
C:\Users\haing\.claude\skills\seo-audit\tools\scripts\csv_parser.py
```

## Usage

```bash
python csv_parser.py --csv FILE [options]
```

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--csv` | Yes | - | Path to CSV file |
| `--columns` | No | SEO defaults | Comma-separated column names |
| `--filter` | No | - | Filter rows (repeatable) |
| `--filter-html` | No | False | Filter `Content Type: text/html` |
| `--output` | No | stdout | Output file path |
| `--preview` | No | False | Show first 10 rows only |
| `--format` | No | `json` | Output: json, csv, sheets |
| `--stats-only` | No | False | Output only stats (row count) - NO DATA |
| `--chunk-size` | No | 1000 | Rows per chunk |
| `--chunk-index` | No | - | Output only this chunk (1-indexed) |

## Filter Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `Column:value` | Exact match | `Status Code:200` |
| `Column:contains:value` | Contains | `Content Type:contains:text/html` |
| `Column:startswith:value` | Starts with | `Address:startswith:https://` |
| `Column:gt:value` | Greater than | `Word Count:gt:100` |
| `Column:lt:value` | Less than | `Crawl Depth:lt:3` |

## Default SEO Columns

- Address, Content Type, Status Code, Status
- Indexability, Indexability Status
- Title 1, Title 1 Length
- Meta Description 1, Meta Description 1 Length
- H1-1, Word Count, Crawl Depth, Inlinks
- Canonical Link Element 1

## Examples

### Basic: Parse with HTML filter
```bash
python csv_parser.py --csv internal_all.csv --filter-html
```

### Select specific columns
```bash
python csv_parser.py --csv internal_all.csv \
    --columns "Address,Title 1,Meta Description 1,H1-1"
```

### Multiple filters (AND logic)
```bash
python csv_parser.py --csv internal_all.csv \
    --filter "Status Code:200" \
    --filter "Indexability:Indexable"
```

### Preview first 10 rows
```bash
python csv_parser.py --csv internal_all.csv --filter-html --preview
```

### Output for Google Sheets MCP
```bash
python csv_parser.py --csv internal_all.csv --filter-html --format sheets
```

### Save to file
```bash
python csv_parser.py --csv internal_all.csv --filter-html --output data.json
```

## Output Formats

### JSON (default)
```json
{
  "headers": ["Address", "Title 1", ...],
  "data": [["https://...", "Page Title", ...], ...],
  "stats": {"total_rows": 1234, "columns": 15}
}
```

### Sheets (for Google Sheets MCP)
```json
[
  ["Address", "Title 1", ...],
  ["https://...", "Page Title", ...],
  ...
]
```

## Integration with Google Sheets MCP

1. Parse CSV:
```bash
python csv_parser.py --csv internal_all.csv --filter-html --format sheets > data.json
```

2. Upload via MCP:
```
mcp__google-sheets__update_cells(
  spreadsheet_id="...",
  sheet="Sheet1",
  range="A1",
  data=<parsed JSON>
)
```

## Token-Efficient Chunking (for 15K+ rows)

When processing large datasets, use chunking to avoid context overflow:

### Step 1: Get Stats Only (NO DATA)
```bash
python csv_parser.py --csv internal_all.csv --filter-html --stats-only
# Output: {"total_rows": 6472, "chunk_size": 1000, "chunk_count": 7}
```

### Step 2: Process Chunks in Parallel Agents
```bash
# Agent 1:
python csv_parser.py --csv internal_all.csv --filter-html \
    --columns "Address,Title 1,Meta Description 1,H1-1" \
    --chunk-index 1 --chunk-size 1000 --format sheets

# Agent 2:
python csv_parser.py --csv internal_all.csv --filter-html \
    --columns "Address,Title 1,Meta Description 1,H1-1" \
    --chunk-index 2 --chunk-size 1000 --format sheets
# ... etc
```

### Token Savings

| Approach | Tokens | Savings |
|----------|--------|---------|
| Load all data | ~14.5M | - |
| Chunked (stats + agents) | ~4K | **99.97%** |

**Key Rules:**
- Agent prompts contain ONLY file path + chunk index, NOT data
- Agents return status only: `{"status": "done", "rows": 1000}`
- File I/O doesn't count as tokens

## Notes

- Uses `utf-8-sig` encoding to handle BOM from Screaming Frog exports
- Progress messages go to stderr, data to stdout
- Empty cells are replaced with empty strings
- `--stats-only` and `--chunk-index` are designed for multi-agent workflows
