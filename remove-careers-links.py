#!/usr/bin/env python3
"""
Remove all Careers page links and the "Apply Today" button from the website.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def remove_careers_links(file_path):
    """Remove careers links and Apply Today button from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # Find and remove all links to /careers/
        careers_links = soup.find_all('a', href=re.compile(r'/careers/', re.I))
        for link in careers_links:
            # Check if this is the "Apply Today" button section
            parent = link.find_parent()
            if parent and 'Apply Today' in link.get_text():
                # Find the parent column that contains this button
                column = link.find_parent('div', class_=re.compile(r'fusion.*column', re.I))
                if column:
                    # Remove the entire column
                    column.decompose()
                    modified = True
                    print(f"    Removed 'Apply Today' button section")
                else:
                    # Just remove the link
                    link.decompose()
                    modified = True
            else:
                # Remove the link but keep the text if it's just a footer link
                link_text = link.get_text()
                link.replace_with(link_text)
                modified = True
        
        # Also remove any standalone "Careers" text in footers that might be left
        # Look for patterns like "Careers" in footer areas
        footers = soup.find_all(['footer', 'div'], class_=re.compile(r'footer', re.I))
        for footer in footers:
            # Find paragraphs with just "Careers" text
            for p in footer.find_all('p'):
                text = p.get_text(strip=True)
                if text.lower() == 'careers':
                    p.decompose()
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main removal process."""
    print(f"{'='*70}")
    print(f"Remove Careers Links and Apply Today Button")
    print(f"{'='*70}")
    print()
    
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        # Skip wp-content, wp-includes, wp-json, and node_modules
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str and 'node_modules' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    updated_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        
        # Check if file has careers links before processing
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '/careers/' not in content.lower() and 'apply today' not in content.lower():
                skipped_count += 1
                continue
        
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        if remove_careers_links(html_file):
            updated_count += 1
            print(f"  [OK] Removed careers links")
        else:
            skipped_count += 1
            print(f"  - No changes needed")
    
    print(f"\n{'='*70}")
    print(f"Removal Complete!")
    print(f"  [OK] Files updated: {updated_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

