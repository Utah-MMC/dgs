#!/usr/bin/env python3
"""
Fix broken blog posts (remove concatenated text) and fix text colors 
so white text only appears on dark backgrounds, not white backgrounds.
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

def has_white_background(style_attr):
    """Check if a style attribute indicates a white background."""
    if not style_attr:
        return False
    
    white_bg_patterns = [
        '#ffffff',
        '#fff',
        'var(--awb-color1)',
    ]
    
    for white_bg in white_bg_patterns:
        if white_bg in style_attr:
            return True
    
    return False

def fix_blog_post(file_path):
    """Remove broken concatenated text from blog posts."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find post-content
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            post_content = soup.find('main') or soup.find('div', id='content')
        
        if not post_content:
            return False
        
        # Find all fusion-fullwidth sections
        fullwidth_sections = post_content.find_all('div', class_='fusion-fullwidth')
        
        for section in fullwidth_sections:
            # Check for broken concatenated text
            text = section.get_text()
            if 'What We DoPaid SearchPaid' in text or 'SocialPerformance CreativeAmazon' in text:
                # This is broken content - remove it
                print(f"    Found broken content, removing...")
                section.extract()
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def fix_text_colors(file_path):
    """Fix text colors - white on dark backgrounds, dark on white backgrounds."""
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
            
            # Check if this section has a dark background
            if has_dark_background(style):
                # Find all text elements in this section
                text_elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i'])
                
                for elem in text_elements:
                    if elem == section:
                        continue
                    
                    elem_style = elem.get('style', '')
                    
                    # Set white color for dark backgrounds
                    if 'color:#ffffff' not in elem_style and 'color: #ffffff' not in elem_style:
                        elem_style_clean = re.sub(r'color:[^;]+;?', '', elem_style)
                        if elem_style_clean:
                            elem['style'] = elem_style_clean + ';color:#ffffff !important;'
                        else:
                            elem['style'] = 'color:#ffffff !important;'
                        modified = True
            
            # Check if this section has a white background
            elif has_white_background(style) or not has_dark_background(style):
                # Find all text elements in this section
                text_elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div', 'a', 'strong', 'b', 'em', 'i'])
                
                for elem in text_elements:
                    if elem == section:
                        continue
                    
                    elem_style = elem.get('style', '')
                    
                    # Remove white color and set dark color for white backgrounds
                    if 'color:#ffffff' in elem_style or 'color: #ffffff' in elem_style:
                        # Remove white color
                        elem_style_clean = re.sub(r'color:\s*#ffffff\s*!important;?', '', elem_style)
                        elem_style_clean = re.sub(r'color:\s*#ffffff;?', '', elem_style_clean)
                        # Set dark color
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
    print(f"Fix Blog Posts and Text Colors")
    print(f"{'='*70}")
    print()
    
    base_dir = Path('blackpropeller.com')
    
    # First, fix blog posts
    print("1. Fixing broken blog posts...")
    blog_files = []
    for blog_file in (base_dir / 'blog').rglob('index.html'):
        blog_files.append(blog_file)
    
    print(f"Found {len(blog_files)} blog posts to check\n")
    
    blog_fixed = 0
    for i, blog_file in enumerate(blog_files, 1):
        rel_path = blog_file.relative_to(base_dir)
        print(f"[{i}/{len(blog_files)}] Processing: {rel_path}")
        
        if fix_blog_post(blog_file):
            blog_fixed += 1
            print(f"  [OK] Removed broken content")
        else:
            print(f"  - No broken content found")
    
    print(f"\nFixed {blog_fixed} blog posts\n")
    
    # Then, fix text colors on all pages
    print("2. Fixing text colors on all pages...")
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    color_fixed = 0
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        if fix_text_colors(html_file):
            color_fixed += 1
            print(f"  [OK] Fixed text colors")
        else:
            print(f"  - No changes needed")
    
    print(f"\n{'='*70}")
    print(f"Fix Complete!")
    print(f"  [OK] Blog posts fixed: {blog_fixed}")
    print(f"  [OK] Files with text color fixes: {color_fixed}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

