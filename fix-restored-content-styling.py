#!/usr/bin/env python3
"""
Fix CSS styling for all restored content sections to match homepage format.
This will add proper padding, background colors, and wrap content in fusion-text divs.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
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

def fix_content_styling(file_path):
    """Fix CSS styling for restored content sections."""
    try:
        # Skip core pages
        if is_core_page(file_path):
            return 'skipped_core'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            return 'skipped_no_post_content'
        
        modified = False
        fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
        
        for box in fullwidth_boxes:
            # Check if this box has h2 tags (restored content indicator)
            h2_tags = box.find_all('h2')
            if h2_tags:
                # Check if it needs styling
                style = box.get('style', '')
                needs_styling = '--awb-padding-top' not in style
                
                if needs_styling:
                    # Add homepage-style CSS
                    new_style = '--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:#ffffff;'
                    if style:
                        if not style.strip().endswith(';'):
                            style += ';'
                        box['style'] = style + ' ' + new_style
                    else:
                        box['style'] = new_style
                    modified = True
                
                # Ensure content is wrapped in fusion-text div
                fusion_text = box.find('div', class_='fusion-text')
                if not fusion_text:
                    # Find the fusion-column-wrapper
                    wrapper = box.find('div', class_='fusion-column-wrapper')
                    if wrapper:
                        # Check if there's content directly in wrapper (h2, p, ul, etc.)
                        has_direct_content = False
                        for child in wrapper.children:
                            if hasattr(child, 'name'):
                                if child.name in ['h2', 'h3', 'h4', 'p', 'ul', 'ol']:
                                    has_direct_content = True
                                    break
                                elif child.name == 'div' and child.get('class') and 'fusion-text' not in ' '.join(child.get('class', [])):
                                    if child.find('h2') or child.find('p'):
                                        has_direct_content = True
                                        break
                        
                        if has_direct_content:
                            # Create fusion-text wrapper
                            fusion_text = soup.new_tag('div')
                            fusion_text['class'] = 'fusion-text'
                            fusion_text['style'] = 'margin-top:40px;'
                            
                            # Collect all content elements to wrap
                            content_elements = []
                            for child in list(wrapper.children):
                                if hasattr(child, 'name'):
                                    if child.name in ['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'span']:
                                        content_elements.append(child)
                                    elif child.name == 'div':
                                        # Check if it's a content div (not fusion-text or other structural divs)
                                        child_classes = child.get('class', [])
                                        if 'fusion-text' not in ' '.join(child_classes) and 'fusion-title' not in ' '.join(child_classes):
                                            if child.find('h2') or child.find('p'):
                                                content_elements.append(child)
                            
                            # Move content into fusion-text
                            if content_elements:
                                for elem in content_elements:
                                    fusion_text.append(elem.extract())
                                wrapper.insert(0, fusion_text)
                                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return 'updated'
        
        return 'skipped_no_changes'
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 'error'

def main():
    """Main process."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    # Find all index.html files
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"{'='*70}")
    print(f"Fix CSS Styling for Restored Content")
    print(f"{'='*70}")
    print(f"Core pages to skip:")
    print(f"  - /services/seo/")
    print(f"  - /services/paid-search/")
    print(f"  - /services/creative/")
    print(f"  - /services/hubspot/")
    print(f"\nFound {len(html_files)} pages to check\n")
    
    stats = {
        'updated': 0,
        'skipped_core': 0,
        'skipped_no_post_content': 0,
        'skipped_no_changes': 0,
        'error': 0
    }
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        result = fix_content_styling(html_file)
        
        if result == 'updated':
            stats['updated'] += 1
            print(f"  ✓ Fixed CSS styling")
        elif result == 'skipped_core':
            stats['skipped_core'] += 1
            print(f"  - Skipped (core page)")
        elif result == 'skipped_no_post_content':
            stats['skipped_no_post_content'] += 1
            print(f"  - Skipped (no post-content div)")
        elif result == 'skipped_no_changes':
            stats['skipped_no_changes'] += 1
            print(f"  - Skipped (already styled)")
        elif result == 'error':
            stats['error'] += 1
    
    print(f"\n{'='*70}")
    print(f"Styling Fix Complete!")
    print(f"  ✓ Updated: {stats['updated']} pages")
    print(f"  - Skipped (core pages): {stats['skipped_core']} pages")
    print(f"  - Skipped (already styled): {stats['skipped_no_changes']} pages")
    if stats['error'] > 0:
        print(f"  ✗ Errors: {stats['error']} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

