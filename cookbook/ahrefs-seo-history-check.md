# Ahrefs SEO History Check

## Purpose

Fetch comprehensive SEO metrics from Ahrefs for a domain and update a Google Sheet with current Domain Rating (DR), URL Rating (UR), Backlinks, Referring Domains, Total Keywords, and Organic Traffic. This provides a historical snapshot of the site's SEO performance and authority metrics.

## Variables

CLIENT_SITE_URL: https://www.example.com/
GOOGLE_SHEETS_SPREADSHEET_ID: your_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: SEO History Check
SEO_HISTORY_CHECK_SHEET_ID: numeric_sheet_id

## Prerequisites

- Ahrefs MCP server configured with API access
- Google Sheets MCP server configured with read/write permissions
- Target Google Sheet with "SEO History Check" worksheet
- Existing metric rows in the sheet (Domain Rating, URL Rating, Backlinks, Ref. Domains, Total Keywords, Organic Traffic)

## Instructions

- Before executing, verify the Google Sheet structure matches expected layout
- The "Overview" column should be prepared to receive metric values
- Ensure Ahrefs API quota is available (batch-analysis endpoint uses 1 API call)

## Workflow

### 1. Fetch Ahrefs Data (Single API Call)

Use the batch-analysis endpoint to fetch all metrics at once:

```
mcp__ahrefs__batch-analysis-batch-analysis({
  select: [
    "domain_rating",
    "url_rating",
    "backlinks",
    "refdomains",
    "org_keywords",
    "paid_keywords",
    "org_traffic"
  ],
  targets: [{
    url: "https://www.example.com",
    mode: "subdomains",
    protocol: "both"
  }]
})
```

**Response example:**
```json
{
  "targets": [{
    "domain_rating": 27.0,
    "url_rating": 9.0,
    "backlinks": 1561,
    "refdomains": 94,
    "org_keywords": 189,
    "paid_keywords": 5,
    "org_traffic": 1789
  }]
}
```

### 2. Read Google Sheet Structure

```
mcp__google-sheets__get_sheet_data({
  spreadsheet_id: "your_spreadsheet_id",
  sheet: "SEO History Check"
})
```

Identify the row numbers for each metric:
- Domain Rating (DR)
- URL Rating (UR)
- Backlinks
- Ref. Domains
- Total Keywords
- Organic Traffic

Determine the column letter for "Overview" values.

### 3. Process API Response

Extract metrics from Ahrefs response:
- `domain_rating` → Domain Rating
- `url_rating` → URL Rating
- `backlinks` → Backlinks
- `refdomains` → Ref. Domains
- `org_keywords + paid_keywords` → Total Keywords (calculated)
- `org_traffic` → Organic Traffic

### 4. Update Google Sheet

Write metrics to the Overview column:

```
mcp__google-sheets__batch_update_cells({
  spreadsheet_id: "your_spreadsheet_id",
  sheet: "SEO History Check",
  ranges: {
    "D5": [[27]],           // Domain Rating
    "D6": [[9]],            // URL Rating
    "D7": [[1561]],         // Backlinks
    "D8": [[94]],           // Ref. Domains
    "D12": [[194]],         // Total Keywords
    "D13": [[1789]]         // Organic Traffic
  }
})
```

## Output Format

The sheet is updated with current metrics in the Overview column:

| Metric | Overview | Description | Status |
|--------|----------|-------------|--------|
| Domain Rating (DR) | 27 | Backlink profile strength (0-100) | Action Required |
| URL Rating (UR) | 9 | Page backlink strength (0-100) | Action Required |
| Backlinks | 1,561 | Total external links to site | - |
| Ref. Domains | 94 | Unique domains linking to site | Action Required |
| Total Keywords | 194 | Organic (189) + Paid (5) keywords | No Action Required |
| Organic Traffic | 1,789 | Monthly organic visitors | No Action Required |

## Metric Explanations

### Domain Rating (DR)
- **Range**: 0-100 (logarithmic scale)
- **Meaning**: Strength of a domain's backlink profile compared to competitors
- **Action**: DR < 30 indicates weak authority; focus on high-quality backlinks

### URL Rating (UR)
- **Range**: 0-100 (logarithmic scale)
- **Meaning**: Strength of a specific page's backlink profile
- **Action**: UR < 20 suggests the page needs more internal/external links

### Backlinks
- **Meaning**: Total number of external links pointing to the domain
- **Action**: Low backlink count (< 500) suggests limited external validation

### Referring Domains
- **Meaning**: Number of unique domains with at least one link to your site
- **Action**: Aim for diverse referrer base; < 50 domains is typically low

### Total Keywords
- **Meaning**: Combined count of organic and paid keywords ranking
- **Action**: < 100 keywords suggests limited SERP coverage

### Organic Traffic
- **Meaning**: Estimated monthly visitors from organic search
- **Action**: Traffic lower than expected may indicate content/technical issues

## Tips

- Run this workflow monthly or quarterly to track SEO progress over time
- Compare results month-over-month to identify trends
- For sites with subdomains, mode "subdomains" includes all of them
- Use protocol "both" to capture http and https variants
- The batch-analysis endpoint is efficient and returns all metrics in one call
- After improving backlinks, expect 4-8 weeks for metric changes to reflect
- Pair this with content and technical SEO improvements for better results

## Common Issues & Solutions

### Low Domain Rating
- **Cause**: Insufficient quantity/quality of backlinks
- **Solution**: Build links from authoritative, relevant sites through content marketing and outreach

### Low URL Rating on Key Pages
- **Cause**: Pages not receiving enough internal/external links
- **Solution**: Internal linking strategy + targeted link building campaigns

### High Backlinks but Low Traffic
- **Cause**: Links from low-authority sites or poor content quality
- **Solution**: Focus on link quality over quantity; improve on-page SEO and content

### Flat Organic Traffic Despite More Keywords
- **Cause**: Keywords ranking in positions 20+; content may be thin
- **Solution**: Improve content depth, add internal links, enhance user experience

## Example Workflow Execution

### Scenario: Check vergolansw.com.au

**Input:**
- Domain: https://www.vergolansw.com.au
- Sheet: SEO History Check
- Date: 2025-12-31

**Execution:**
1. Fetch Ahrefs metrics for vergolansw.com.au
2. Read the "SEO History Check" sheet structure
3. Map metrics to cells D5:D8, D12:D13
4. Update the Overview column with current values

**Output:**
- Domain Rating: 27
- URL Rating: 9
- Backlinks: 1,561
- Ref. Domains: 94
- Total Keywords: 194
- Organic Traffic: 1,789

## Next Steps

After updating the sheet:
1. Compare with previous month's data to identify trends
2. Focus on improving lowest-performing metrics
3. Plan content and link-building initiatives based on keyword gaps
4. Re-check metrics in 4-8 weeks after implementing changes
