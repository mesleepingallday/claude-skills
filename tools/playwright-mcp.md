# Playwright MCP Tool

## Description
Browser automation tool for capturing screenshots, testing page rendering, and analyzing visual SEO elements.

## Capabilities
- Screenshot capture of pages
- Full-page scrolling screenshots
- Mobile/desktop viewport testing
- Visual regression testing
- Page load performance metrics
- JavaScript error detection

## Usage Examples

```json
{
  "tool": "playwright_navigate",
  "url": "https://example.com",
  "viewport": {"width": 1920, "height": 1080}
}
```

```json
{
  "tool": "playwright_screenshot",
  "path": "screenshots/homepage.png",
  "fullPage": true
}
```

## Configuration
Requires Playwright MCP server to be installed and configured in Claude Code settings.
