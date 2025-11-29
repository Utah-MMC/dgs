#!/usr/bin/env python3
"""
Fix text visibility in footer banner (fusion-builder-row-17, 18, 19).
Ensure all text is visible based on background colors.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_footer_banner_text(file_path):
    """Fix text colors in footer banner sections."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find all footer banner sections (row-17, row-18, row-19)
        footer_sections = soup.find_all('div', class_=re.compile(r'fusion-builder-row-(17|18|19)'))
        
        for section in footer_sections:
            style = section.get('style', '')
            
            # Check background color
            has_dark_bg = (
                'var(--awb-color5)' in style or
                'var(--awb-color7)' in style or
                '#051334' in style or
                '#0c1428' in style
            )
            
            has_white_bg = (
                '#ffffff' in style or
                '#fff' in style or
                'var(--awb-color1)' in style
            )
            
            has_light_bg = (
                '#f3f3f3' in style or
                '#fafafa' in style or
                'rgba(255,250,249' in style  # Light pink
            )
            
            # Find all text elements in this section
            text_elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i', 'ul', 'ol'])
            
            for elem in text_elements:
                if elem == section:
                    continue
                
                elem_style = elem.get('style', '')
                
                if has_dark_bg:
                    # Dark background - need white text
                    if 'color:#ffffff' not in elem_style and 'color: #ffffff' not in elem_style:
                        elem_style_clean = re.sub(r'color:[^;]+;?', '', elem_style)
                        if elem_style_clean:
                            elem['style'] = elem_style_clean + ';color:#ffffff !important;'
                        else:
                            elem['style'] = 'color:#ffffff !important;'
                        modified = True
                
                elif has_white_bg or has_light_bg:
                    # White or light background - need dark text
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
                    elif 'color:#051334' not in elem_style and 'color: #051334' not in elem_style:
                        # No color set - add dark color
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
    print(f"Fix Footer Banner Text Visibility")
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
        
        if fix_footer_banner_text(html_file):
            fixed_count += 1
            print(f"  [OK] Fixed footer banner text")
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

