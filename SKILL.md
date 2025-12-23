---
name: seo-audit
description: Audit an Anthropic Cookbook notebook based on a rubric. Use whenever a notebook review or audit is requested.
---

# SEO Audit

## Purpose

Conduct comprehensive SEO audits of websites using Screaming Frog SEO Spider CLI, covering the following areas:

1. **SEO History Check**

   - Google Trust (DR, UR, Backlinks, Ref. Domains)
   - Organic Search (Total Keywords, Organic Traffic)
   - Branding
   - Content Penalty
   - Backlink Penalty
   - Citation

2. **Security & Site Info**

   - Site Security (SSL, Domain Redirect, CMS Version, CMS Child Theme, CMS Theme Version, CMS Plugin Version)
   - Site Basics (Favicon, Website Name, Alternate Website Name, Tagline, Title Separator, Site image, Site Language, Time zone)
   - Site Representation (Organisation Name, Alternate Organisation Name, Organisation Logo, Other Social Profiles)

3. **Business Trust Page**

   - Privacy Policy Page
   - Terms & Conditions Page
   - About Page
   - Contact Page
   - Team Page
   - Testimonials Page
   - FAQs Page

4. **Site Crawling**

   - XML Sitemap
   - XML Sitemap on Google Search Console
   - HTML Sitemap
   - Set Noindex to No-Target Pages (Low-Quality Content Types, Low-Quality Archives/Categories/Tags)
   - Pages aren't Indexed (GSC)

5. **Page Structure & Metadata**

   - Meta Tags (Meta Title, Meta Description, URL)
   - Featured Images
   - Schema Markup
   - Heading HTML Tags

6. **Link Structure**

   - Internal Linking (Home Page, Landing Pages, Top Navigation, Footer, Contextual, Widget)
   - Internal Broken Link (301 Permanent Redirect, 302 Temporary Redirect, 404 Not Found)
   - External Broken Link

7. **User Experience**

   - Core Web Vitals
   - Page Speed
   - Mobile Friendly / Website Responsive

8. **Image**

   - Image Data (Filename, Title)
   - Image Alt Text (Missing Alt Text, Alt Text Over 100 Characters)
   - Image File Size (Over 100 KB, Next-Gen Format WebP)
   - Redirect Image URL to Content

9. **Online Reputation Management**
   - Google Business Profile
   - Social Profiles (Facebook Page, X/Twitter, LinkedIn)

Follow the `Instructions`, Execute the `Workflow`, based on the `Cookbook` to perform the SEO audit based on user requests.

## Variables

ENABLE_SCREAMING_FROG_CLI: false
ENABLE_GOOGLE_SHEETS_MCP: false
ENABLE_GOOGLE_DRIVE_MCP: false
ENABLE_PULSE_FETCH_MCP: false
ENABLE_PLAYWRIGHT_MCP: false
ENABLE_ZOHO_PROJECTS_MCP: false
ENABLE_AHREFS_MCP: false

GOOGLE_SHEETS_SPREADSHEET_ID: your_google_sheets_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: examle_worksheet_name
INPUT_CELLS_RANGE: A1:A10
OUTPUT_CELLS_RANGE: B1:B10
PULSE_FETCH_URLS[]: [url_1, url_2, ...]
PLAYWRIGHT_URL: your_playwright_url

ZOHO_PROJECTS_PROJECT_ID: your_zoho_projects_project_id
ZOHO_PROJECTS_TASK_ID: your_zoho_projects_task_id

## Instructions

- Based on the user's request, follow the `Cookbook` to determine which tool to use.

## Workflow

1. Understand the user's request.
2. READ: .md file in `/.claude/skills/seo-audit/tools/` to understand our toolings.
3. Follow the `Cookbook` to determine which tool to use.
4. Execute the tools based on the user's request.

## Cookbook

### Page Structure & Metadata

- IF: the user requests an SEO audit for page structure and metadata.
- THEN: Read and execute: `.claude/skills/seo-audit/cookbook/page-structure-and-metadata.md`
- EXAMPLE:
  - "Can you help me to seo audit this url page structure and metadata?"
  - "I want to run a seo audit for page structure and metadata."
  - "Audit page structure and metadata for this url."
  - "Please perform an SEO audit focusing on page structure and metadata."
  - "SEO Audit meta title, meta description, headings for this page."
  - "page structure and metadata sheet."
