#!/usr/bin/env python3
"""
Replace "Black Propeller" and "#TeamBP" with "Digital Growth Studios" and "#TeamDGS"
throughout all HTML files.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def replace_brand_names(file_path):
    """Replace brand names in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace "Black Propeller" with "Digital Growth Studios" (case-insensitive)
        content = re.sub(r'Black Propeller', 'Digital Growth Studios', content, flags=re.IGNORECASE)
        
        # Replace "#TeamBP" with "#TeamDGS" (case-insensitive)
        content = re.sub(r'#TeamBP', '#TeamDGS', content, flags=re.IGNORECASE)
        
        # Also handle variations like "TeamBP" without the #
        content = re.sub(r'TeamBP', 'TeamDGS', content, flags=re.IGNORECASE)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def main():
    """Main replacement process."""
    print(f"{'='*70}")
    print(f"Replace Brand Names")
    print(f"{'='*70}")
    print(f"Replacing:")
    print(f"  - 'Black Propeller' -> 'Digital Growth Studios'")
    print(f"  - '#TeamBP' -> '#TeamDGS'")
    print(f"  - 'TeamBP' -> 'TeamDGS'")
    print()
    
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        # Skip wp-content, wp-includes, etc.
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    replaced_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        if replace_brand_names(html_file):
            replaced_count += 1
            print(f"  [OK] Replaced brand names")
        else:
            skipped_count += 1
            print(f"  - No replacements needed")
    
    print(f"\n{'='*70}")
    print(f"Replacement Complete!")
    print(f"  [OK] Files updated: {replaced_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

