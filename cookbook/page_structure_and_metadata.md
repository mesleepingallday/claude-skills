# Purpose

Extract SEO data from Screaming Frog CLI crawl or .csv file and then populate Google Sheets for auditing.

## Variables

GOOGLE_SHEETS_SPREADSHEET_ID: your_google_sheets_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: examle_worksheet_name
CSV_FILE_PATH?: /path/to/your/file.csv

INPUT_CELLS_RANGE: A1:A10
OUTPUT_CELLS_RANGE: B1:B10

PLAN_MODEL: opus 4.5
EXECUTE_MODEL: haiku 4.5
BASE_MODEL: sonnet 4.5
TEST_MODEL: haiku 4.5
MULTI_AGENTS_PARALLEL_EXECUTION: true
AGENTS_COUNT: 5
URLS_PER_AGENT: 25

PAGE_TYPE_CLASSIFICATION: false
PAGE_TYPE: ["Home Page", "Landing Page", "Location Page", "Trust Page", "Service Page", "Product Page", "Product Category", "Blog Post", "Blog Category", "Archive Page"]

FEATURED_IMAGE_EXISTENCE_CHECK: false
EXIST_VALUE: ["Exits", "Missing"]

INDEXABILITY: ["Indexable", "Non-Indexable"]
SCHEMA_MARKUP: ["Action Required", "No Action Required"]

## Prerequisites

- Screaming Frog `.seospider` crawl file
- OR: CSV file with Screaming Frog export data
- Google Sheet with "Page Structure & Metadata" tab
- Screaming Frog CLI at `C:\Users\haing\.claude\skills\seo-audit\tools\screaming-frog-cli\`
- google-sheets MCP configured
- pulse-fetch MCP configured

## Instructions

- Before executing with the MCP, run `claude mcp get <mcp-name>` to understand the mcp and its options.
  - EXAMPLE:
    - `claude mcp get google-sheets`
    - `claude mcp get pulse-fetch`
- Before executing with the CLI, ensure Screaming Frog CLI is installed and accessible at the specified path. If okay, run `ScreamingFrogSEOSpiderCli.exe --help` or `screamingfrogseospider --help` to understand available commands.
- For the -m (model) argument, use the defined models in the Variables section. If 'focus' is requested, use the BASE_MODEL.
- You can choose how many agents to run in parallel and how many URLs per agent based on your system capabilities., best for token optimization.
- If you are concerned about the execution workflow, propose a plan with PLAN_MODEL first.
- Always run with `MULTI_AGENTS_PARALLEL_EXECUTION` enabled for speed, run with `--dangerously-skip-permissions` in case you do not need to propose a plan.
- If you are concerned about the execution quality, run a small test first with 10 URLs before running the full execution.

## Workflow
1. IF NOT: CSV_FILE_PATH is provided
   - THEN: Execute Screaming Frog CLI to export crawl data as CSV.
### Step 1: Export from Screaming Frog CLI

```cmd
"C:\Users\haing\.claude\skills\seo-audit\tools\screaming-frog-cli\ScreamingFrogSEOSpiderCli.exe" ^
  --load-crawl "C:\Users\haing\clients\{client}.seospider" ^
  --headless ^
  --export-tabs "Internal:All" ^
  --output-folder "C:\Users\haing\temp" ^
  --export-format csv ^
  --overwrite
```

### Step 2: Parse CSV and Filter HTML Only

```python
import csv
import json

with open('C:/Users/haing/temp/internal_all.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    data = []
    for row in reader:
        if row.get('Content Type', '').startswith('text/html'):
            data.append({
                'url': row['Address'],
                'indexability': row['Indexability'],
                'title': row['Title 1'],
                'title_length': row['Title 1 Length'],
                'meta_desc': row['Meta Description 1'],
                'h1': row['H1-1']
            })

# Save filtered data
with open('C:/Users/haing/temp/seo_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
```

### Step 3: Write to Google Sheet

Use Google Sheets MCP to update columns:

| CSV Column         | Sheet Column | Description                |
| ------------------ | ------------ | -------------------------- |
| Address            | F            | URL                        |
| Title 1            | I            | Meta Title (Current)       |
| Title 1 Length     | J            | Meta Title Length          |
| Meta Description 1 | O            | Meta Description (Current) |
| H1-1               | S            | H1 (Current)               |
| Indexability       | E            | Indexable/Non-Indexable    |

### Step 4: Determine Page Types (Optional)

Use parallel Haiku agents with pulse-fetch MCP to classify pages:

**Page Type Categories:**

- Home Page
- Industry Page (`/industry/`)
- Module Page (`/module/`)
- Feature Page (`/feature/`)
- Segment Page (`/segment/`)
- Case Study (`/case-study/`)
- Blog Post (articles, news)
- Trust Page (about, privacy, terms, careers)
- Landing Page (product/marketing pages)
- Resource Page (downloads, guides)
- Contact Page (`/contact-us/`)
- Archive Page (listing pages)
- Utility Page (cdn-cgi, technical)

**Classification Logic:**

1. URL patterns (primary signal)
2. H1/Title keywords (secondary)
3. Content analysis via pulse-fetch (for ambiguous URLs)

Write page types to column D.

## Column Mapping Summary

| Sheet Column | Data Source                 | Start Row |
| ------------ | --------------------------- | --------- |
| D            | Page Type (via pulse-fetch) | D14       |
| E            | Indexability                | E14       |
| F            | URL (Address)               | F14       |
| I            | Meta Title (Title 1)        | I14       |
| J            | Title Length                | J14       |
| O            | Meta Description            | O14       |
| S            | H1                          | S14       |

## Tips

- Always filter for `Content Type: text/html` to exclude CSS, JS, images
- Use `encoding='utf-8-sig'` when reading CSV to handle BOM
- Process URLs in parallel batches (3 agents x 36 URLs) for speed
- URL patterns can classify ~50% of pages; use pulse-fetch for the rest
