#!/usr/bin/env python3
"""
Restore original HTML content (with accordions and images) from rewrite_progress.json.
This restores the full HTML structure scraped from blackpropeller.com.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Core pages to skip
CORE_PAGES = {
    'services/seo/index.html',
    'services/paid-search/index.html',
    'services/creative/index.html',
    'services/hubspot/index.html',
}

def is_core_page(file_path):
    """Check if this is one of the 4 core pages."""
    rel_path = str(file_path.relative_to(Path('blackpropeller.com')))
    return rel_path.replace('\\', '/') in CORE_PAGES

def load_rewrite_progress():
    """Load the rewrite progress JSON file."""
    progress_file = Path('blackpropeller.com/rewrite_progress.json')
    
    if not progress_file.exists():
        print(f"Error: {progress_file} not found!")
        return None
    
    print(f"Loading rewrite progress from {progress_file}...")
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    data = None
    
    for encoding in encodings:
        try:
            with open(progress_file, 'r', encoding=encoding, errors='replace') as f:
                data = json.load(f)
            print(f"Successfully loaded with {encoding} encoding")
            break
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            continue
    
    if data is None:
        print("Error: Could not load JSON file with any encoding!")
        return None
    
    return data

def extract_page_content_from_progress(progress_data, page_path):
    """Extract all original HTML content for a specific page."""
    if 'rewritten' not in progress_data:
        return []
    
    # Build the expected file path format (e.g., "services\index.html" or "blog\post-name\index.html")
    # Get relative path from blackpropeller.com
    try:
        rel_path = page_path.relative_to(Path('blackpropeller.com'))
        # Convert to the format used in JSON (backslashes, no leading path)
        expected_path = str(rel_path).replace('/', '\\')
    except:
        # Fallback: construct from parent directory
        if page_path.parent.name:
            expected_path = f"{page_path.parent.name}\\{page_path.name}"
        else:
            expected_path = page_path.name
    
    # Also try with forward slashes
    expected_path_alt = expected_path.replace('\\', '/')
    
    # Build list of all content items for this page
    content_items = []
    
    for item in progress_data['rewritten']:
        file_path = item.get('file', '')
        original = item.get('original', '')
        tag = item.get('tag', '')
        
        # Normalize file_path for comparison
        file_path_normalized = file_path.replace('/', '\\')
        
        # Match if the file path exactly matches or contains our expected path
        matches = False
        if file_path_normalized == expected_path or file_path == expected_path_alt:
            matches = True
        elif expected_path in file_path_normalized or expected_path_alt in file_path:
            matches = True
        # Also check if just the directory and filename match
        elif page_path.parent.name in file_path and page_path.name in file_path:
            matches = True
        
        if matches and original:
            # Check if it's HTML content (contains tags) or substantial content
            if '<' in original and '>' in original:
                content_items.append({
                    'file': file_path,
                    'tag': tag,
                    'original': original,
                    'id': item.get('id', '')
                })
            elif len(original.strip()) > 100:  # Also include substantial text content
                content_items.append({
                    'file': file_path,
                    'tag': tag,
                    'original': original,
                    'id': item.get('id', '')
                })
    
    return content_items

def reconstruct_html_from_items(content_items):
    """Reconstruct full HTML structure from content items."""
    if not content_items:
        return None
    
    # Sort items by their order in the original file (if we can determine it)
    # For now, just combine all HTML content
    html_parts = []
    
    for item in content_items:
        original = item['original'].strip()
        if original:
            # If it's already HTML, use it as-is
            if '<' in original and '>' in original:
                html_parts.append(original)
            else:
                # If it's plain text, wrap it
                html_parts.append(f'<p>{original}</p>')
    
    if not html_parts:
        return None
    
    # Combine all HTML parts
    combined_html = '\n'.join(html_parts)
    
    # Parse to ensure valid HTML structure
    soup = BeautifulSoup(combined_html, 'html.parser')
    
    return soup

def restore_page_from_original(file_path, progress_data):
    """Restore a page using original HTML content from rewrite progress."""
    try:
        # Skip core pages
        if is_core_page(file_path):
            return 'skipped_core'
        
        # Extract original content for this page
        content_items = extract_page_content_from_progress(progress_data, file_path)
        
        if not content_items:
            return 'skipped_no_content'
        
        # Reconstruct HTML
        original_soup = reconstruct_html_from_items(content_items)
        
        if not original_soup:
            return 'skipped_no_html'
        
        # Read current page
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the content area
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            return 'skipped_no_post_content'
        
        # Find the first fusion-fullwidth (title/description section)
        first_fullwidth = post_content.find('div', class_='fusion-fullwidth')
        if not first_fullwidth:
            return 'skipped_no_fullwidth'
        
        # Remove all content after the first fullwidth (the simple text we added)
        # Keep only the first fullwidth
        for sibling in list(first_fullwidth.next_siblings):
            if hasattr(sibling, 'extract'):
                sibling.extract()
        
        # Now insert the original HTML content after the first fullwidth
        # Wrap it in a fusion-fullwidth container with proper styling
        new_fullwidth = soup.new_tag('div')
        new_fullwidth['class'] = 'fusion-fullwidth fullwidth-box'
        new_fullwidth['style'] = '--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:#ffffff;'
        
        new_row = soup.new_tag('div')
        new_row['class'] = 'fusion-builder-row fusion-row'
        
        new_column = soup.new_tag('div')
        new_column['class'] = 'fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column'
        
        new_wrapper = soup.new_tag('div')
        new_wrapper['class'] = 'fusion-column-wrapper'
        
        # Insert the original HTML content
        for element in original_soup.children:
            if hasattr(element, 'name') and element.name:
                new_wrapper.append(element)
        
        new_column.append(new_wrapper)
        new_row.append(new_column)
        new_fullwidth.append(new_row)
        
        # Insert after first fullwidth
        first_fullwidth.insert_after(new_fullwidth)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return 'restored'
    
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return 'error'

def main():
    """Main restoration process."""
    print(f"{'='*70}")
    print(f"Restore Original HTML from Scraped Content")
    print(f"{'='*70}")
    
    # Load rewrite progress
    progress_data = load_rewrite_progress()
    if not progress_data:
        return
    
    total_items = len(progress_data.get('rewritten', []))
    print(f"Loaded {total_items} items from rewrite progress\n")
    
    # Find all index.html files
    base_dir = Path('blackpropeller.com')
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} pages to check\n")
    print(f"Core pages to skip:")
    print(f"  - /services/seo/")
    print(f"  - /services/paid-search/")
    print(f"  - /services/creative/")
    print(f"  - /services/hubspot/")
    print()
    
    stats = {
        'restored': 0,
        'skipped_core': 0,
        'skipped_no_content': 0,
        'skipped_no_html': 0,
        'skipped_no_post_content': 0,
        'skipped_no_fullwidth': 0,
        'error': 0
    }
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        result = restore_page_from_original(html_file, progress_data)
        
        if result == 'restored':
            stats['restored'] += 1
            print(f"  [OK] Restored original HTML content")
        elif result == 'skipped_core':
            stats['skipped_core'] += 1
            print(f"  - Skipped (core page)")
        elif result == 'skipped_no_content':
            stats['skipped_no_content'] += 1
            print(f"  - Skipped (no original content found)")
        elif result == 'skipped_no_html':
            stats['skipped_no_html'] += 1
            print(f"  - Skipped (no HTML content)")
        elif result == 'skipped_no_post_content':
            stats['skipped_no_post_content'] += 1
            print(f"  - Skipped (no post-content div)")
        elif result == 'skipped_no_fullwidth':
            stats['skipped_no_fullwidth'] += 1
            print(f"  - Skipped (no fusion-fullwidth found)")
        elif result == 'error':
            stats['error'] += 1
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  [OK] Restored: {stats['restored']} pages")
    print(f"  - Skipped (core pages): {stats['skipped_core']} pages")
    print(f"  - Skipped (no content): {stats['skipped_no_content']} pages")
    print(f"  - Skipped (no HTML): {stats['skipped_no_html']} pages")
    print(f"  - Skipped (structure issues): {stats['skipped_no_post_content'] + stats['skipped_no_fullwidth']} pages")
    if stats['error'] > 0:
        print(f"  [ERROR] Errors: {stats['error']} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

