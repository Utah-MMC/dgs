#!/usr/bin/env python3
"""
Add proper CSS styling to restored content sections to match homepage format.
This will update the fusion-fullwidth boxes that contain restored content.
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

def has_restored_content(soup):
    """Check if page has restored content that needs styling."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Find all fusion-fullwidth boxes
    fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
    
    # Check if any box has content but no proper styling
    for box in fullwidth_boxes:
        # Check if it has h2 tags (restored content indicator)
        h2_tags = box.find_all('h2')
        if h2_tags:
            # Check if it has proper styling
            style = box.get('style', '')
            if '--awb-padding-top' not in style or '--awb-background-color' not in style:
                return True
    
    return False

def add_styling_to_content(file_path):
    """Add proper CSS styling to restored content sections."""
    try:
        # Skip core pages
        if is_core_page(file_path):
            return 'skipped_core'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        if not has_restored_content(soup):
            return 'skipped_no_restored_content'
        
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            return 'skipped_no_post_content'
        
        modified = False
        fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
        
        for box in fullwidth_boxes:
            # Check if this box has restored content (h2 tags)
            h2_tags = box.find_all('h2')
            if h2_tags:
                # Check if it needs styling
                style = box.get('style', '')
                needs_styling = '--awb-padding-top' not in style or '--awb-background-color' not in style
                
                # Check if it's the first box (title/description) - keep it as is
                is_first = box == fullwidth_boxes[0]
                
                # Only style if it's not the first box OR if it's the first box but has no styling at all
                if not is_first or (is_first and needs_styling and not style):
                    # This is restored content - add styling
                    new_style = '--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:#ffffff;'
                    if style:
                        # Merge styles properly
                        if style.strip().endswith(';'):
                            box['style'] = style + ' ' + new_style
                        else:
                            box['style'] = style + ';' + new_style
                    else:
                        box['style'] = new_style
                    
                    # Ensure content is wrapped in fusion-text div
                    fusion_text = box.find('div', class_='fusion-text')
                    if not fusion_text:
                        # Find the fusion-column-wrapper
                        wrapper = box.find('div', class_='fusion-column-wrapper')
                        if wrapper:
                            # Get all children that need to be wrapped
                            children_to_wrap = []
                            for child in list(wrapper.children):
                                # Include text nodes, h2, p, ul, ol, and other content elements
                                if isinstance(child, str) and child.strip():
                                    children_to_wrap.append(child)
                                elif hasattr(child, 'name') and child.name:
                                    if child.name in ['h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'a']:
                                        children_to_wrap.append(child)
                                    elif child.name == 'div' and child.get('class') and 'fusion-text' not in ' '.join(child.get('class', [])):
                                        # Check if this div contains h2 or other content
                                        if child.find('h2') or child.find('p'):
                                            children_to_wrap.append(child)
                            
                            if children_to_wrap:
                                # Wrap content in fusion-text
                                fusion_text = soup.new_tag('div')
                                fusion_text['class'] = 'fusion-text'
                                fusion_text['style'] = 'margin-top:40px;'
                                
                                # Move all content into fusion-text
                                for child in children_to_wrap:
                                    if isinstance(child, str):
                                        fusion_text.append(child)
                                    else:
                                        fusion_text.append(child.extract())
                                
                                if len(fusion_text.contents) > 0:
                                    wrapper.insert(0, fusion_text)
                                    modified = True
                    
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
    print(f"Add CSS Styling to Restored Content")
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
        'skipped_no_restored_content': 0,
        'skipped_no_post_content': 0,
        'skipped_no_changes': 0,
        'error': 0
    }
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        result = add_styling_to_content(html_file)
        
        if result == 'updated':
            stats['updated'] += 1
            print(f"  ✓ Added CSS styling")
        elif result == 'skipped_core':
            stats['skipped_core'] += 1
            print(f"  - Skipped (core page)")
        elif result == 'skipped_no_restored_content':
            stats['skipped_no_restored_content'] += 1
            print(f"  - Skipped (no restored content found)")
        elif result == 'skipped_no_post_content':
            stats['skipped_no_post_content'] += 1
            print(f"  - Skipped (no post-content div)")
        elif result == 'skipped_no_changes':
            stats['skipped_no_changes'] += 1
            print(f"  - Skipped (already has styling)")
        elif result == 'error':
            stats['error'] += 1
    
    print(f"\n{'='*70}")
    print(f"Styling Update Complete!")
    print(f"  ✓ Updated: {stats['updated']} pages")
    print(f"  - Skipped (core pages): {stats['skipped_core']} pages")
    print(f"  - Skipped (no restored content): {stats['skipped_no_restored_content']} pages")
    print(f"  - Skipped (already styled): {stats['skipped_no_changes']} pages")
    if stats['error'] > 0:
        print(f"  ✗ Errors: {stats['error']} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

