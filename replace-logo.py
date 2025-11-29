#!/usr/bin/env python3
"""
Replace all logo references with the new Digital Growth Studios logo.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# New logo path (relative to site root)
NEW_LOGO_PATH = "/wp-content/uploads/digital-growth-studios-logo.jpg"

def replace_logo_in_file(file_path):
    """Replace logo references in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common logo file patterns to replace
        logo_patterns = [
            (r'/wp-content/uploads/Black-Propeller-Logo[^"\s]*', NEW_LOGO_PATH),
            (r'Black-Propeller-Logo[^"\s]*', 'digital-growth-studios-logo.jpg'),
            (r'black-propeller-logo[^"\s]*', 'digital-growth-studios-logo.jpg'),
        ]
        
        for pattern, replacement in logo_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def replace_logo_in_soup(file_path):
    """Use BeautifulSoup to replace logo in img src and other attributes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Find all img tags
        for img in soup.find_all('img'):
            # Check src attribute
            if 'src' in img.attrs:
                src = img.attrs['src']
                if 'Black-Propeller-Logo' in src or 'black-propeller-logo' in src:
                    # Replace with new logo
                    img.attrs['src'] = NEW_LOGO_PATH
                    modified = True
            
            # Check srcset attribute
            if 'srcset' in img.attrs:
                srcset = img.attrs['srcset']
                if 'Black-Propeller-Logo' in srcset or 'black-propeller-logo' in srcset:
                    # Replace srcset with new logo (single size)
                    img.attrs['srcset'] = f"{NEW_LOGO_PATH} 1x"
                    modified = True
            
            # Check data-src (lazy loading)
            if 'data-src' in img.attrs:
                data_src = img.attrs['data-src']
                if 'Black-Propeller-Logo' in data_src or 'black-propeller-logo' in data_src:
                    img.attrs['data-src'] = NEW_LOGO_PATH
                    modified = True
        
        # Also check in link tags (for favicons, etc.)
        for link in soup.find_all('link'):
            if 'href' in link.attrs:
                href = link.attrs['href']
                if 'Black-Propeller-Logo' in href or 'black-propeller-logo' in href:
                    link.attrs['href'] = NEW_LOGO_PATH
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing with BeautifulSoup {file_path}: {e}")
        return False

def main():
    """Main logo replacement process."""
    print(f"{'='*70}")
    print(f"Replace Logo with Digital Growth Studios Logo")
    print(f"{'='*70}")
    print(f"New logo path: {NEW_LOGO_PATH}")
    print()
    
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        # Skip node_modules
        if 'node_modules' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    replaced_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        # First do regex replacement
        regex_changed = replace_logo_in_file(html_file)
        
        # Then do BeautifulSoup replacement for img tags
        soup_changed = replace_logo_in_soup(html_file)
        
        if regex_changed or soup_changed:
            replaced_count += 1
            print(f"  [OK] Replaced logo")
        else:
            skipped_count += 1
            print(f"  - No logo found")
    
    print(f"\n{'='*70}")
    print(f"Logo Replacement Complete!")
    print(f"  [OK] Files updated: {replaced_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

