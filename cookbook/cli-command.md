# SEO Audit CLI Commands

## Basic Crawl
```bash
# Crawl a website with standard settings
screaming-frog-cli crawl https://example.com ./output/example-audit

# Crawl with depth limit
screaming-frog-cli crawl https://example.com ./output/example-audit --max-depth 3

# Crawl specific subdirectory
screaming-frog-cli crawl https://example.com/blog/ ./output/blog-audit
```

## Export Commands
```bash
# Export all data as CSV
screaming-frog-cli export crawl-123 csv ./reports/

# Export specific reports
screaming-frog-cli export crawl-123 xlsx ./reports/internal-links.xlsx --report internal-links

# Export broken links only
screaming-frog-cli export crawl-123 csv ./reports/broken-links.csv --filter "status:404"
```

## Configuration
```bash
# Use custom configuration file
screaming-frog-cli config ./configs/deep-crawl.config crawl https://example.com ./output/

# Set user agent
screaming-frog-cli crawl https://example.com ./output/ --user-agent "SEO-Audit-Bot/1.0"

# Follow external links
screaming-frog-cli crawl https://example.com ./output/ --follow-external
```

## Common Workflows

### Full Technical SEO Audit
```bash
# 1. Crawl the site
screaming-frog-cli crawl https://example.com ./output/full-audit --max-depth 5

# 2. Export key reports
screaming-frog-cli export full-audit csv ./reports/all-pages.csv
screaming-frog-cli export full-audit csv ./reports/broken-links.csv --filter "status:404,500"
screaming-frog-cli export full-audit csv ./reports/redirects.csv --filter "status:301,302"
screaming-frog-cli export full-audit csv ./reports/missing-meta.csv --filter "meta-description:empty"
```

### On-Page SEO Analysis
```bash
# Export title and meta analysis
screaming-frog-cli export full-audit csv ./reports/titles.csv --report page-titles
screaming-frog-cli export full-audit csv ./reports/meta-descriptions.csv --report meta-descriptions
screaming-frog-cli export full-audit csv ./reports/headings.csv --report h1-headings
```

### Performance Audit
```bash
# Crawl with performance metrics
screaming-frog-cli crawl https://example.com ./output/perf-audit --collect-performance --throttle 3G
```
