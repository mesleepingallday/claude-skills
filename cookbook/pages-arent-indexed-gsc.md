# Pages aren't Indexed (GSC)

## Purpose

Extract all non-indexed pages from Google Search Console for a website and export them to a Google Sheet for analysis and action tracking. This helps identify pages that Google has discovered but not indexed, enabling SEO teams to take corrective action.

## Variables

SITE_URL: https://example.com/
GSC_SITE_FORMAT: https://www.example.com/ | sc-domain:example.com
GOOGLE_SHEETS_SPREADSHEET_ID: your_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: Pages aren't Indexed (GSC)
OUTPUT_SHEET_ID: numeric_sheet_id (for batch_update)

### Indexing Status Categories

NON_INDEXED_STATUSES:
  - "Discovered - currently not indexed"
  - "Crawled - currently not indexed"
  - "URL is unknown to Google"
  - "Excluded by 'noindex' tag"
  - "Blocked by robots.txt"

INDEXED_STATUSES:
  - "Submitted and indexed"

### Execution Configuration

BATCH_SIZE: 10 (max URLs per GSC API call)
PARALLEL_SITEMAP_FETCH: true

## Prerequisites

- Site verified in Google Search Console
- GSC MCP server configured with OAuth authentication
- Google Sheets MCP server configured
- Target Google Sheet with appropriate worksheet

## Instructions

- Before executing, verify site access: `mcp__gsc__list_properties()`
- Check site URL format matches GSC property exactly
- For sheets with special characters in names, use `batch_update` with sheet ID instead of sheet name

## Workflow

### 1. Verify GSC Access

```
mcp__gsc__list_properties()
```

Look for the target site and note the exact URL format (standard or domain property).

### 2. Get All Sitemaps

```
mcp__gsc__list_sitemaps_enhanced({
  site_url: "https://www.example.com/"
})
```

Note the sitemap URLs and total URL count.

### 3. Fetch All URLs from Sitemaps

For sitemap index files, fetch each child sitemap:

```
WebFetch({
  url: "https://www.example.com/sitemap.xml",
  prompt: "Extract all URLs from this sitemap XML. List each URL on a new line."
})
```

For sitemap indexes, also fetch:
- pages-sitemap.xml
- posts-sitemap.xml
- products-sitemap.xml
- etc.

### 4. Batch URL Inspection

Process URLs in batches of 10 (API limit):

```
mcp__gsc__batch_url_inspection({
  site_url: "https://www.example.com/",
  urls: "url1\nurl2\nurl3\n...url10"
})
```

### 5. Categorize Results

Parse inspection results and categorize:

| Status | Category | Action |
|--------|----------|--------|
| Submitted and indexed | INDEXED | None |
| Discovered - currently not indexed | NOT_INDEXED | Request indexing |
| Crawled - currently not indexed | NOT_INDEXED | Improve content quality |
| URL is unknown to Google | NOT_INDEXED | Submit sitemap / add internal links |

### 6. Export to Google Sheets

Use `batch_update` for sheets with special characters in names:

```
mcp__google-sheets__batch_update({
  spreadsheet_id: "your_spreadsheet_id",
  requests: [{
    "updateCells": {
      "range": {
        "sheetId": 336502875,
        "startRowIndex": 3,
        "startColumnIndex": 1
      },
      "rows": [
        {"values": [
          {"userEnteredValue": {"numberValue": 1}},
          {"userEnteredValue": {"stringValue": "https://example.com/page1"}},
          {"userEnteredValue": {"stringValue": "Discovered - currently not indexed"}},
          {"userEnteredValue": {"stringValue": "Action Required"}}
        ]},
        // ... more rows
      ],
      "fields": "userEnteredValue"
    }
  }]
})
```

## Output Format

| Column | Description |
|--------|-------------|
| NO. | Row number |
| URL | Full page URL |
| Reason | Indexing status from GSC |
| Status | Action Required / Resolved |

### Sample Output

| NO. | URL | Reason | Status |
|-----|-----|--------|--------|
| 1 | https://example.com/page1 | Discovered - currently not indexed | Action Required |
| 2 | https://example.com/page2 | Crawled - currently not indexed | Action Required |
| 3 | https://example.com/page3 | URL is unknown to Google | Action Required |

## Indexing Issue Breakdown

### Discovered - currently not indexed
- **Meaning**: Google knows the URL exists but hasn't crawled it yet
- **Cause**: Low priority, insufficient crawl budget, or weak internal linking
- **Fix**: Add internal links, request indexing via GSC, improve site structure

### Crawled - currently not indexed
- **Meaning**: Google crawled the page but decided not to index it
- **Cause**: Thin content, duplicate content, low quality, or cannibalization
- **Fix**: Improve content quality, add unique value, consolidate similar pages

### URL is unknown to Google
- **Meaning**: Google has never discovered this URL
- **Cause**: No internal links, not in sitemap, recently created
- **Fix**: Add to sitemap, create internal links, submit URL in GSC

## Tips

- Always verify the GSC property URL format before running (trailing slash matters)
- Process URLs in batches of 10 to avoid API quota issues
- For large sites (1000+ URLs), run in segments or use parallel agents
- Sheets with special characters (apostrophes, parentheses) require `batch_update` with numeric sheet ID
- Focus on high-priority pages first (landing pages, products) over blog posts
- Check Last Crawl date for "Crawled - not indexed" pages - older dates suggest deeper quality issues
- Cross-reference with search analytics to prioritize pages with existing impressions
- After fixing issues, wait 1-2 weeks and re-check status before requesting re-indexing

## Example Results Summary

### Site: nirahomes.com.au (134 URLs checked)

| Category | Count | Percentage |
|----------|-------|------------|
| Indexed | 75 | 56% |
| Discovered - not indexed | 43 | 32% |
| Crawled - not indexed | 14 | 10% |
| Unknown to Google | 2 | 1.5% |
| **Total Not Indexed** | **59** | **44%** |
