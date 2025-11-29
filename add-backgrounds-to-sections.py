#!/usr/bin/env python3
"""
Add backgrounds to sections that are missing them, especially testimonial sections
and content sections that should have visible backgrounds.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def add_background_to_section(file_path):
    """Add background colors to sections that need them."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find all fusion-fullwidth sections
        fullwidth_sections = soup.find_all('div', class_='fusion-fullwidth')
        
        for section in fullwidth_sections:
            style = section.get('style', '')
            
            # Check if this section contains testimonials or similar content
            has_testimonial = (
                section.find('div', class_=re.compile(r'rev_slider|testimonial', re.I)) or
                section.find('rs-module') or
                'testimonial' in str(section).lower() or
                'clutch' in str(section).lower()
            )
            
            # Check if section has content but no background color
            has_content = (
                section.find('h1') or
                section.find('h2') or
                section.find('h3') or
                section.find('p') or
                section.find('img') or
                section.find('div', class_='fusion-text') or
                section.find('div', class_='fusion-title')
            )
            
            # Check if background-color is missing or transparent
            has_background = (
                '--awb-background-color' in style or
                'background-color' in style or
                'background:' in style
            )
            
            # If it's a testimonial section or has content but no background, add one
            if (has_testimonial or has_content) and not has_background:
                # Determine appropriate background color
                # Testimonials should have dark blue background
                if has_testimonial:
                    bg_color = '#051334'
                else:
                    # Other content sections should have white or light gray
                    bg_color = '#ffffff'
                
                # Add background color to style
                if style:
                    # Check if style already has --awb-background-color
                    if '--awb-background-color' not in style:
                        section['style'] = style + f';--awb-background-color:{bg_color};'
                        modified = True
                else:
                    section['style'] = f'--awb-background-color:{bg_color};'
                    modified = True
            
            # Also check for Revolution Slider sections that need background
            rev_slider = section.find('div', class_='rev_slider_wrapper')
            if rev_slider:
                rev_style = rev_slider.get('style', '')
                if 'background' not in rev_style or 'transparent' in rev_style:
                    if rev_style:
                        rev_slider['style'] = rev_style.replace('background:transparent', 'background:#051334')
                    else:
                        rev_slider['style'] = 'background:#051334;'
                    modified = True
            
            # Check rs-module-wrap for background
            rs_wrapper = section.find('rs-module-wrap')
            if rs_wrapper:
                rs_style = rs_wrapper.get('style', '')
                if 'background' not in rs_style or 'transparent' in rs_style:
                    if rs_style:
                        rs_wrapper['style'] = rs_style.replace('background:transparent', 'background:#051334')
                    else:
                        rs_wrapper['style'] = 'background:#051334;'
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def add_css_for_section_backgrounds():
    """Add CSS to ensure sections have backgrounds."""
    css_file = Path('blackpropeller.com/assets/theme-overrides.css')
    
    # Read existing CSS
    existing_css = ""
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            existing_css = f.read()
    
    # Check if section background CSS already exists
    if 'section-background-fix' in existing_css or 'rev_slider_wrapper' in existing_css:
        # Update existing
        pass
    else:
        # Add section background CSS
        section_bg_css = """
/* Ensure testimonial and content sections have backgrounds */
.rev_slider_wrapper,
.rs-module-wrap {
  background-color: #051334 !important;
  background: #051334 !important;
}

/* Ensure fusion-fullwidth sections with content have backgrounds */
.fusion-fullwidth:not(.fusion-tb-header .fusion-fullwidth) {
  background-color: #ffffff !important;
}

/* Testimonial sections should have dark blue background */
.fusion-fullwidth:has(.rev_slider_wrapper),
.fusion-fullwidth:has(rs-module-wrap),
.fusion-fullwidth:has(.testimonial) {
  background-color: #051334 !important;
}

/* Ensure sections with content but no explicit background get one */
.fusion-fullwidth:not([style*="--awb-background-color"]):not([style*="background-color"]) {
  background-color: #ffffff !important;
}
"""
        
        # Append to existing CSS
        new_css = existing_css.rstrip() + "\n" + section_bg_css
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(new_css)
        
        print("Added section background CSS to theme-overrides.css")

def main():
    """Main function."""
    print(f"{'='*70}")
    print(f"Add Backgrounds to Sections")
    print(f"{'='*70}")
    print()
    
    # First add CSS rules
    print("1. Adding CSS rules for section backgrounds...")
    add_css_for_section_backgrounds()
    
    # Then process HTML files
    print("\n2. Processing HTML files...")
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        if 'node_modules' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    replaced_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        if add_background_to_section(html_file):
            replaced_count += 1
            print(f"  [OK] Added backgrounds to sections")
        else:
            skipped_count += 1
            print(f"  - No changes needed")
    
    print(f"\n{'='*70}")
    print(f"Background Addition Complete!")
    print(f"  [OK] Files updated: {replaced_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

