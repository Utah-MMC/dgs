#!/usr/bin/env python3
"""
Fix broken headers on all pages by fetching the correct header structure from the live site.
"""

import urllib.request
import ssl
from bs4 import BeautifulSoup
from pathlib import Path
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_header_from_live_site(url):
    """Fetch the header structure from the live site."""
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    )
    
    try:
        response = urllib.request.urlopen(req, timeout=30)
        html = response.read().decode('utf-8', errors='replace')
        return html
    except Exception as e:
        print(f"  Error fetching: {e}")
        return None

def extract_header(soup):
    """Extract the header section from the soup."""
    # Find the fusion-tb-header div
    header = soup.find('div', class_='fusion-tb-header')
    if header:
        return header
    return None

def get_url_from_file_path(file_path):
    """Convert file path to URL on blackpropeller.com."""
    rel_path = str(file_path.relative_to(Path('blackpropeller.com')))
    rel_path = rel_path.replace('\\', '/')
    
    # Remove index.html from the end
    if rel_path.endswith('/index.html'):
        rel_path = rel_path[:-11]  # Remove '/index.html'
    elif rel_path == 'index.html':
        rel_path = ''
    
    if rel_path and not rel_path.endswith('/'):
        rel_path += '/'
    
    return f'https://blackpropeller.com/{rel_path}'

def fix_header(file_path):
    """Fix the header for a single page."""
    try:
        # Get URL for this page
        url = get_url_from_file_path(file_path)
        
        print(f"  Fetching header from: {url}")
        fetched_html = fetch_header_from_live_site(url)
        
        if not fetched_html:
            return False
        
        fetched_soup = BeautifulSoup(fetched_html, 'html.parser')
        fetched_header = extract_header(fetched_soup)
        
        if not fetched_header:
            print(f"  Could not find header in fetched HTML")
            return False
        
        # Read local file
        with open(file_path, 'r', encoding='utf-8') as f:
            local_html = f.read()
        
        local_soup = BeautifulSoup(local_html, 'html.parser')
        local_header = local_soup.find('div', class_='fusion-tb-header')
        
        if not local_header:
            print(f"  Could not find header in local file")
            return False
        
        # Replace the local header with the fetched header
        local_header.replace_with(fetched_header)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(local_soup))
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fix headers on all pages."""
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        # Skip wp-content, wp-includes, wp-json, and node_modules
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str and 'node_modules' not in file_str:
            html_files.append(html_file)
    
    print(f"{'='*70}")
    print(f"Fix Headers on All Pages")
    print(f"{'='*70}")
    print(f"Found {len(html_files)} pages to process\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        if fix_header(html_file):
            fixed_count += 1
            print(f"  [OK] Header fixed")
        else:
            skipped_count += 1
            print(f"  - Skipped")
    
    print(f"\n{'='*70}")
    print(f"Header Fix Complete!")
    print(f"  [OK] Headers fixed: {fixed_count}")
    print(f"  - Skipped: {skipped_count}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

