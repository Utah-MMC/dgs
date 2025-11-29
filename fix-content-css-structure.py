#!/usr/bin/env python3
"""
Fix content CSS structure by wrapping headings, paragraphs, and lists
with proper Fusion Builder CSS classes.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_content_css_structure(html_content):
    """Fix CSS structure for restored content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    modified = False
    
    # Find all post-content sections
    post_contents = soup.find_all('div', class_='post-content')
    
    for post_content in post_contents:
        # Find all fusion-fullwidth boxes in post-content
        fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
        
        for fullwidth in fullwidth_boxes:
            # Find fusion-column-wrapper
            column_wrapper = fullwidth.find('div', class_='fusion-column-wrapper')
            if not column_wrapper:
                continue
            
            # Process all direct children of column-wrapper
            children = list(column_wrapper.children)
            
            for child in children:
                if not hasattr(child, 'name'):
                    continue
                
                # If it's an h2, wrap it in fusion-title
                if child.name == 'h2':
                    # Check if already wrapped
                    if child.parent and child.parent.get('class') and 'fusion-title' in child.parent.get('class'):
                        continue
                    
                    # Create wrapper
                    title_wrapper = soup.new_tag('div')
                    title_wrapper['class'] = 'fusion-title title'
                    
                    # Add class to h2 if not present
                    if not child.get('class'):
                        child['class'] = 'title-heading-left'
                    elif 'title-heading-left' not in child.get('class', []):
                        child['class'].append('title-heading-left')
                    
                    # Wrap the h2
                    child.insert_before(title_wrapper)
                    title_wrapper.append(child.extract())
                    modified = True
                
                # If it's a p, wrap it in fusion-text
                elif child.name == 'p':
                    # Check if already wrapped
                    if child.parent and child.parent.get('class') and 'fusion-text' in child.parent.get('class'):
                        continue
                    
                    # Check if next sibling is also a p or list - group them
                    siblings_to_group = [child]
                    next_sibling = child.next_sibling
                    
                    while next_sibling and hasattr(next_sibling, 'name'):
                        if next_sibling.name in ['p', 'ul', 'ol']:
                            siblings_to_group.append(next_sibling)
                            next_sibling = next_sibling.next_sibling
                        else:
                            break
                    
                    # Create wrapper for grouped elements
                    text_wrapper = soup.new_tag('div')
                    text_wrapper['class'] = 'fusion-text'
                    
                    # Wrap all grouped elements
                    for elem in siblings_to_group:
                        elem.insert_before(text_wrapper)
                        text_wrapper.append(elem.extract())
                    
                    modified = True
                
                # If it's a ul or ol, wrap it in fusion-text
                elif child.name in ['ul', 'ol']:
                    # Check if already wrapped
                    if child.parent and child.parent.get('class') and 'fusion-text' in child.parent.get('class'):
                        continue
                    
                    # Create wrapper
                    text_wrapper = soup.new_tag('div')
                    text_wrapper['class'] = 'fusion-text'
                    
                    # Wrap the list
                    child.insert_before(text_wrapper)
                    text_wrapper.append(child.extract())
                    modified = True
    
    return str(soup), modified

def fix_all_pages():
    """Fix CSS structure for all pages."""
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
    print(f"Fixing CSS Structure for Content")
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
            
            # Fix CSS structure
            html_content, modified = fix_content_css_structure(html_content)
            
            if modified:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                fixed_count += 1
                print(f"  ✓ Fixed CSS structure")
            else:
                print(f"  - No changes needed")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print(f"\n{'='*70}")
    print(f"Fixed CSS structure for {fixed_count} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    fix_all_pages()

