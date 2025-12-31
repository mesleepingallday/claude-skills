# Purpose

Extract SEO data from Screaming Frog CLI crawl or .csv file and then populate Google Sheets for auditing.

## Variables

CLIENT_SITE_URL: https://example.com
GOOGLE_SHEETS_SPREADSHEET_URL: https://docs.google.com/spreadsheets/d/your_google_sheets_spreadsheet_id/edit#gid=0
GOOGLE_SHEETS_SPREADSHEET_ID: your_google_sheets_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: examle_worksheet_name
CSV_FILE_PATH?: /path/to/your/file.csv

INPUT_CELLS_RANGE: A1:A10
OUTPUT_CELLS_RANGE: B1:B10
SORT_OUTPUT_URLS_BY_PAGE_TYPE_ORDER: ["Home Page", "Landing Page", "Location Page", "Trust Page", "Service Page", "Product Page", "Product Category", "Blog Post", "Blog Category", "Archive Page", "Other"]

META_TITLE_CHECK: false
META_DESCRIPTION_CHECK: false
PAGE_TYPE_CLASSIFICATION: false
PAGE_TYPE: ["Home Page", "Landing Page", "Location Page", "Trust Page", "Service Page", "Product Page", "Product Category", "Blog Post", "Blog Category", "Archive Page"]

FEATURED_IMAGE_CHECK: false
EXIST_VALUE: ["Exists", "Missing"]

SCHEMA_MARKUP_CHECK: false
SCHEMA_MARKUP: ["Action Required", "No Action Required"]
INDEXABILITY: ["Indexable", "Non-Indexable"]

PLAN_MODEL: opus 4.5
EXECUTE_MODEL: haiku 4.5
BASE_MODEL: sonnet 4.5
TEST_MODEL: haiku 4.5
MULTI_AGENTS_PARALLEL_EXECUTION: true
AGENTS_COUNT: 5
URLS_PER_AGENT: 25

## Subworkflows

Each subworkflow can be triggered directly or as part of the full audit.

### Featured Image Check

- TRIGGER: User mentions featured images, og:image, or social share images
- EXECUTE: [featured-image-check.md](./subworkflows/featured-image-check.md)
- EXAMPLE:
  - "Check if featured images exist"
  - "Check og:image meta tags"
  - "Are there featured images on these pages?"
  - "Audit featured images"
  - "Check Open Graph images"
  - "featured images column"
  - "Do these pages have social share images?"

### Meta Title Check & Meta Description Check

- TRIGGER: User mentions meta titles, title tags, SEO titles or meta descriptions or metadata
- EXECUTE: [meta-data.md](./subworkflows/meta-data.md)
- EXAMPLE:
  - "Check meta titles"
  - "Check meta descriptions"
  - "Are meta titles optimized?"
  - "Audit meta descriptions"
  - "Check SEO titles"
  - "Audit title tags"

### Schema Markup Check (coming soon)

- TRIGGER: User mentions schema, structured data, JSON-LD
- EXECUTE: schema-markup-check.md

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
- For the -f (full) argument, set [*]\_CHECK variables to true.
- You can choose how many agents to run in parallel and how many URLs per agent based on your system capabilities., best for token optimization.
- If you are concerned about the execution workflow, propose a plan with PLAN_MODEL first.
- Always run with `MULTI_AGENTS_PARALLEL_EXECUTION` enabled for speed, run with `--dangerously-skip-permissions` in case you do not need to propose a plan.
- If you are concerned about the execution quality, run a small test first with 10 URLs before running the full execution.

## Workflow

1. IF: CSV_FILE_PATH is provided in the user's request
   - THEN: Skip to Step 2.

- IF NOT IF: CLIENT_SITE_URL is provided in the user's request.
  - THEN: Execute Screaming Frog CLI to crawl CLIENT_SITE_URL and export crawl data as CSV.
  - IF NOT: Ask user to provide CLIENT_SITE_URL AND: Execute Screaming Frog CLI to crawl CLIENT_SITE_URL and export crawl data as CSV.

2. **Populate URLs to Google Sheets**

   - Connect to GOOGLE_SHEETS_SPREADSHEET_URL via google-sheets MCP
   - Write URLs to INPUT_CELLS_RANGE
   - Sort by SORT_OUTPUT_URLS_BY_PAGE_TYPE_ORDER if PAGE_TYPE_CLASSIFICATION enabled

3. **Execute Enabled Checks**

   - IF FEATURED_IMAGE_CHECK = true:
     - Run [Featured Image Check](./subworkflows/featured-image-check.md) subworkflow
   - IF META_TITLE_CHECK = true:
     - Check meta title presence and length
   - IF META_DESCRIPTION_CHECK = true:
     - Check meta description presence and length
   - IF SCHEMA_MARKUP_CHECK = true:
     - Check schema.org markup

4. **Write Results & Report**
   - Write check results to OUTPUT_CELLS_RANGE columns
   - Generate summary report: X URLs processed, Y passed, Z failed

## Tips

- Always filter for `Content Type: text/html` to exclude CSS, JS, images
- Use `encoding='utf-8-sig'` when reading CSV to handle BOM
- Process URLs in parallel batches (3 agents x 36 URLs) for speed
- URL patterns can classify ~50% of pages; use pulse-fetch for the rest
