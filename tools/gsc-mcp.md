# Google Search Console MCP Tool

## Description
Access Google Search Console data for SEO audits including indexing status, search analytics, sitemaps, and URL inspection.

## Capabilities
- List GSC properties
- Get search analytics data (queries, pages, devices, countries)
- Inspect URL indexing status (single and batch)
- Check indexing issues
- List and manage sitemaps
- Compare search performance between periods
- Get performance overview

## Key Functions

### URL Inspection
- `mcp__gsc__inspect_url_enhanced` - Check single URL indexing status
- `mcp__gsc__batch_url_inspection` - Check multiple URLs (max 10 per batch)
- `mcp__gsc__check_indexing_issues` - Check indexing issues for URLs

### Search Analytics
- `mcp__gsc__get_search_analytics` - Get search data by dimensions
- `mcp__gsc__get_advanced_search_analytics` - Advanced filtering and sorting
- `mcp__gsc__compare_search_periods` - Compare two time periods
- `mcp__gsc__get_search_by_page_query` - Get queries for specific page

### Sitemaps
- `mcp__gsc__list_sitemaps_enhanced` - List all sitemaps
- `mcp__gsc__get_sitemap_details` - Get sitemap details
- `mcp__gsc__submit_sitemap` - Submit new sitemap
- `mcp__gsc__delete_sitemap` - Delete/unsubmit sitemap
- `mcp__gsc__manage_sitemaps` - All-in-one sitemap management

### Properties
- `mcp__gsc__list_properties` - List all GSC properties
- `mcp__gsc__get_site_details` - Get property details
- `mcp__gsc__add_site` - Add new property
- `mcp__gsc__delete_site` - Remove property
- `mcp__gsc__get_performance_overview` - Performance summary

## Usage Examples

### List Properties
```
mcp__gsc__list_properties()
```

### Check URL Indexing Status (Batch)
```
mcp__gsc__batch_url_inspection({
  site_url: "https://example.com/",
  urls: "https://example.com/page1\nhttps://example.com/page2\nhttps://example.com/page3"
})
```
Note: Maximum 10 URLs per batch to avoid API quota issues.

### Get Search Analytics
```
mcp__gsc__get_search_analytics({
  site_url: "https://example.com/",
  days: 28,
  dimensions: "query,page"
})
```

### Get Advanced Search Analytics with Filters
```
mcp__gsc__get_advanced_search_analytics({
  site_url: "https://example.com/",
  dimensions: "query,page",
  row_limit: 1000,
  sort_by: "clicks",
  sort_direction: "descending",
  filter_dimension: "page",
  filter_operator: "contains",
  filter_expression: "/blog/"
})
```

### Compare Search Periods
```
mcp__gsc__compare_search_periods({
  site_url: "https://example.com/",
  period1_start: "2025-11-01",
  period1_end: "2025-11-30",
  period2_start: "2025-12-01",
  period2_end: "2025-12-30",
  dimensions: "query",
  limit: 20
})
```

### List Sitemaps
```
mcp__gsc__list_sitemaps_enhanced({
  site_url: "https://example.com/"
})
```

## Indexing Status Values

| Status | Description |
|--------|-------------|
| `Submitted and indexed` | Page is indexed in Google |
| `Discovered - currently not indexed` | Google knows the URL but hasn't crawled it |
| `Crawled - currently not indexed` | Google crawled but chose not to index |
| `URL is unknown to Google` | Google has never seen this URL |
| `Excluded by 'noindex' tag` | Page has noindex directive |
| `Blocked by robots.txt` | Page blocked by robots.txt |

## Site URL Formats

- Standard: `https://example.com/` or `https://www.example.com/`
- Domain property: `sc-domain:example.com`

## Configuration
Requires GSC MCP server with OAuth authentication configured.
