#!/usr/bin/env python3
"""
Convert all markdown files in the Promo folder to HTML with nice styling.
"""
import os
import re
from pathlib import Path
import markdown
from datetime import datetime


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 60px;
            border-radius: 16px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
        }}
        h1 {{
            font-size: 42px;
            color: #1a1a1a;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}
        h2 {{
            font-size: 32px;
            color: #1a1a1a;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }}
        h3 {{
            font-size: 24px;
            color: #333;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        h4 {{
            font-size: 20px;
            color: #444;
            margin-top: 25px;
            margin-bottom: 12px;
        }}
        h5 {{
            font-size: 18px;
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        h6 {{
            font-size: 16px;
            color: #666;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        p {{
            color: #555;
            font-size: 16px;
            margin-bottom: 16px;
            line-height: 1.8;
        }}
        a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px solid #667eea;
            transition: all 0.3s ease;
        }}
        a:hover {{
            color: #764ba2;
            border-bottom-color: #764ba2;
        }}
        ul, ol {{
            margin: 20px 0 20px 30px;
            color: #555;
        }}
        li {{
            margin-bottom: 10px;
            line-height: 1.7;
        }}
        code {{
            background: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            color: #e74c3c;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            line-height: 1.5;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
            font-size: 14px;
        }}
        blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 25px 0;
            color: #666;
            font-style: italic;
            background: #f8f9fa;
            padding: 20px 20px 20px 25px;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        table tbody tr:hover {{
            background-color: #f8f9fa;
        }}
        table tbody tr:last-child td {{
            border-bottom: none;
        }}
        hr {{
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 40px 0;
        }}
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 20px;
        }}
        .info-box {{
            background: #e8f4f8;
            border-left: 4px solid #0066cc;
            padding: 20px;
            margin: 25px 0;
            border-radius: 4px;
        }}
        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ff9800;
            padding: 20px;
            margin: 25px 0;
            border-radius: 4px;
        }}
        .success-box {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 20px;
            margin: 25px 0;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #999;
            font-size: 14px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        strong {{
            color: #333;
            font-weight: 600;
        }}
        em {{
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p>Vatican Vault v2.0 — Digital Forensics Platform</p>
            <p style="margin-top: 10px;">Generated: {date}</p>
        </div>
    </div>
</body>
</html>
"""


def convert_markdown_to_html(md_file_path: Path, output_path: Path = None):
    """Convert a markdown file to styled HTML."""

    # Read markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title from first # heading or use filename
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
    else:
        title = md_file_path.stem.replace('_', ' ').title()

    # Convert markdown to HTML with extensions
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'tables',
        'fenced_code',
        'nl2br',
        'sane_lists',
        'toc'
    ])
    html_content = md.convert(md_content)

    # Generate full HTML with template
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    # Determine output path
    if output_path is None:
        output_path = md_file_path.with_suffix('.html')

    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✓ Converted: {md_file_path.name} → {output_path.name}")
    return output_path


def convert_all_markdown_files(base_dir: Path):
    """Convert all markdown files in the Promo directory to HTML."""

    print("=" * 60)
    print("Converting Markdown Files to HTML")
    print("=" * 60)
    print()

    # Find all markdown files
    md_files = list(base_dir.rglob('*.md'))

    if not md_files:
        print("No markdown files found.")
        return

    print(f"Found {len(md_files)} markdown file(s)\n")

    converted_count = 0
    for md_file in md_files:
        try:
            convert_markdown_to_html(md_file)
            converted_count += 1
        except Exception as e:
            print(f"✗ Error converting {md_file.name}: {e}")

    print()
    print("=" * 60)
    print(f"Conversion Complete: {converted_count}/{len(md_files)} files")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Update VC_DEMO_INDEX.html to link to .html instead of .md files")
    print("2. Verify all links open in new tabs (target='_blank')")
    print()


if __name__ == "__main__":
    # Get the Promo directory
    promo_dir = Path(__file__).parent

    # Convert all markdown files
    convert_all_markdown_files(promo_dir)
