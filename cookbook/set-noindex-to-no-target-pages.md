# Purpose

Identify and categorize URLs that should be set to `noindex` to prevent search engine indexing of non-SEO target pages. This helps eliminate duplicate content, thin content, and low-value pages from Google's index.

## Variables

SITE_DOMAIN: example.com
INPUT_URLS_SOURCE: Google Sheets URL column | CSV file | User-provided list
GOOGLE_SHEETS_SPREADSHEET_URL: https://docs.google.com/spreadsheets/d/your_id/edit
GOOGLE_SHEETS_WORKSHEET_NAME: Noindex Analysis

### URL Pattern Categories

NOINDEX_PATTERNS:
  PAGINATION: ["?page=2", "?page=3", "&page="]
  SORT_FILTER: ["?limit=", "?order=", "&order=", "phcursor="]
  PRICE_FILTER: ["/-$", "/0-50", "/50-100", "/100-200", "/200-300", "/300-400", "/400-500", "/500-750", "/750-1000", "/1000"]
  BRAND_FILTER: ["/-brandname", "/brand?page=", "/brand/brand"]
  UTILITY_PAGES: ["/order-tracking", "/register-for-sms", "/online-orders-form"]

KEEP_INDEXED_PATTERNS:
  PRODUCTS: ["/products/"]
  MAIN_COLLECTIONS: ["/collections/" without parameters]
  BLOG_CONTENT: ["/blogs/"]
  INFO_PAGES: ["/pages/" except utility pages]

### Execution Configuration

PLAN_MODEL: opus 4.5
EXECUTE_MODEL: haiku 4.5
MULTI_AGENTS_PARALLEL_EXECUTION: true
AGENTS_COUNT: 3
URLS_PER_AGENT: 100

## Prerequisites

- List of URLs to analyze (from sitemap, crawl, or Google Sheets)
- pulse-fetch MCP configured (for page content verification)
- google-sheets MCP configured (for output)

## Instructions

- Before executing, run `claude mcp get pulse-fetch` to understand MCP options.
- Use pattern matching for initial categorization (~80% accuracy).
- Use pulse-fetch to verify uncertain cases.
- Output results to Google Sheets or markdown report.

## Workflow

### 1. Collect URLs

- IF Google Sheets input: Read URLs from INPUT_CELLS_RANGE
- IF CSV file: Parse URLs from CSV
- IF User list: Parse provided URL list

### 2. Pattern-Based Categorization

For each URL, apply pattern matching in order:

```python
def categorize_url(url):
    # Check NOINDEX patterns first
    if "?page=" in url and not url.endswith("?page=1"):
        return "NOINDEX", "Pagination (page 2+)"

    if any(p in url for p in ["?limit=", "?order=", "phcursor="]):
        return "NOINDEX", "Sort/Filter Parameters"

    if any(p in url for p in ["/-$", "/0-50", "/50-100", "/100-200", "/200-300", "/300-400", "/400-500", "/500-750", "/750-1000"]):
        return "NOINDEX", "Price Filter"

    if re.search(r'/collections/[^/]+/-[^/]+', url):
        return "NOINDEX", "Brand Filter"

    if "/products/" in url:
        return "INDEX", "Product Page"

    if "/blogs/" in url:
        return "INDEX", "Blog Content"

    if "/collections/" in url and "?" not in url and "/-" not in url:
        return "INDEX", "Main Collection"

    return "VERIFY", "Needs Manual Review"
```

### 3. Verify Uncertain URLs (Optional)

For URLs marked "VERIFY", use pulse-fetch:

```
mcp__pulse-fetch__scrape({
  url: <target_url>,
  cleanScrape: true,
  maxChars: 5000,
  resultHandling: returnOnly
})
```

Check content for:
- Unique valuable content -> INDEX
- Duplicate/thin content -> NOINDEX
- Product listings without filters -> INDEX
- Filtered/sorted product listings -> NOINDEX

### 4. Generate Report

Output categories:
- **NOINDEX** - Should be blocked from indexing
- **INDEX** - Should remain indexed
- **VERIFY** - Requires manual review

### 5. Implementation Recommendations

Provide recommendations based on platform:

#### Shopify
```liquid
{% if request.path contains '?page=' or request.path contains '?limit=' %}
  <meta name="robots" content="noindex, follow">
{% endif %}
```

#### WordPress
```php
if (is_paged() || isset($_GET['orderby'])) {
    add_action('wp_head', function() {
        echo '<meta name="robots" content="noindex, follow">';
    });
}
```

#### robots.txt
```
Disallow: /*?page=
Disallow: /*?limit=
Disallow: /*?order=
Disallow: /*phcursor=
```

## Pattern Reference

### Patterns That Should Be NOINDEXED

| Pattern | Example | Reason |
|---------|---------|--------|
| `?page=2+` | `/collections/awnings?page=2` | Pagination duplicate content |
| `?limit=` | `/collections/shop-all?limit=50` | Results per page variation |
| `?order=` | `/collections/all?order=price` | Sort order variation |
| `phcursor=` | `/collections/shop-all?phcursor=...` | Cursor pagination |
| `/-$XXX---$XXX` | `/collections/doors/-$100---$200` | Price range filter |
| `/0-50`, `/50-100` | `/collections/fire-safety/400-500` | Price bracket filter |
| `/-brandname` | `/collections/awnings/-northstar` | Negative brand filter |
| `/brand/brand` | `/collections/aussie-traveller/aussie-traveller` | Redundant filter |

### Patterns That Should Remain INDEXED

| Pattern | Example | Reason |
|---------|---------|--------|
| `/products/*` | `/products/thule-single-step-motor` | Product pages - primary SEO targets |
| `/collections/*` (base) | `/collections/awnings` | Main collection pages |
| `/blogs/*` | `/blogs/products/diy-guide` | Unique content |
| `/pages/*` (info) | `/pages/installation-instructions` | Valuable info pages |

## Example Results

### Input: aussietraveller.com.au (580 URLs)

| Category | Count | Percentage |
|----------|-------|------------|
| NOINDEX - Pagination | ~150 | 26% |
| NOINDEX - Price Filters | ~80 | 14% |
| NOINDEX - Query Params | ~60 | 10% |
| NOINDEX - Brand Filters | ~60 | 10% |
| NOINDEX - Utility | ~5 | 1% |
| **Total NOINDEX** | **~355** | **61%** |
| INDEX - Products | ~200 | 34% |
| INDEX - Collections | ~60 | 10% |
| INDEX - Blog/Content | ~15 | 3% |
| **Total INDEX** | **~275** | **47%** |

### Sample NOINDEX URLs
```
https://aussietraveller.com.au/collections/awnings?page=2
https://aussietraveller.com.au/collections/shop-all?limit=10&order=name&page=34
https://aussietraveller.com.au/collections/bathroom-laundry/-$100---$200
https://aussietraveller.com.au/collections/fire-safety/400-500
https://aussietraveller.com.au/collections/awnings/-northstar
```

### Sample INDEX URLs (Keep)
```
https://aussietraveller.com.au/products/thule-single-step-motor
https://aussietraveller.com.au/collections/awnings
https://aussietraveller.com.au/blogs/products/diy-12v-led-strip-lighting
https://aussietraveller.com.au/pages/installation-instructions
```

## Tips

- Run pattern matching first to categorize 80-90% of URLs automatically.
- Only use pulse-fetch for ambiguous cases to save API calls.
- Price filter patterns vary by platform: Shopify uses `/0-50` or `/-$100---$200`.
- Always keep page 1 of collections indexed - only noindex page 2+.
- Product pages should NEVER be noindexed unless explicitly out of stock/discontinued.
- After noindex implementation, monitor Google Search Console for index coverage changes.
- Consider using canonical tags as an alternative for some filtered pages.
