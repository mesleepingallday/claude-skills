# Purpose

Look up hosting and CMS access information for a client from Zoho Projects and Google Sheets.

## Variables

CLIENT_NAME: "Nira Homes"
CLIENT_DOMAIN: "nirahomes.com.au"
ZOHO_PROJECT_ID?: "973435000011259011"

GOOGLE_SHEETS_SPREADSHEET_ID: "1I-Sd2zGnb2m0Fq32cB6o7YzsBTnn3Wk1DeU8g2P7M9M"
GOOGLE_SHEETS_WORKSHEET_NAME: "IM - SEO Clients"

## Prerequisites

- zoho-projects MCP configured and enabled
- google-sheets MCP configured and enabled
- Access to Zoho Vault (for sensitive credentials)

## Instructions

- Before executing with the MCP, run `claude mcp get <mcp-name>` to understand the mcp and its options.
  - EXAMPLE:
    - `claude mcp get zoho-projects`
    - `claude mcp get google-sheets`
- Use CLIENT_DOMAIN to resolve project automatically when possible
- Hosting credentials (cPanel, FTP, etc.) are typically stored in Zoho Vault, not in spreadsheets

## Workflow

1. **Search Zoho Projects for Client**

   - Use `search_portal` operation with CLIENT_NAME or CLIENT_DOMAIN
   - Extract ZOHO_PROJECT_ID from results
   - EXAMPLE:
     ```
     mcp__zoho-projects__search_portal:
       operation: search_portal
       search_term: "Nira Homes"
       module: all
     ```

2. **List Tasklists in Project**

   - Use `list_tasklists` operation with domain
   - Look for tasklists related to hosting, setup, or onboarding
   - EXAMPLE:
     ```
     mcp__zoho-projects__manage_projects:
       operation: list_tasklists
       domain: "nirahomes.com.au"
     ```

3. **Search for Hosting-Related Tasks**

   - Search within project for terms: "hosting", "access", "credentials", "CMS", "cpanel", "wordpress", "webflow", "DNS"
   - EXAMPLE:
     ```
     mcp__zoho-projects__search_portal:
       operation: search_project
       search_term: "hosting"
       domain: "nirahomes.com.au"
     ```

4. **Check Google Sheets for Client Record**

   - Connect to Agency Analytics spreadsheet (ID: 1I-Sd2zGnb2m0Fq32cB6o7YzsBTnn3Wk1DeU8g2P7M9M)
   - Read "IM - SEO Clients" sheet
   - Search for CLIENT_DOMAIN in column B
   - EXAMPLE:
     ```
     mcp__google-sheets__get_sheet_data:
       spreadsheet_id: "1I-Sd2zGnb2m0Fq32cB6o7YzsBTnn3Wk1DeU8g2P7M9M"
       sheet: "IM - SEO Clients"
     ```

5. **Extract Available Information**

   - From Google Sheet columns:
     - Column A: Reseller
     - Column B: Client website URL
     - Column C: Status
     - Column D: iReport Username
     - Column E: iReport Password
     - Column F: Work Report Doc link

6. **Report Findings**

   - Present found information to user
   - IF hosting credentials not found in spreadsheet:
     - Inform user that hosting credentials are stored in Zoho Vault
     - Provide instructions to check Zoho Vault directly

## Expected Output

```
**[CLIENT_NAME] ([CLIENT_DOMAIN])**
- Project ID: [ZOHO_PROJECT_ID]
- Work Report Doc: [link]
- iReport Username: [username or "Not stored"]
- iReport Password: [password or "Not stored"]
- Hosting Access: Check Zoho Vault
```

## Tips

- The Agency Analytics spreadsheet contains iReport/dashboard logins, NOT hosting credentials
- Hosting credentials (cPanel, FTP, WordPress admin) are stored in Zoho Vault for security
- Use domain parameter instead of project_id when possible - it auto-resolves
- If MCP servers are disabled, run `claude mcp enable zoho-projects google-sheets` first
- Check task comments for access details shared by team members
