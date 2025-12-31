# Purpose

Check if a website has all required Business Trust Pages (legal and credibility pages) using MCP Docker Playwright browser tools. These pages are essential for establishing trust with visitors and search engines.

## Variables

TARGET_URL: https://example.com

## Pages to Check

| Page | Common URL Patterns | Purpose |
|------|---------------------|---------|
| Privacy Policy | /privacy/, /privacy-policy/, /privacy-statement/ | Legal requirement for data collection |
| Terms & Conditions | /terms/, /terms-conditions/, /terms-and-conditions/ | Legal protection and user agreement |
| About | /about/, /about-us/ | Company/brand information |
| Contact | /contact/, /contact-us/ | Customer communication channel |
| Team | /team/, /our-team/, /meet-the-team/ | Human element and credibility |
| Testimonials | /testimonials/, /reviews/, /*/testimonials/ | Social proof |
| FAQs | /faq/, /faqs/, /frequently-asked-questions/ | User support and keyword targeting |

## Prerequisites

- MCP Docker with Playwright browser tools configured
- Chrome browser available for remote debugging

## Instructions

- Use MCP Docker browser tools (`mcp__MCP_DOCKER__browser_*`)
- Take accessibility snapshots (`browser_snapshot`) to analyze page structure
- Check footer links first (most trust pages are linked there)
- Open navigation menu to find additional page links
- Navigate to each page URL to verify it exists (200) or returns 404

## Workflow

1. **Navigate to Target Homepage**

   - Use `mcp__MCP_DOCKER__browser_navigate` to load the target URL
   - Wait for page to fully load

2. **Take Accessibility Snapshot**

   - Use `mcp__MCP_DOCKER__browser_snapshot` to capture page structure
   - Look for footer section (`contentinfo`) for trust page links
   - Common footer links: Privacy Statement, Terms & Conditions

3. **Open Navigation Menu**

   - Click on Menu/hamburger button if present
   - Take another snapshot to reveal full navigation
   - Look for Contact, About, FAQ links in navigation

4. **Check Each Trust Page**

   For each page type, try common URL patterns:

   ```
   Privacy Policy:
   - /privacy-statement/
   - /privacy-policy/
   - /privacy/

   Terms & Conditions:
   - /terms-conditions/
   - /terms-and-conditions/
   - /terms/

   About:
   - /about/
   - /about-us/

   Contact:
   - /contact-us/
   - /contact/

   Team:
   - /team/
   - /our-team/

   Testimonials:
   - /testimonials/
   - /why-vergola/testimonials/ (subfolder pattern)
   - /reviews/

   FAQs:
   - /faq/
   - /faqs/
   ```

5. **Verify Page Existence**

   - Navigate to each URL
   - Check if page loads successfully (200) or returns 404
   - Page Title containing "Page not found" indicates 404

6. **Generate Summary Report**

   - Create table with page name, status (Yes/No), and URL
   - Count pages found vs missing
   - Note any alternative pages that serve similar purpose

## Example Tool Calls

### Navigate to URL
```javascript
mcp__MCP_DOCKER__browser_navigate({
  url: "https://www.example.com/"
})
```

### Take Snapshot
```javascript
mcp__MCP_DOCKER__browser_snapshot()
```

### Click Menu
```javascript
mcp__MCP_DOCKER__browser_click({
  element: "Menu navigation",
  ref: "e18"  // ref from snapshot
})
```

### Close Browser When Done
```javascript
mcp__MCP_DOCKER__browser_close()
```

## Output Format

### Summary Table Example

| Page | Status | URL |
|------|--------|-----|
| Privacy Policy | Yes | https://example.com/privacy-statement/ |
| Terms & Conditions | Yes | https://example.com/terms-conditions/ |
| About Page | No | Returns 404 |
| Contact Page | Yes | https://example.com/contact-us/ |
| Team Page | No | Returns 404 |
| Testimonials Page | Yes | https://example.com/why-vergola/testimonials/ |
| FAQs Page | Yes | https://example.com/faq/ |

### Summary
- **5 of 7 pages exist**: Privacy Policy, Terms & Conditions, Contact, Testimonials, FAQs
- **2 pages are missing**: About Page, Team Page

### Notes
- The "Why VERGOLA" page may contain About-like content but is not a dedicated About page
- Consider recommending creation of missing pages for improved trust signals

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Page not loading | Timeout or blocked | Increase timeout, check URL access |
| Links not visible | Hidden in mobile menu | Click hamburger menu first |
| 404 on common URL | Non-standard URL structure | Check footer/nav for actual links |
| Snapshot too large | Complex page DOM | Focus on footer section only |

## Tips

- Footer section (`contentinfo` in snapshot) usually contains Privacy and Terms links
- Navigation menu reveals Contact, About, FAQ pages
- Some sites use non-standard URLs (e.g., /why-us/ instead of /about/)
- Testimonials may be under a parent page (e.g., /why-vergola/testimonials/)
- Check for alternative content that serves same purpose even if page name differs

## Learning Curve (Updated: 2025-12-31)

### Real-World Example: www.vergolansw.com.au

Successfully checked trust pages with following results:

| Page | Status | URL |
|------|--------|-----|
| Privacy Policy | Yes | /privacy-statement/ |
| Terms & Conditions | Yes | /terms-conditions/ |
| About Page | No | /about/ and /about-us/ return 404 |
| Contact Page | Yes | /contact-us/ |
| Team Page | No | /team/ returns 404 |
| Testimonials Page | Yes | /why-vergola/testimonials/ |
| FAQs Page | Yes | /faq/ |

**Key Observations**:

1. **Footer Links** - Privacy Statement and Terms & Conditions found in footer (contentinfo section)
2. **Menu Navigation** - Contact and FAQ found in main menu after clicking hamburger icon
3. **Subfolder Pattern** - Testimonials located under /why-vergola/ parent page
4. **"Why VERGOLA" Page** - Contains company history (since 1984, Australian made) but is product-focused, not a true About page
5. **Processing Time** - Full audit completed in ~2 minutes with 7 page navigations

**Recommendations for this site**:
- Create dedicated /about/ page with company story, mission, values
- Create /team/ page to showcase staff and build human connection
