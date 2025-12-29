#!/usr/bin/env python3
"""
CSV Parser for SEO Audit
Reads and parses Screaming Frog CSV exports.

Usage:
    python csv_parser.py --csv FILE [options]

Output is designed for Google Sheets MCP upload via:
    mcp__google-sheets__update_cells

Examples:
    # Parse with HTML filter
    python csv_parser.py --csv internal_all.csv --filter-html

    # Select specific columns
    python csv_parser.py --csv internal_all.csv \
        --columns "Address,Title 1,Meta Description 1"

    # Filter by exact value
    python csv_parser.py --csv internal_all.csv --filter "Status Code:200"

    # Filter by multiple conditions
    python csv_parser.py --csv internal_all.csv \
        --filter "Status Code:200" --filter "Indexability:Indexable"

    # Output to file
    python csv_parser.py --csv internal_all.csv --output data.json

    # Preview first 10 rows
    python csv_parser.py --csv internal_all.csv --preview

Token-Efficient Chunking (for large datasets 15K+ rows):
    # Step 1: Get stats only (no data in output - saves 99% tokens)
    python csv_parser.py --csv internal_all.csv --filter-html --stats-only
    # Output: {"total_rows": 6472, "chunk_size": 1000, "chunk_count": 7}

    # Step 2: Process specific chunk (for parallel agents)
    python csv_parser.py --csv internal_all.csv --filter-html \
        --columns "Address,Title 1,Meta Description 1,H1-1" \
        --chunk-index 1 --chunk-size 1000 --format sheets
    # Outputs only rows 1-1000

    # Agent 2 processes chunk 2:
    python csv_parser.py --csv internal_all.csv --filter-html \
        --columns "Address,Title 1,Meta Description 1,H1-1" \
        --chunk-index 2 --chunk-size 1000 --format sheets
    # Outputs only rows 1001-2000
"""

import argparse
import pandas as pd
import json
import sys
from pathlib import Path

# Default SEO columns from Screaming Frog
DEFAULT_COLUMNS = [
    'Address', 'Content Type', 'Status Code', 'Status',
    'Indexability', 'Indexability Status',
    'Title 1', 'Title 1 Length',
    'Meta Description 1', 'Meta Description 1 Length',
    'H1-1', 'Word Count', 'Crawl Depth', 'Inlinks',
    'Canonical Link Element 1'
]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Parse Screaming Frog CSV for SEO audit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--columns', help='Comma-separated column names to output')
    parser.add_argument('--filter', action='append', dest='filters',
                        help='Filter rows: "Column:value" or "Column:contains:value"')
    parser.add_argument('--filter-html', action='store_true',
                        help='Shortcut: filter Content Type contains text/html')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--preview', action='store_true',
                        help='Show first 10 rows only')
    parser.add_argument('--format', choices=['json', 'csv', 'sheets'],
                        default='json', help='Output format (default: json)')
    # Chunking support for large datasets (token-efficient)
    parser.add_argument('--stats-only', action='store_true',
                        help='Output only stats (row count) - no data. Token-efficient.')
    parser.add_argument('--chunk-size', type=int, default=1000,
                        help='Rows per chunk (default: 1000)')
    parser.add_argument('--chunk-index', type=int,
                        help='Output only this chunk (1-indexed). Used by agents.')
    return parser.parse_args()


def read_csv(csv_path: str) -> pd.DataFrame:
    """Read CSV with proper encoding."""
    print(f"[1/3] Reading: {csv_path}", file=sys.stderr)

    df = pd.read_csv(
        csv_path,
        encoding='utf-8-sig',  # Handle BOM
        low_memory=False
    )
    print(f"      Loaded: {len(df)} rows, {len(df.columns)} columns", file=sys.stderr)
    return df


def apply_filter(df: pd.DataFrame, filter_str: str) -> pd.DataFrame:
    """Apply a single filter to DataFrame.

    Filter syntax:
        Column:value          - exact match
        Column:contains:value - substring match
        Column:startswith:value - starts with
        Column:gt:value       - greater than (numeric)
        Column:lt:value       - less than (numeric)
    """
    parts = filter_str.split(':', 2)

    if len(parts) == 2:
        # Exact match: Column:value
        col, value = parts
        if col in df.columns:
            df = df[df[col].astype(str) == value]
        else:
            print(f"      Warning: Column '{col}' not found", file=sys.stderr)

    elif len(parts) == 3:
        col, op, value = parts
        if col not in df.columns:
            print(f"      Warning: Column '{col}' not found", file=sys.stderr)
            return df

        if op == 'contains':
            df = df[df[col].astype(str).str.contains(value, na=False)]
        elif op == 'startswith':
            df = df[df[col].astype(str).str.startswith(value, na=False)]
        elif op == 'gt':
            df = df[pd.to_numeric(df[col], errors='coerce') > float(value)]
        elif op == 'lt':
            df = df[pd.to_numeric(df[col], errors='coerce') < float(value)]
        else:
            print(f"      Warning: Unknown operator '{op}'", file=sys.stderr)

    return df


def apply_filters(df: pd.DataFrame, filters: list, filter_html: bool) -> pd.DataFrame:
    """Apply all filters to DataFrame."""
    print("[2/3] Applying filters...", file=sys.stderr)
    original_count = len(df)

    # Apply --filter-html shortcut
    if filter_html:
        df = apply_filter(df, "Content Type:contains:text/html")
        print(f"      --filter-html: {len(df)} rows", file=sys.stderr)

    # Apply custom filters
    if filters:
        for f in filters:
            before = len(df)
            df = apply_filter(df, f)
            print(f"      --filter \"{f}\": {before} -> {len(df)} rows", file=sys.stderr)

    if not filters and not filter_html:
        print("      No filters applied", file=sys.stderr)

    print(f"      Total: {original_count} -> {len(df)} rows", file=sys.stderr)
    return df


def format_output(df: pd.DataFrame, fmt: str) -> str:
    """Format DataFrame for output."""
    # Replace NaN with empty string
    df = df.fillna('')

    if fmt == 'sheets':
        # 2D array for Google Sheets MCP
        data = [df.columns.tolist()] + df.astype(str).values.tolist()
        return json.dumps(data, ensure_ascii=False)

    elif fmt == 'csv':
        return df.to_csv(index=False)

    else:  # json
        return json.dumps({
            'headers': df.columns.tolist(),
            'data': df.astype(str).values.tolist(),
            'stats': {
                'total_rows': len(df),
                'columns': len(df.columns)
            }
        }, ensure_ascii=False, indent=2)


def get_chunk(df: pd.DataFrame, chunk_index: int, chunk_size: int) -> pd.DataFrame:
    """Extract a specific chunk from DataFrame (1-indexed)."""
    start = (chunk_index - 1) * chunk_size
    end = start + chunk_size
    return df.iloc[start:end]


def main():
    args = parse_args()

    # Parse columns
    columns = args.columns.split(',') if args.columns else DEFAULT_COLUMNS
    columns = [c.strip() for c in columns]

    # Read CSV (need all columns for filtering, select later)
    df = read_csv(args.csv)

    # Apply filters
    df = apply_filters(df, args.filters, args.filter_html)

    # Stats-only mode: output row count without loading data into context
    if args.stats_only:
        total_rows = len(df)
        chunk_count = (total_rows + args.chunk_size - 1) // args.chunk_size
        stats = {
            "total_rows": total_rows,
            "chunk_size": args.chunk_size,
            "chunk_count": chunk_count
        }
        print(json.dumps(stats))
        print(f"Stats: {total_rows} rows, {chunk_count} chunks of {args.chunk_size}", file=sys.stderr)
        return

    # Select output columns (after filtering)
    available_cols = [c for c in columns if c in df.columns]
    missing_cols = [c for c in columns if c not in df.columns]
    if missing_cols:
        print(f"      Warning: Columns not found: {missing_cols}", file=sys.stderr)

    df = df[available_cols]
    print(f"      Selected {len(available_cols)} columns for output", file=sys.stderr)

    # Chunk mode: extract specific chunk (for parallel agent execution)
    if args.chunk_index:
        total_rows = len(df)
        chunk_count = (total_rows + args.chunk_size - 1) // args.chunk_size
        if args.chunk_index < 1 or args.chunk_index > chunk_count:
            print(f"Error: chunk_index {args.chunk_index} out of range (1-{chunk_count})", file=sys.stderr)
            sys.exit(1)
        df = get_chunk(df, args.chunk_index, args.chunk_size)
        print(f"[3/3] Chunk {args.chunk_index}/{chunk_count}: {len(df)} rows", file=sys.stderr)
    # Preview mode
    elif args.preview:
        df = df.head(10)
        print(f"[3/3] Preview mode: showing first 10 rows", file=sys.stderr)
    else:
        print(f"[3/3] Processing {len(df)} rows...", file=sys.stderr)

    # Format output
    output = format_output(df, args.format)

    # Write output
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"      Saved to: {args.output}", file=sys.stderr)
    else:
        # Print with UTF-8 encoding to handle non-ASCII characters on Windows
        sys.stdout.reconfigure(encoding='utf-8')
        print(output)

    print(f"Done! Rows: {len(df)}, Columns: {len(df.columns)}", file=sys.stderr)


if __name__ == '__main__':
    main()
