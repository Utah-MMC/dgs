#!/usr/bin/env python3
"""
Fix duplicate content and restructure content into proper Fusion Builder sections.
Removes duplicates and splits content into separate fusion-fullwidth sections.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def remove_duplicate_content(soup):
    """Remove duplicate content sections."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    modified = False
    
    # Find all fusion-fullwidth boxes in post-content
    fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
    
    if len(fullwidth_boxes) < 2:
        return False
    
    # Get the first box (the original title/description)
    first_box = fullwidth_boxes[0]
    first_text = first_box.get_text(strip=True).lower()
    
    # Check subsequent boxes for duplicates
    boxes_to_remove = []
    for i, box in enumerate(fullwidth_boxes[1:], 1):
        box_text = box.get_text(strip=True).lower()
        
        # If this box starts with the same content as the first box, it's likely a duplicate
        if box_text.startswith(first_text[:100]) or first_text[:100] in box_text[:200]:
            # Check if it's the broken content we added (has class_= or is missing proper structure)
            box_html = str(box)
            if 'class_=' in box_html or not box.find('div', class_='fusion-builder-row'):
                boxes_to_remove.append(box)
                modified = True
    
    # Remove duplicate boxes
    for box in boxes_to_remove:
        box.decompose()
    
    return modified

def restructure_content_into_sections(soup):
    """Restructure content into proper Fusion Builder sections."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Find the first fusion-fullwidth (title/description - keep this)
    first_fullwidth = post_content.find('div', class_='fusion-fullwidth')
    if not first_fullwidth:
        return False
    
    # Find all content after the first fullwidth
    # Look for the broken content section
    broken_content = None
    for sibling in first_fullwidth.next_siblings:
        if hasattr(sibling, 'name') and sibling.name == 'div':
            if 'class' in sibling.attrs and 'fusion-fullwidth' in sibling.get('class', []):
                # Check if it's broken (has class_= or missing proper structure)
                if 'class_=' in str(sibling) or not sibling.find('div', class_='fusion-builder-row'):
                    broken_content = sibling
                    break
    
    if not broken_content:
        return False
    
    # Extract all headings and content from broken section
    headings = broken_content.find_all(['h2', 'h3'])
    paragraphs = broken_content.find_all('p')
    lists = broken_content.find_all(['ul', 'ol'])
    
    # Group content by headings
    content_groups = []
    current_group = {'heading': None, 'content': []}
    
    # Process all elements in order
    all_elements = broken_content.find_all(['h2', 'h3', 'p', 'ul', 'ol'], recursive=False)
    all_elements.extend(broken_content.find_all(['div'], class_=['fusion-title', 'fusion-text']))
    
    for elem in all_elements:
        if elem.name in ['h2', 'h3']:
            # Save previous group and start new one
            if current_group['heading'] or current_group['content']:
                content_groups.append(current_group)
            current_group = {'heading': elem, 'content': []}
        else:
            current_group['content'].append(elem)
    
    # Add last group
    if current_group['heading'] or current_group['content']:
        content_groups.append(current_group)
    
    # Remove the broken content section
    broken_content.decompose()
    
    # Create new properly structured sections for each group
    for i, group in enumerate(content_groups, 1):
        if not group['heading'] and not group['content']:
            continue
        
        # Create new fusion-fullwidth section
        new_fullwidth = soup.new_tag('div')
        new_fullwidth['class'] = 'fusion-fullwidth fullwidth-box'
        
        # Create fusion-builder-row
        new_row = soup.new_tag('div')
        new_row['class'] = 'fusion-builder-row fusion-row'
        
        # Create column
        new_column = soup.new_tag('div')
        new_column['class'] = 'fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column'
        
        # Create wrapper
        new_wrapper = soup.new_tag('div')
        new_wrapper['class'] = 'fusion-column-wrapper'
        
        # Add heading if exists
        if group['heading']:
            title_wrapper = soup.new_tag('div')
            title_wrapper['class'] = 'fusion-title title'
            h_tag = soup.new_tag(group['heading'].name)
            h_tag['class'] = 'title-heading-left'
            h_tag.string = group['heading'].get_text(strip=True)
            title_wrapper.append(h_tag)
            new_wrapper.append(title_wrapper)
        
        # Add content elements
        for content_elem in group['content']:
            if content_elem.name == 'p':
                text_wrapper = soup.new_tag('div')
                text_wrapper['class'] = 'fusion-text'
                text_wrapper.append(content_elem)
                new_wrapper.append(text_wrapper)
            elif content_elem.name in ['ul', 'ol']:
                text_wrapper = soup.new_tag('div')
                text_wrapper['class'] = 'fusion-text'
                text_wrapper.append(content_elem)
                new_wrapper.append(text_wrapper)
            elif content_elem.name == 'div' and 'fusion-text' in content_elem.get('class', []):
                new_wrapper.append(content_elem)
            elif content_elem.name == 'div' and 'fusion-title' in content_elem.get('class', []):
                new_wrapper.append(content_elem)
        
        # Assemble structure
        new_column.append(new_wrapper)
        new_row.append(new_column)
        new_fullwidth.append(new_row)
        
        # Insert after first fullwidth
        first_fullwidth.insert_after(new_fullwidth)
    
    return True

def fix_all_pages():
    """Fix all pages with duplicate content and restructuring."""
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
    print(f"Fixing Duplicates and Restructuring Content")
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
            
            # Remove duplicates
            duplicates_removed = remove_duplicate_content(soup)
            
            # Restructure content
            restructured = restructure_content_into_sections(soup)
            
            if duplicates_removed or restructured:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                fixed_count += 1
                print(f"  ✓ Fixed (duplicates removed: {duplicates_removed}, restructured: {restructured})")
            else:
                print(f"  - No changes needed")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*70}")
    print(f"Fixed {fixed_count} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    fix_all_pages()

