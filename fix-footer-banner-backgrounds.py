#!/usr/bin/env python3
"""
Fix footer banner backgrounds - ensure row-19 (copyright) has proper background color.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_footer_banner_backgrounds(file_path):
    """Fix background colors in footer banner sections."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find row-19 (copyright section)
        row_19 = soup.find('div', class_=re.compile(r'fusion-builder-row-19'))
        
        if row_19:
            style = row_19.get('style', '')
            
            # Check if background color is missing or incomplete
            if '--awb-background-color:' not in style or '--awb-background-' in style and '--awb-background-color:' not in style:
                # Add white background for copyright section
                if style:
                    # Remove incomplete background attribute
                    style = re.sub(r'--awb-background-[^;]*;?', '', style)
                    style = style.rstrip(';')
                    if style:
                        style += ';--awb-background-color:#ffffff;'
                    else:
                        style = '--awb-background-color:#ffffff;'
                else:
                    style = '--awb-background-color:#ffffff;'
                
                row_19['style'] = style
                modified = True
                
                # Ensure text is dark on white background
                text_elements = row_19.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i'])
                for elem in text_elements:
                    if elem == row_19:
                        continue
                    elem_style = elem.get('style', '')
                    if 'color:#051334' not in elem_style and 'color: #051334' not in elem_style:
                        elem_style_clean = re.sub(r'color:[^;]+;?', '', elem_style)
                        if elem_style_clean:
                            elem['style'] = elem_style_clean + ';color:#051334 !important;'
                        else:
                            elem['style'] = 'color:#051334 !important;'
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
    print(f"Fix Footer Banner Backgrounds")
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
        
        if fix_footer_banner_backgrounds(html_file):
            fixed_count += 1
            print(f"  [OK] Fixed footer banner background")
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

