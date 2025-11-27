#!/usr/bin/env python3
"""
Fix broken HTML pages that are missing opening structure tags.
Pages start with </ul></li> right after <body> which means the opening tags are missing.
"""

import os
import re
from pathlib import Path

def fix_broken_page(file_path):
    """Fix a single broken HTML page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page is broken (starts with </ul></li> after <body>)
        body_match = re.search(r'<body[^>]*>', content)
        if not body_match:
            return False
        
        body_end = body_match.end()
        after_body = content[body_end:].strip()
        
        # Check if it starts with closing tags (broken)
        if after_body.startswith('</ul></li>'):
            # Find where </body> is
            body_close_match = re.search(r'</body>', content)
            if not body_close_match:
                return False
            
            # Get everything between <body> and </body>
            body_content = content[body_end:body_close_match.start()]
            
            # Check if wrapper structure already exists
            if '<div id="wrapper"' in body_content or '<div class="wrapper">' in body_content:
                return False
            
            # Insert the wrapper structure right after <body>
            # Based on working index.html structure
            wrapper_start = '''	<div id="wrapper" class="fusion-wrapper">
		<div id="home" style="position:relative;top:-1px;"></div>
		<div class="fusion-tb-header">'''
            
            # Also need main content wrapper
            # Find where the main content should start (look for patterns)
            # For now, just add the wrapper and let the existing structure work
            
            # Insert wrapper after body tag
            new_content = content[:body_end] + '\n' + wrapper_start + '\n' + body_content
            
            # Close the wrapper before </body>
            body_close_pos = new_content.rfind('</body>')
            if body_close_pos > 0:
                # Check if closing tags already exist
                before_body_close = new_content[:body_close_pos].rstrip()
                if not before_body_close.endswith('</div> <!-- wrapper -->'):
                    wrapper_end = '''		</div> <!-- wrapper -->
	</div> <!-- #boxed-wrapper -->'''
                    new_content = new_content[:body_close_pos] + '\n' + wrapper_end + '\n' + new_content[body_close_pos:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Find and fix all broken HTML pages"""
    base_dir = Path('blackpropeller.com')
    html_files = list(base_dir.rglob('*.html'))
    
    fixed_count = 0
    for html_file in html_files:
        if fix_broken_page(html_file):
            print(f"Fixed: {html_file}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
