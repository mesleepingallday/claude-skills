# Purpose

Check if URLs have a featured image by detecting the `og:image` meta tag, then populate results to Google Sheets.

## Variables

GOOGLE_SHEETS_SPREADSHEET_URL: https://docs.google.com/spreadsheets/d/your_google_sheets_spreadsheet_id/edit#gid=0
GOOGLE_SHEETS_SPREADSHEET_ID: your_google_sheets_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: Page Structure & Metadata

HEADER_ROW: 12:13
DATA_START_ROW: 14
INPUT_COLUMN_HEADER: URL
INPUT_CELLS_RANGE: F14:F (default, auto-detected from header)
OUTPUT_COLUMN_HEADER: Featured Images
OUTPUT_CELLS_RANGE: V14:V (default, auto-detected from header)

EXIST_VALUE: ["Exists", "Missing"]

### pulse-fetch Configuration (CRITICAL)

PULSE_FETCH_CLEAN_SCRAPE: false
PULSE_FETCH_MAX_CHARS: 3000
PULSE_FETCH_RESULT_HANDLING: returnOnly
PULSE_FETCH_TIMEOUT: 60000

### Execution Configuration

EXECUTE_MODEL: haiku 4.5
MULTI_AGENTS_PARALLEL_EXECUTION: true
AGENTS_COUNT: 5
URLS_PER_AGENT: 25

## Prerequisites

- Google Sheet with "Page Structure & Metadata" worksheet
- URLs populated in the URL column
- google-sheets MCP configured
- pulse-fetch MCP configured

## Instructions

- Before executing with MCP, run `claude mcp get <mcp-name>` to understand the MCP and its options.
  - EXAMPLE:
    - `claude mcp get google-sheets`
    - `claude mcp get pulse-fetch`
- For the -m (model) argument, use EXECUTE_MODEL (haiku 4.5) for speed and cost efficiency.
- Always run with `MULTI_AGENTS_PARALLEL_EXECUTION` enabled for speed.
- Run with `--dangerously-skip-permissions` if you do not need to propose a plan.
- If concerned about execution quality, run a small test first with 10 URLs before running full execution.

## Workflow

1. **Access Google Sheets**

   - Use google-sheets MCP to connect to GOOGLE_SHEETS_SPREADSHEET_URL
   - Navigate to worksheet: GOOGLE_SHEETS_WORKSHEET_NAME

2. **Find Column Headers (Dynamic Detection)**

   - Read HEADER_ROW (row 13) to find column positions
   - Search for cell containing "URL" → get column letter (e.g., F)
   - Search for cell containing "Featured Images" → get column letter (e.g., V)
   - IF headers not found → fall back to defaults (F for URL, V for Featured Images)
   - Data starts at DATA_START_ROW (row 14)

3. **Read URLs**

   - Read all URLs from detected URL column starting at DATA_START_ROW
   - Filter out empty cells
   - Count total URLs to process

4. **Check Featured Images**

   Choose one of the following methods:

   ### Method A: Direct pulse-fetch (Recommended for Reliability)

   - Process URLs in batches of 5 parallel pulse-fetch calls
   - For each URL, call `mcp__pulse-fetch__scrape` with:
     ```
     url: <target_url>
     cleanScrape: false     # CRITICAL - preserves og:image meta tags
     maxChars: 3000         # Enough to capture <head> section
     resultHandling: returnOnly
     ```
   - Parse response HTML for `<meta property="og:image" content="...">` tag
   - IF og:image tag exists with non-empty content → "Exists"
   - IF og:image tag missing or empty → "Missing"

   ### Method B: Parallel Task Agents (Faster but May Fail)

   - Divide URLs into batches (URLS_PER_AGENT per agent)
   - For each URL batch, spawn a haiku agent with prompt:
     ```
     Check if these URLs have og:image meta tags.
     Use mcp__pulse-fetch__scrape with cleanScrape: false, maxChars: 3000.
     Return JSON array: [{"url": "...", "status": "Exists" or "Missing"}]
     ```
   - Collect results from all agents

5. **Write Results**

   - Use google-sheets MCP to write results to detected Featured Images column
   - Write "Exists" or "Missing" for each corresponding URL row
   - Maintain row alignment with source URLs

6. **Verify**
   - Confirm all results written successfully
   - Report summary: X URLs processed, Y with images, Z missing

## Critical Configuration Notes

### Why cleanScrape: false is REQUIRED

By default, pulse-fetch uses `cleanScrape: true` which:
- Converts HTML to semantic markdown
- **Removes the `<head>` section** where og:image meta tags reside
- Results in og:image never being detected

Setting `cleanScrape: false`:
- Returns raw HTML
- Preserves all meta tags in `<head>`
- Allows accurate og:image detection

### pulse-fetch Call Example

```javascript
mcp__pulse-fetch__scrape({
  url: "https://example.com/page",
  cleanScrape: false,      // CRITICAL
  maxChars: 3000,          // Head section is usually < 2000 chars
  resultHandling: "returnOnly"
})
```

### Detecting og:image in Response

Look for this pattern in the raw HTML response:
```html
<meta property="og:image" content="https://..." />
```

Also check for alternatives:
- `<meta property="og:image:url" content="..." />`
- `<meta property="og:image:secure_url" content="..." />`

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| og:image never detected | `cleanScrape: true` (default) | Set `cleanScrape: false` |
| "Prompt is too long" error | Too many URLs per agent | Reduce URLS_PER_AGENT to 10-15 |
| Timeout errors | Slow page loading | Increase timeout or reduce batch size |
| Task agent can't detect og:image | Agent using cleaned HTML | Use Method A (direct pulse-fetch) |
| Empty response | URL blocked or 404 | Mark as "Missing" with note |

## Tips

- **ALWAYS use `cleanScrape: false`** to preserve meta tags in `<head>`
- Test with 1 URL first to verify pulse-fetch configuration works
- The og:image tag is in `<head>`: `<meta property="og:image" content="https://...">`
- Some sites use `og:image:url` as an alternative - check both if needed
- Handle timeout/error cases by marking as "Missing" with a note
- For large datasets (500+ URLs), use Method A with batches of 5 parallel calls
- For very large datasets, consider running in multiple sessions to avoid rate limits

## Learning Curve (Updated: 2025-12-31)

Lessons learned from real workflow execution on 156 URLs:

### Optimal Execution Strategy

1. **Hybrid Approach Works Best**
   - Start with direct pulse-fetch for first 10-15 URLs (validates configuration)
   - Then launch 3 parallel Task agents with haiku model for remaining URLs
   - Each agent handles 35-50 URLs efficiently

2. **Recommended Agent Configuration**
   ```
   AGENTS_COUNT: 3
   URLS_PER_AGENT: 35-50
   MODEL: haiku (fast, cost-effective)
   ```

3. **Processing Time**
   - 156 URLs completed in ~5 minutes using hybrid approach
   - Direct pulse-fetch: ~5 URLs per batch (parallel)
   - Task agents: 3 agents processing 35-50 URLs each in parallel

### Common URL Patterns & Expected Results

| URL Type | Typical Result | Notes |
|----------|---------------|-------|
| Home page | Exists | Usually has og:image set |
| Landing pages | Mixed | Depends on SEO setup |
| Blog posts/Articles | Exists | Most CMS auto-generate from featured image |
| Portfolio items | Exists | Gallery pages often have og:image |
| Date archives (/YYYY/MM/) | Missing | WordPress date archives rarely have og:image |
| Category/Tag pages | Missing | Archive pages typically lack og:image |
| Pagination pages (?page=2) | Missing | Pagination inherits parent's missing og:image |
| Thank you/Landing forms | Missing | Utility pages often overlooked |
| CSS/JS files | Error/Missing | Non-HTML URLs return 404 or empty |
| Test/Sample pages | Missing | Development pages usually lack og:image |

### Error Handling

1. **Non-HTML URLs** (CSS, JS, images)
   - Will return 404 or empty response
   - Mark as "Missing" in results
   - Consider filtering these out before processing

2. **Timeout Errors**
   - Increase timeout for slow sites
   - Default 60000ms (1 minute) is usually sufficient
   - For slow sites, use 120000ms (2 minutes)

3. **Rate Limiting**
   - If processing 500+ URLs, add delays between batches
   - Consider breaking into multiple sessions

### Spreadsheet Update Tips

1. **Column Detection**
   - Featured Images column may vary (S, T, V depending on sheet structure)
   - Always verify header row position before bulk updates
   - Use `get_sheet_data` to confirm column layout

2. **Data Alignment**
   - Ensure results array matches exact row count
   - Missing alignment causes data shift errors
   - Count URLs before and after processing to verify

### Real-World Results Distribution

From 156 URL audit:
- **~40% Exists** (62 URLs with og:image)
- **~60% Missing** (94 URLs without og:image)

Most missing og:image pages were:
- Date archive pages (all missing)
- Category/pagination pages (all missing)
- Utility pages (thank you, forms, maintenance)
- Test/development pages
