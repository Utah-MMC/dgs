#!/usr/bin/env python3
"""
Fix text color on dark background sections to ensure readability.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Dark background colors that need white text
DARK_BACKGROUNDS = [
    'var(--awb-color5)',
    'var(--awb-color7)',
    '#051334',
    '#0c1428',
    '#101a34',
]

def has_dark_background(style_attr):
    """Check if a style attribute indicates a dark background."""
    if not style_attr:
        return False
    
    for dark_bg in DARK_BACKGROUNDS:
        if dark_bg in style_attr:
            return True
    
    return False

def fix_text_color_in_section(file_path):
    """Fix text color in sections with dark backgrounds."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find all fusion-fullwidth sections
        fullwidth_sections = soup.find_all('div', class_='fusion-fullwidth')
        
        for section in fullwidth_sections:
            style = section.get('style', '')
            
            # Check if this section has a dark background
            if has_dark_background(style):
                # Find all text elements in this section (including nested ones)
                text_elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i'])
                
                for elem in text_elements:
                    # Skip if it's the section itself
                    if elem == section:
                        continue
                    
                    elem_style = elem.get('style', '')
                    
                    # Check if element already has a color set (and it's not already white)
                    if 'color:#ffffff' not in elem_style and 'color: #ffffff' not in elem_style:
                        # Add white color
                        if elem_style:
                            # Remove any existing color declarations first
                            elem_style_clean = re.sub(r'color:[^;]+;?', '', elem_style)
                            elem['style'] = elem_style_clean + ';color:#ffffff !important;'
                        else:
                            elem['style'] = 'color:#ffffff !important;'
                        modified = True
                
                # Also set color on the section itself if it doesn't have one
                if 'color:#ffffff' not in style and 'color: #ffffff' not in style:
                    if style:
                        section['style'] = style + ';--awb-text-color:#ffffff !important;color:#ffffff !important;'
                    else:
                        section['style'] = '--awb-text-color:#ffffff !important;color:#ffffff !important;'
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def main():
    """Main function."""
    print(f"{'='*70}")
    print(f"Fix Text Color on Dark Background Sections")
    print(f"{'='*70}")
    print()
    
    base_dir = Path('blackpropeller.com')
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        if fix_text_color_in_section(html_file):
            fixed_count += 1
            print(f"  [OK] Fixed text colors")
        else:
            skipped_count += 1
            print(f"  - No changes needed")
    
    print(f"\n{'='*70}")
    print(f"Text Color Fix Complete!")
    print(f"  [OK] Files updated: {fixed_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

