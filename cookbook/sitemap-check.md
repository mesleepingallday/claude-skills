# Sitemap Check

## Purpose

Check if a website has XML Sitemap and HTML Sitemap, verify robots.txt configuration, and report findings.

## Variables

CLIENT_SITE_URL: https://www.example.com

## Prerequisites

- pulse-fetch MCP configured

## Sitemap Types

| Type | Description | Common URLs |
|------|-------------|-------------|
| XML Sitemap | Machine-readable sitemap for search engines | `/sitemap.xml`, `/sitemap_index.xml` |
| HTML Sitemap | Human-readable sitemap page for users | `/sitemap/`, `/sitemap.html`, `/site-map/` |
| robots.txt | Should reference XML sitemap location | `/robots.txt` |

## Common XML Sitemap Generators

| Generator | Sitemap URL Pattern |
|-----------|---------------------|
| Yoast SEO | `/sitemap_index.xml` with sub-sitemaps |
| Rank Math | `/sitemap_index.xml` |
| All in One SEO | `/sitemap.xml` |
| XML Sitemaps | `/sitemap.xml` |
| Custom | Various |

## Workflow

### Step 1: Check XML Sitemap

Fetch these URLs using pulse-fetch MCP:

```
mcp__pulse-fetch__scrape(
  url="{CLIENT_SITE_URL}/sitemap.xml",
  maxChars=5000,
  resultHandling="returnOnly"
)

mcp__pulse-fetch__scrape(
  url="{CLIENT_SITE_URL}/sitemap_index.xml",
  maxChars=5000,
  resultHandling="returnOnly"
)
```

**Success indicators**:
- HTTP 200 response
- XML content with `<sitemapindex>` or `<urlset>` tags
- Contains `<loc>` entries with URLs

**Parse sitemap index** to identify sub-sitemaps:
- post-sitemap.xml (blog posts)
- page-sitemap.xml (pages)
- category-sitemap.xml (categories)
- author-sitemap.xml (authors)
- product-sitemap.xml (products - ecommerce)

### Step 2: Check HTML Sitemap

Fetch these URLs:

```
mcp__pulse-fetch__scrape(
  url="{CLIENT_SITE_URL}/sitemap/",
  maxChars=5000,
  resultHandling="returnOnly"
)

mcp__pulse-fetch__scrape(
  url="{CLIENT_SITE_URL}/sitemap.html",
  maxChars=5000,
  resultHandling="returnOnly"
)
```

**Success indicators**:
- HTTP 200 response
- HTML content with links to site pages
- Organized list/hierarchy of pages

### Step 3: Check robots.txt

```
mcp__pulse-fetch__scrape(
  url="{CLIENT_SITE_URL}/robots.txt",
  maxChars=2000,
  resultHandling="returnOnly"
)
```

**Verify**:
- Contains `Sitemap:` directive
- Sitemap URL is correct and accessible
- No conflicting `Disallow` rules blocking sitemap

### Step 4: Report Findings

Generate report in this format:

```markdown
## Sitemap Check Results for {CLIENT_SITE_URL}

### XML Sitemap: [EXISTS/NOT FOUND]

**URL**: `{sitemap_url}`
**Generator**: {generator_name}

**Sub-sitemaps**:
| Sitemap | Last Modified |
|---------|---------------|
| post-sitemap.xml | YYYY-MM-DD |
| page-sitemap.xml | YYYY-MM-DD |
| ... | ... |

**robots.txt**: [References sitemap / Missing reference]

---

### HTML Sitemap: [EXISTS/NOT FOUND]

**URL**: `{html_sitemap_url}` (if exists)

**Recommendation**: {recommendation if missing}
```

## Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Sitemap exists | Parse and report details |
| 404 | Sitemap not found | Report as missing |
| 301/302 | Redirect | Follow redirect and check |
| 403 | Forbidden | Report access issue |
| 500 | Server error | Report server issue |

## Recommendations

### If XML Sitemap Missing:
- Install SEO plugin (Yoast, Rank Math, etc.)
- Generate sitemap via plugin settings
- Submit to Google Search Console

### If HTML Sitemap Missing:
- Create dedicated sitemap page
- Use plugin or manual creation
- Link from footer navigation

### If robots.txt Missing Sitemap Reference:
- Add `Sitemap: https://example.com/sitemap.xml` to robots.txt

## Example Execution

```bash
# User request
"Check if https://www.vergolansw.com.au/ has XML and HTML sitemap"

# Steps executed
1. Fetch /sitemap.xml → 200 OK, Yoast SEO sitemap index
2. Fetch /sitemap_index.xml → 200 OK (same content)
3. Fetch /sitemap/ → 404 Not Found
4. Fetch /sitemap.html → 404 Not Found
5. Fetch /robots.txt → Contains Sitemap directive

# Result
- XML Sitemap: EXISTS (Yoast SEO, 6 sub-sitemaps)
- HTML Sitemap: NOT FOUND
- robots.txt: Correctly references sitemap
```

## Tips

- Always check both /sitemap.xml and /sitemap_index.xml
- Some sites use custom sitemap paths - check robots.txt first
- Large sites may have multiple sitemap indexes
- Check lastmod dates to verify sitemap freshness
