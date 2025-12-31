# Purpose

Check if a website is responsive across desktop, tablet, and mobile viewports using MCP Docker browser tools. Analyzes navigation behavior, layout adaptation, and device detection.

## Variables

TARGET_URL: https://example.com
DESKTOP_WIDTH: 1440
DESKTOP_HEIGHT: 900
TABLET_WIDTH: 768
TABLET_HEIGHT: 1024
MOBILE_WIDTH: 375
MOBILE_HEIGHT: 667

## Prerequisites

- MCP Docker with Playwright browser tools configured
- Chrome browser available for remote debugging

## Instructions

- Use MCP Docker browser tools (`mcp__MCP_DOCKER__browser_*`)
- Take accessibility snapshots (`browser_snapshot`) rather than screenshots for faster analysis
- Check for device indicator elements that may reveal responsive breakpoints
- Look for navigation changes (hamburger menu vs full menu)

## Workflow

1. **Navigate to Target URL**

   - Use `mcp__MCP_DOCKER__browser_navigate` to load the target URL
   - Wait for page to fully load

2. **Check Desktop View (1440x900)**

   - Use `mcp__MCP_DOCKER__browser_resize` with width: 1440, height: 900
   - Take accessibility snapshot with `mcp__MCP_DOCKER__browser_snapshot`
   - Analyze:
     - Full navigation menu visibility
     - Multi-column layouts
     - Footer structure
     - Device indicator if present

3. **Check Tablet View (768x1024)**

   - Use `mcp__MCP_DOCKER__browser_resize` with width: 768, height: 1024
   - Take accessibility snapshot
   - Analyze:
     - Navigation collapse behavior (hamburger menu)
     - Layout adaptation
     - Device indicator changes

4. **Check Mobile View (375x667)**

   - Use `mcp__MCP_DOCKER__browser_resize` with width: 375, height: 667
   - Take accessibility snapshot
   - Analyze:
     - Single-column layout
     - Touch-friendly elements
     - Stacked content
     - CTA button accessibility

5. **Generate Summary Report**

   - Create comparison table of features across breakpoints
   - Note any responsive issues found
   - Provide verdict on responsive design quality

## Key Observations to Check

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Navigation | Full menu visible | Hamburger menu | Hamburger menu |
| Layout | Multi-column | Adapted columns | Single-column, stacked |
| Device Indicator | N/A or "desktop" | "tablet" | "mobile" |
| CTAs | Visible | Visible | Visible and tappable |
| Forms | Full width | Adapted | Full width, stacked fields |
| Images | Full size | Scaled | Responsive/hidden |
| Footer | Multi-column | Adapted | Stacked |

## Example Tool Calls

### Navigate to URL
```javascript
mcp__MCP_DOCKER__browser_navigate({
  url: "https://www.example.com/"
})
```

### Resize to Mobile
```javascript
mcp__MCP_DOCKER__browser_resize({
  width: 375,
  height: 667
})
```

### Take Snapshot
```javascript
mcp__MCP_DOCKER__browser_snapshot()
```

## Output Format

### Summary Table Example

| Feature | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Navigation | Full menu | Hamburger | Hamburger |
| Layout | Multi-column | Adapted | Single-column |
| Device Detection | N/A | Shows "tablet" | Shows "mobile" |
| CTA Buttons | Visible | Visible | Visible |
| Form | Visible | Visible | Visible |
| Social Links | Visible | Visible | Visible |

**Verdict**: The website is responsive and adapts well across all tested viewport sizes.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Snapshot too large | Complex page DOM | Focus on key sections only |
| Navigation not collapsing | CSS breakpoint mismatch | Check actual breakpoint values |
| Page not loading | Timeout or blocked | Increase timeout, check URL access |
| Device indicator missing | Not implemented on site | Use layout changes as indicator |

## Tips

- Use accessibility snapshots instead of screenshots for faster processing
- Check for hidden device indicator elements (often used for CSS debugging)
- Look for "Menu" or hamburger icon elements as navigation collapse indicator
- Some sites use custom breakpoints - adjust viewport sizes if needed
- Sticky/fixed elements (headers, CTAs) should remain accessible at all sizes
- Test form fields are accessible and properly sized for touch on mobile

## Learning Curve (Updated: 2025-12-31)

### Real-World Example: www.vergolansw.com.au

Successfully tested responsive design with following observations:

1. **Device Detection**
   - Site has built-in device indicator showing "tablet" or "mobile" text
   - Useful for confirming responsive breakpoints are triggered

2. **Navigation Behavior**
   - Desktop: Full menu visible in header
   - Tablet/Mobile: Collapses to "Menu" hamburger button

3. **Content Adaptation**
   - Hero sections maintain readability across all sizes
   - Instagram feed slider works with arrow navigation at all sizes
   - Sticky quote form bar remains functional

4. **Processing Time**
   - 3 viewport tests completed in ~30 seconds
   - Accessibility snapshots are much faster than screenshots
