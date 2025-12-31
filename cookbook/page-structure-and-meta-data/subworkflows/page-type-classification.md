# Page Type Classification

## Purpose

Classify URLs into SEO page types using pulse-fetch MCP scraping and URL pattern analysis, then update Google Sheets with results.

## Variables

GOOGLE_SHEETS_SPREADSHEET_ID: your_google_sheets_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: Page Structure & Metadata
URL_COLUMN: F
PAGE_TYPE_COLUMN: D
START_ROW: 16

## SEO Page Type Categories

| Page Type | Description | URL Patterns |
|-----------|-------------|--------------|
| Home Page | Main landing page | `/` (root only) |
| Service Page | Service descriptions | `/services/`, `/opening-roof/`, `/residential-*/`, `/commercial-*/` |
| Product Page | Product showcases | `/colours/`, `/colorbond-*/`, `/electric-*/` |
| Landing Page | Marketing/partnership pages | Partner names, campaign URLs |
| Blog Post | Article content | `/blog/`, articles with dates |
| Blog Archive | Blog listing pages | `/blog/`, `/blog/?page=*` |
| Category Archive | Category listings | `/category/*` |
| Date Archive | Monthly/yearly archives | `/YYYY/MM/`, `/2024/03/` |
| Contact Page | Contact forms | `/contact*/` |
| About Page | Company info | `/about*/`, `/why-*/` |
| FAQ Page | Frequently asked questions | `/faq*/` |
| Gallery Page | Image galleries | `/gallery/`, `/portfolio-item/*`, `/our-gallery/` |
| Testimonials Page | Customer reviews | `/testimonials/` |
| Legal Page | Privacy/Terms | `/privacy*/`, `/terms*/` |
| Resource Page | Downloads/Manuals | `/cad-drawings/`, `/for-architects/`, `/warranty/` |
| Thank You Page | Form confirmations | `/thank-you*/`, `/quote-thank-you/` |
| Form Page | Specific forms | `/register-*/`, `/service-cleaning-request/` |
| Test Page | Draft/test pages | `/test-*/`, `/sample-*/` |
| CSS Asset | Non-HTML resources | `.css`, `.js` file extensions |

## Prerequisites

- google-sheets MCP configured
- pulse-fetch MCP configured

## Classification Logic

### Step 1: URL Pattern Analysis (Fast)

Classify ~60% of pages instantly using URL patterns:

```
IF url == "/" THEN "Home Page"
IF url matches /\/\d{4}\/\d{2}\// THEN "Date Archive"
IF url contains "/contact" THEN "Contact Page"
IF url contains "/faq" THEN "FAQ Page"
IF url contains "/privacy" OR "/terms" THEN "Legal Page"
IF url contains "/thank-you" THEN "Thank You Page"
IF url contains "/gallery" OR "/portfolio-item" THEN "Gallery Page"
IF url contains "/category/" THEN "Category Archive"
IF url contains "/blog/" with pagination THEN "Blog Archive"
IF url ends with ".css" OR ".js" THEN "CSS Asset"
IF url contains "/test-" OR "/sample-" THEN "Test Page"
```

### Step 2: Content Scraping (For Ambiguous URLs)

Use pulse-fetch MCP to scrape pages that can't be classified by URL alone:

```bash
mcp__pulse-fetch__scrape(url, maxChars=10000, resultHandling="returnOnly")
```

Analyze scraped content for:
- H1 heading text
- Page structure (blog breadcrumb, share buttons, dates)
- Content type (article vs service description vs gallery)
- Meta information

### Step 3: Classification Decision

Based on content analysis:
- Blog breadcrumb + date + share buttons = Blog Post
- Service description + CTA buttons = Service Page
- Image gallery grid = Gallery Page
- FAQ accordion structure = FAQ Page
- Form elements = Form Page or Contact Page

## Workflow

1. **Read URLs from Google Sheets**
   ```
   mcp__google-sheets__get_sheet_data(
     spreadsheet_id=GOOGLE_SHEETS_SPREADSHEET_ID,
     sheet=GOOGLE_SHEETS_WORKSHEET_NAME
   )
   ```

2. **Extract URLs**
   - Get URLs from URL_COLUMN starting at START_ROW
   - Count total URLs to process

3. **Classify by URL Patterns**
   - Apply pattern matching rules
   - Mark ~60% as classified
   - Flag remaining for content scraping

4. **Scrape Ambiguous Pages**
   - Use pulse-fetch MCP for unclassified URLs
   - Process in batches (5-10 concurrent)
   - Analyze H1, structure, content

5. **Finalize Classifications**
   - Apply content-based rules
   - Handle edge cases

6. **Update Spreadsheet**
   ```
   mcp__google-sheets__update_cells(
     spreadsheet_id=GOOGLE_SHEETS_SPREADSHEET_ID,
     sheet=GOOGLE_SHEETS_WORKSHEET_NAME,
     range="D16:D{last_row}",
     data=[[page_type] for page_type in classifications]
   )
   ```

7. **Report Summary**
   ```
   Total URLs: X
   Classified by pattern: Y (Z%)
   Classified by scraping: A (B%)

   Page Type Distribution:
   - Home Page: 1
   - Service Page: X
   - Blog Post: Y
   ...
   ```

## Tips

- Process URLs in parallel batches for speed
- Use URL patterns first to minimize API calls
- Scrape only when necessary (ambiguous cases)
- Handle rate limiting with delays between batches
- Cache scraped content to avoid re-fetching

## Example Execution

```bash
# User request
"Classify page types for URLs in the Page Structure & Metadata sheet"

# Steps
1. Read spreadsheet → 156 URLs found
2. Pattern match → 95 classified (61%)
3. Scrape remaining → 61 pages
4. Update column D → 156 rows updated

# Result
Page Type Distribution:
- Blog Post: 48
- Date Archive: 32
- Service Page: 16
- Gallery Page: 13
...
```
