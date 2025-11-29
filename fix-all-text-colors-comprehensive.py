#!/usr/bin/env python3
"""
Comprehensively fix text colors - white on dark backgrounds, dark on white backgrounds.
Also remove broken concatenated text from blog posts.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

DARK_BACKGROUNDS = ['var(--awb-color5)', 'var(--awb-color7)', '#051334', '#0c1428', '#101a34']
WHITE_BACKGROUNDS = ['#ffffff', '#fff', 'var(--awb-color1)']

def has_dark_background(style_attr):
    """Check if a style attribute indicates a dark background."""
    if not style_attr:
        return False
    return any(dark_bg in style_attr for dark_bg in DARK_BACKGROUNDS)

def has_white_background(style_attr):
    """Check if a style attribute indicates a white background."""
    if not style_attr:
        return False
    return any(white_bg in style_attr for white_bg in WHITE_BACKGROUNDS)

def fix_file(file_path):
    """Fix text colors and remove broken content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # First, remove broken concatenated text from blog posts
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            post_content = soup.find('main') or soup.find('div', id='content')
        
        if post_content:
            fullwidth_sections = post_content.find_all('div', class_='fusion-fullwidth')
            for section in fullwidth_sections:
                text = section.get_text()
                if 'What We DoPaid SearchPaid' in text or 'SocialPerformance CreativeAmazon' in text:
                    print(f"    Removing broken content...")
                    section.extract()
                    modified = True
        
        # Then fix text colors
        all_fullwidth = soup.find_all('div', class_='fusion-fullwidth')
        
        for section in all_fullwidth:
            # Skip header sections
            if section.find_parent('div', class_='fusion-tb-header'):
                continue
            
            style = section.get('style', '')
            
            # Determine background type
            is_dark = has_dark_background(style)
            is_white = has_white_background(style)
            
            # If no explicit background, assume white (default)
            if not is_dark and not is_white:
                is_white = True
            
            # Find all text elements
            text_elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i', 'ol', 'ul'])
            
            for elem in text_elements:
                if elem == section:
                    continue
                
                elem_style = elem.get('style', '')
                
                if is_dark:
                    # Dark background - need white text
                    if 'color:#ffffff' not in elem_style and 'color: #ffffff' not in elem_style:
                        elem_style_clean = re.sub(r'color:[^;]+;?', '', elem_style)
                        if elem_style_clean:
                            elem['style'] = elem_style_clean + ';color:#ffffff !important;'
                        else:
                            elem['style'] = 'color:#ffffff !important;'
                        modified = True
                
                elif is_white:
                    # White background - need dark text
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
    print(f"Comprehensive Text Color Fix")
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
        
        if fix_file(html_file):
            fixed_count += 1
            print(f"  [OK] Fixed")
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

