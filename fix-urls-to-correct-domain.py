#!/usr/bin/env python3
"""
Fix all URLs to use the correct domain: digitalgrowthstudios.com
Replace:
- https://Digital Growth Studios.com/ -> https://digitalgrowthstudios.com/
- https://blackpropeller.com/ -> https://digitalgrowthstudios.com/
- http://Digital Growth Studios.com/ -> http://digitalgrowthstudios.com/
- http://blackpropeller.com/ -> http://digitalgrowthstudios.com/
And all variations
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_urls_in_file(file_path):
    """Fix URLs in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace URLs with spaces in domain (Digital Growth Studios.com)
        # Match http:// or https:// followed by domain with spaces
        content = re.sub(
            r'https?://(?:www\.)?Digital\s+Growth\s+Studios\.com',
            r'https://digitalgrowthstudios.com',
            content,
            flags=re.IGNORECASE
        )
        
        # Replace blackpropeller.com with digitalgrowthstudios.com
        content = re.sub(
            r'https?://(?:www\.)?blackpropeller\.com',
            r'https://digitalgrowthstudios.com',
            content,
            flags=re.IGNORECASE
        )
        
        # Also handle URLs in attributes and other contexts
        # Fix any remaining variations
        content = re.sub(
            r'//(?:www\.)?Digital\s+Growth\s+Studios\.com',
            r'//digitalgrowthstudios.com',
            content,
            flags=re.IGNORECASE
        )
        
        content = re.sub(
            r'//(?:www\.)?blackpropeller\.com',
            r'//digitalgrowthstudios.com',
            content,
            flags=re.IGNORECASE
        )
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def fix_urls_in_soup(file_path):
    """Also use BeautifulSoup to fix URLs in attributes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Fix URLs in href, src, and other URL attributes
        url_attributes = ['href', 'src', 'action', 'data-url', 'data-src', 'data-href', 'cite', 'background']
        
        for tag in soup.find_all(True):  # Find all tags
            for attr_name in url_attributes:
                if attr_name in tag.attrs:
                    attr_value = tag.attrs[attr_name]
                    if isinstance(attr_value, str):
                        original_value = attr_value
                        new_value = original_value
                        
                        # Replace URLs
                        new_value = re.sub(
                            r'https?://(?:www\.)?Digital\s+Growth\s+Studios\.com',
                            r'https://digitalgrowthstudios.com',
                            new_value,
                            flags=re.IGNORECASE
                        )
                        
                        new_value = re.sub(
                            r'https?://(?:www\.)?blackpropeller\.com',
                            r'https://digitalgrowthstudios.com',
                            new_value,
                            flags=re.IGNORECASE
                        )
                        
                        new_value = re.sub(
                            r'//(?:www\.)?Digital\s+Growth\s+Studios\.com',
                            r'//digitalgrowthstudios.com',
                            new_value,
                            flags=re.IGNORECASE
                        )
                        
                        new_value = re.sub(
                            r'//(?:www\.)?blackpropeller\.com',
                            r'//digitalgrowthstudios.com',
                            new_value,
                            flags=re.IGNORECASE
                        )
                        
                        if new_value != original_value:
                            tag.attrs[attr_name] = new_value
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
    """Main URL fixing process."""
    print(f"{'='*70}")
    print(f"Fix URLs to Correct Domain")
    print(f"{'='*70}")
    print(f"Replacing URLs:")
    print(f"  - 'Digital Growth Studios.com' -> 'digitalgrowthstudios.com'")
    print(f"  - 'blackpropeller.com' -> 'digitalgrowthstudios.com'")
    print()
    
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        # Skip wp-content, wp-includes, etc. (but we might need to fix some URLs there too)
        if 'node_modules' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    replaced_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        # First do regex replacement
        regex_changed = fix_urls_in_file(html_file)
        
        # Then do BeautifulSoup replacement for attributes
        soup_changed = fix_urls_in_soup(html_file)
        
        if regex_changed or soup_changed:
            replaced_count += 1
            print(f"  [OK] Fixed URLs")
        else:
            skipped_count += 1
            print(f"  - No URL fixes needed")
    
    print(f"\n{'='*70}")
    print(f"URL Fix Complete!")
    print(f"  [OK] Files updated: {replaced_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")
    
    # Final verification
    print(f"\nVerifying URL fixes...")
    remaining = []
    for html_file in html_files[:50]:  # Check first 50 files
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'Digital\s+Growth\s+Studios\.com|blackpropeller\.com', content, re.IGNORECASE):
                remaining.append(str(html_file.relative_to(base_dir)))
    
    if remaining:
        print(f"  [WARNING] Found remaining old domain references in {len(remaining)} files:")
        for file in remaining[:10]:  # Show first 10
            print(f"    - {file}")
        if len(remaining) > 10:
            print(f"    ... and {len(remaining) - 10} more")
    else:
        print(f"  [OK] All URLs fixed!")

if __name__ == '__main__':
    main()

