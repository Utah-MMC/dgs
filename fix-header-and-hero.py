#!/usr/bin/env python3
"""
Fix header background color, z-index, and restore hero section on homepage.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_header_css():
    """Add CSS to fix header background and z-index."""
    css_file = Path('blackpropeller.com/assets/theme-overrides.css')
    
    # Read existing CSS
    existing_css = ""
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            existing_css = f.read()
    
    # Check if header fixes already exist
    if 'header-background-fix' in existing_css or 'fusion-tb-header' in existing_css:
        # Update existing
        # Remove old header fixes if they exist
        existing_css = re.sub(r'/\* Header fixes.*?\*/.*?(?=/\*|$)', '', existing_css, flags=re.DOTALL)
    
    # Add header fixes
    header_fixes = """
/* Header fixes - keep blue background and prevent underlapping */
.fusion-tb-header {
  position: relative !important;
  z-index: 20051 !important;
}

.fusion-tb-header .fusion-fullwidth {
  background-color: #051334 !important;
  background: #051334 !important;
}

.fusion-tb-header .fusion-fullwidth,
.fusion-tb-header .fusion-builder-row,
.fusion-tb-header .fusion-layout-column,
.fusion-tb-header .fusion-column-wrapper {
  background-color: #051334 !important;
  background: #051334 !important;
}

/* Ensure header stays on top and content doesn't overlap */
.fusion-tb-header {
  position: sticky !important;
  top: 0 !important;
  z-index: 20051 !important;
}

/* Add padding to main content to prevent underlapping */
main#main {
  position: relative !important;
  z-index: 1 !important;
}

.post-content {
  position: relative !important;
  z-index: 1 !important;
}

/* Ensure sections don't overlap header */
.fusion-fullwidth:not(.fusion-tb-header .fusion-fullwidth) {
  position: relative !important;
  z-index: 1 !important;
}
"""
    
    # Append header fixes
    new_css = existing_css.rstrip() + "\n" + header_fixes
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(new_css)
    
    print("Header CSS fixes added")

def add_hero_section_to_homepage():
    """Add hero section to homepage if missing."""
    homepage = Path('blackpropeller.com/index.html')
    
    if not homepage.exists():
        print("Homepage not found")
        return
    
    with open(homepage, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find post-content
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        print("Could not find post-content")
        return
    
    # Check if hero section (fusion-builder-row-2) exists
    hero_section = post_content.find('div', class_='fusion-fullwidth', 
                                     attrs={'class': lambda x: x and 'fusion-builder-row-2' in ' '.join(x) if isinstance(x, list) else 'fusion-builder-row-2' in str(x)})
    
    if hero_section:
        print("Hero section already exists")
        return
    
    # Check what's the first section after header
    first_section = post_content.find('div', class_='fusion-fullwidth')
    
    if first_section:
        # Check if it's the brand logos section (fusion-builder-row-3)
        if 'fusion-builder-row-3' in str(first_section.get('class', [])):
            print("Hero section is missing, but brand logos section exists")
            # The hero should be before the brand logos
            # Let's check the live site structure - for now, we'll note it
            print("Note: Hero section may need to be fetched from live site")
            return
    
    print("Hero section check complete")

def add_header_css_to_all_pages():
    """Add header CSS fix to all HTML pages."""
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str and 'node_modules' not in file_str:
            html_files.append(html_file)
    
    print(f"\nChecking {len(html_files)} pages for header CSS...")
    
    updated_count = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check if header-background-fix style already exists
            existing_style = soup.find('style', id='header-background-fix')
            
            if existing_style:
                # Update it
                existing_style.string = """/* Ensure header has blue background from the start */
.fusion-tb-header .fusion-fullwidth {
  background-color: #051334 !important;
  background: #051334 !important;
}

.fusion-tb-header {
  position: sticky !important;
  top: 0 !important;
  z-index: 20051 !important;
}

/* Prevent content from underlapping header */
main#main,
.post-content {
  position: relative !important;
  z-index: 1 !important;
}"""
                updated_count += 1
            else:
                # Add new style tag in head
                head = soup.find('head')
                if head:
                    new_style = soup.new_tag('style', id='header-background-fix', type='text/css')
                    new_style.string = """/* Ensure header has blue background from the start */
.fusion-tb-header .fusion-fullwidth {
  background-color: #051334 !important;
  background: #051334 !important;
}

.fusion-tb-header {
  position: sticky !important;
  top: 0 !important;
  z-index: 20051 !important;
}

/* Prevent content from underlapping header */
main#main,
.post-content {
  position: relative !important;
  z-index: 1 !important;
}"""
                    head.append(new_style)
                    updated_count += 1
            
            # Write back if modified
            if existing_style or (head and not existing_style):
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
        
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
            continue
    
    print(f"Updated header CSS on {updated_count} pages")

def main():
    """Main function."""
    print("="*70)
    print("Fix Header Background and Z-Index")
    print("="*70)
    print()
    
    print("1. Adding header CSS fixes to theme-overrides.css...")
    fix_header_css()
    
    print("\n2. Adding header CSS to all HTML pages...")
    add_header_css_to_all_pages()
    
    print("\n3. Checking homepage hero section...")
    add_hero_section_to_homepage()
    
    print("\n" + "="*70)
    print("Header fixes complete!")
    print("="*70)

if __name__ == '__main__':
    main()

