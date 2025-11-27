#!/usr/bin/env python3
"""Direct fix for empty headers"""

from pathlib import Path
import re

# Read the header from index.html
index_path = Path('blackpropeller.com/index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract header content (everything between fusion-tb-header opening and closing)
header_match = re.search(r'<div class="fusion-tb-header">(.*?)</div>\s*<div id="sliders-container"', index_content, re.DOTALL)
if not header_match:
    print("Could not find header in index.html")
    exit(1)

header_content = header_match.group(1).strip()
print(f"Header content length: {len(header_content)}")

# Find all HTML files
base_dir = Path('blackpropeller.com')
html_files = [f for f in base_dir.rglob('*.html') if f.name != 'index.html' or 'index.html' not in str(f.parent)]

fixed = 0
for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for empty header pattern
        if '<div class="fusion-tb-header">' in content and '</div>' in content:
            # Find the header section
            header_start = content.find('<div class="fusion-tb-header">')
            if header_start >= 0:
                # Find the closing </div> for the header
                header_end_tag = content.find('</div>', header_start)
                if header_end_tag > header_start:
                    header_section = content[header_start:header_end_tag + 6]
                    # Check if it's empty (just whitespace/newlines between tags)
                    inner = content[header_start + len('<div class="fusion-tb-header">'):header_end_tag].strip()
                    if not inner or inner in ['\n', '\n\n', '']:
                        # Replace with full header
                        new_header = f'<div class="fusion-tb-header">{header_content}</div>'
                        content = content[:header_start] + new_header + content[header_end_tag + 6:]
                        
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed: {html_file}")
                        fixed += 1
    except Exception as e:
        print(f"Error with {html_file}: {e}")

print(f"\nFixed {fixed} files")

