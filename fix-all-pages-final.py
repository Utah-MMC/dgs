#!/usr/bin/env python3
"""
Comprehensive fix for all broken pages:
1. Restore header content to pages with empty headers
2. Ensure proper structure
"""

import re
from pathlib import Path

# Extract header from index.html
def get_header_template():
    """Get the header HTML from index.html"""
    index_path = Path('blackpropeller.com/index.html')
    if not index_path.exists():
        return None
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the header section
    match = re.search(r'<div class="fusion-tb-header">(.*?)</div>\s*<div id="sliders-container"', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def fix_page_header(file_path, header_content):
    """Fix a single page's header"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if header is empty - match the exact pattern we see
        # Pattern: <div class="fusion-tb-header">\n\n</div> or similar
        pattern = r'<div class="fusion-tb-header">\s*\n?\s*</div>'
        
        if re.search(pattern, content):
            # Replace empty header with full header
            replacement = f'<div class="fusion-tb-header">{header_content}</div>'
            content = re.sub(pattern, replacement, content)
            fixed = True
        else:
            fixed = False
        
        if fixed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all broken pages"""
    header_content = get_header_template()
    if not header_content:
        print("ERROR: Could not extract header from index.html")
        return
    
    base_dir = Path('blackpropeller.com')
    html_files = list(base_dir.rglob('*.html'))
    
    # Skip index.html itself
    html_files = [f for f in html_files if f.name != 'index.html' or 'index.html' not in str(f)]
    
    fixed_count = 0
    for html_file in html_files:
        if fix_page_header(html_file, header_content):
            print(f"Fixed: {html_file}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()

