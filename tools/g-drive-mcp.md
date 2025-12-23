# Google Drive MCP Tool

## Description
Store and share SEO audit reports, crawl data, and screenshots via Google Drive.

## Capabilities
- Upload files and folders
- Create shareable links
- Organize reports in folders
- Set permissions and access control
- Version control for reports
- Search and retrieve past audits

## Usage Examples

```json
{
  "tool": "drive_upload",
  "filePath": "reports/seo-audit-2025-12.pdf",
  "parentFolderId": "folder123",
  "name": "SEO Audit Report - December 2025"
}
```

```json
{
  "tool": "drive_share",
  "fileId": "file123",
  "role": "reader",
  "type": "anyone"
}
```

## Configuration
Requires Google Drive MCP server with OAuth authentication configured.
