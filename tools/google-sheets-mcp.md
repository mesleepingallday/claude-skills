# Google Sheets MCP Tool

## Description
Export SEO audit data and reports to Google Sheets for client delivery and collaborative analysis.

## Capabilities
- Create new spreadsheets
- Write audit data to sheets
- Format cells and apply styles
- Create charts and visualizations
- Share sheets with stakeholders
- Append data for historical tracking

## Usage Examples

```json
{
  "tool": "sheets_create",
  "title": "SEO Audit Report - Example.com",
  "sheets": ["Overview", "Technical Issues", "On-Page SEO", "Recommendations"]
}
```

```json
{
  "tool": "sheets_write",
  "spreadsheetId": "abc123",
  "range": "Technical Issues!A1",
  "values": [
    ["URL", "Issue Type", "Status Code", "Priority"],
    ["https://example.com/page1", "404 Error", "404", "High"]
  ]
}
```

## Configuration
Requires Google Sheets MCP server with OAuth authentication configured.
