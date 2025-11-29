#!/usr/bin/env python3
"""
Fix text colors on white background sections - ensure they have dark text, not white.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_white_background_sections(file_path):
    """Fix text colors on white background sections."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find all fusion-fullwidth sections
        fullwidth_sections = soup.find_all('div', class_='fusion-fullwidth')
        
        for section in fullwidth_sections:
            # Skip header sections
            if section.find_parent('div', class_='fusion-tb-header'):
                continue
            
            style = section.get('style', '')
            
            # Check if this section has a white background
            has_white_bg = (
                '#ffffff' in style or
                '#fff' in style or
                'var(--awb-color1)' in style or
                ('--awb-background-color:#ffffff' in style) or
                ('--awb-background-color: #ffffff' in style)
            )
            
            # Check if it has a dark background (if so, skip)
            has_dark_bg = (
                'var(--awb-color5)' in style or
                'var(--awb-color7)' in style or
                '#051334' in style or
                '#0c1428' in style
            )
            
            # Only process white background sections
            if has_white_bg and not has_dark_bg:
                # Find all text elements in this section
                text_elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i'])
                
                for elem in text_elements:
                    if elem == section:
                        continue
                    
                    elem_style = elem.get('style', '')
                    
                    # If element has white color, change it to dark
                    if 'color:#ffffff' in elem_style or 'color: #ffffff' in elem_style:
                        # Remove white color
                        elem_style_clean = re.sub(r'color:\s*#ffffff\s*!important;?', '', elem_style)
                        elem_style_clean = re.sub(r'color:\s*#ffffff;?', '', elem_style_clean)
                        # Set dark color if no color remains
                        if 'color:' not in elem_style_clean:
                            if elem_style_clean:
                                elem['style'] = elem_style_clean + ';color:#051334 !important;'
                            else:
                                elem['style'] = 'color:#051334 !important;'
                        else:
                            elem['style'] = elem_style_clean
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
    print(f"Fix Text Colors on White Background Sections")
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
        
        if fix_white_background_sections(html_file):
            fixed_count += 1
            print(f"  [OK] Fixed white background text colors")
        else:
            skipped_count += 1
            print(f"  - No changes needed")
    
    print(f"\n{'='*70}")
    print(f"Fix Complete!")
    print(f"  [OK] Files updated: {fixed_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

