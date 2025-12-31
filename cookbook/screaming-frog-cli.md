# Screaming Frog CLI Integration Guide

## Installation

### Windows
```powershell
# Download and install Screaming Frog SEO Spider
# Add to PATH or create alias
$env:PATH += ";C:\Program Files\Screaming Frog SEO Spider"
```

### macOS
```bash
# Install via Homebrew (if available) or download from website
# Create symlink
ln -s "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpider" /usr/local/bin/screaming-frog
```

### Linux
```bash
# Download and extract
wget https://download.screamingfrog.co.uk/products/seo-spider/ScreamingFrogSEOSpider-XX.X.deb
sudo dpkg -i ScreamingFrogSEOSpider-XX.X.deb
```

## Configuration Files

### Basic Config (basic-crawl.config)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
  <crawl>
    <max-depth>3</max-depth>
    <max-urls>10000</max-urls>
    <respect-robots>true</respect-robots>
  </crawl>
  <spider>
    <user-agent>SEO-Audit-Bot/1.0</user-agent>
    <crawl-speed>fast</crawl-speed>
  </spider>
</config>
```

### Deep Crawl Config (deep-crawl.config)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
  <crawl>
    <max-depth>10</max-depth>
    <max-urls>100000</max-urls>
    <follow-external>false</follow-external>
  </crawl>
  <extraction>
    <page-titles>true</page-titles>
    <meta-descriptions>true</meta-descriptions>
    <headings>true</headings>
    <images>true</images>
    <links>true</links>
  </extraction>
</config>
```

## Integration with Claude Code

### Example Workflow Script
```bash
#!/bin/bash
# complete-seo-audit.sh

CLIENT_SITE_URL=$1
OUTPUT_DIR=$2
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
AUDIT_DIR="${OUTPUT_DIR}/${TIMESTAMP}"

# Create output directory
mkdir -p "${AUDIT_DIR}"

# Run crawl
echo "Starting crawl of ${CLIENT_SITE_URL}..."
screaming-frog-cli crawl "${CLIENT_SITE_URL}" "${AUDIT_DIR}" --config ./configs/deep-crawl.config

# Export reports
echo "Exporting reports..."
screaming-frog-cli export "${AUDIT_DIR}" csv "${AUDIT_DIR}/reports/all-pages.csv"
screaming-frog-cli export "${AUDIT_DIR}" csv "${AUDIT_DIR}/reports/errors.csv" --filter "status:4xx,5xx"

# Generate summary
echo "Audit complete. Reports saved to ${AUDIT_DIR}"
ls -lh "${AUDIT_DIR}/reports/"
```

## Tips for Effective Crawling

### 1. Set Appropriate Limits
- Small sites (<1000 pages): No limits needed
- Medium sites (1000-10000 pages): Set max-depth 5-7
- Large sites (>10000 pages): Use URL sampling or segment crawls

### 2. Optimize Crawl Speed
- Fast networks: Use fast crawl speed
- Slow/shared hosting: Throttle to avoid server overload
- Always respect robots.txt

### 3. Focus on Priorities
- Initial audit: Crawl entire site
- Regular monitoring: Crawl new/changed pages only
- Quick checks: Crawl specific sections

### 4. Handle Authentication
```bash
# For sites requiring login
screaming-frog-cli crawl https://example.com ./output/ --auth-user username --auth-pass password
```

### 5. JavaScript Rendering
```bash
# Enable JavaScript rendering for SPAs
screaming-frog-cli crawl https://example.com ./output/ --render-js
```

## Common Issues and Solutions

### Issue: Crawl too slow
**Solution**: Increase crawl threads or reduce extraction options

### Issue: Running out of memory
**Solution**: Reduce max URLs or use database mode

### Issue: Missing pages
**Solution**: Check robots.txt, increase max depth, verify internal linking

### Issue: Authentication required
**Solution**: Use --auth-user and --auth-pass flags or configure session cookies
