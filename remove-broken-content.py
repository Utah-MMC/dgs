#!/usr/bin/env python3
"""
Remove all broken/duplicate content that was incorrectly added.
This will clean up pages to their original state (just title/description).
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def remove_broken_content(soup):
    """Remove broken/duplicate content sections."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    modified = False
    
    # Find all fusion-fullwidth boxes in post-content
    fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
    
    if len(fullwidth_boxes) < 2:
        return False
    
    # Keep the first box (original title/description)
    first_box = fullwidth_boxes[0]
    
    # Remove all subsequent boxes that are broken or duplicates
    for box in fullwidth_boxes[1:]:
        box_html = str(box)
        
        # Check if it's broken (has class_=, missing proper structure, or is duplicate)
        is_broken = (
            'class_=' in box_html or
            not box.find('div', class_='fusion-builder-row') or
            'About ' in box.get_text() and 'Why Choose Our' in box.get_text()
        )
        
        if is_broken:
            box.decompose()
            modified = True
    
    return modified

def fix_all_pages():
    """Remove broken content from all pages."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"{'='*70}")
    print(f"Removing Broken/Duplicate Content")
    print(f"{'='*70}")
    print(f"Found {len(html_files)} pages to process\n")
    
    fixed_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Fix broken HTML attributes first
            html_content = re.sub(r'class_="([^"]*)"', r'class="\1"', html_content)
            html_content = re.sub(r"class_='([^']*)'", r"class='\1'", html_content)
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove broken content
            if remove_broken_content(soup):
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                fixed_count += 1
                print(f"  ✓ Removed broken content")
            else:
                print(f"  - No broken content found")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*70}")
    print(f"Removed broken content from {fixed_count} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    fix_all_pages()

