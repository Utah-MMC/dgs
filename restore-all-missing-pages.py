#!/usr/bin/env python3
"""
Restore all missing pages from the live site, including core pages if needed.
This will fetch and restore content for ALL pages that need it.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import urllib.request
import urllib.error
import ssl
import time

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Disable SSL verification for local testing (use with caution)
ssl._create_default_https_context = ssl._create_unverified_context

# Only skip the homepage
SKIP_PAGES = {
    'index.html',  # Homepage
}

def is_skip_page(file_path):
    """Check if this page should be skipped."""
    rel_path = str(file_path.relative_to(Path('blackpropeller.com')))
    rel_path_normalized = rel_path.replace('\\', '/')
    # Only skip the root homepage (index.html at root level)
    return rel_path_normalized == 'index.html'

def get_url_from_file_path(file_path):
    """Convert file path to URL on blackpropeller.com."""
    rel_path = str(file_path.relative_to(Path('blackpropeller.com')))
    rel_path = rel_path.replace('\\', '/')
    
    # Remove index.html from path
    if rel_path.endswith('/index.html'):
        rel_path = rel_path[:-11]  # Remove '/index.html'
    elif rel_path.endswith('index.html'):
        rel_path = rel_path[:-10]  # Remove 'index.html'
    
    # Build URL
    if rel_path == '' or rel_path == '.':
        url = 'https://blackpropeller.com/'
    else:
        url = f'https://blackpropeller.com/{rel_path}/'
    
    return url

def fetch_html_from_url(url, retries=3):
    """Fetch HTML content from a URL."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                html_content = response.read().decode('utf-8', errors='replace')
                return html_content
        except urllib.error.HTTPError as e:
            if e.code == 403:
                if attempt < retries - 1:
                    time.sleep(3)
                    continue
            print(f"    [ERROR] HTTP {e.code} for {url}")
            return None
        except (urllib.error.URLError, Exception) as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            print(f"    [ERROR] Failed to fetch {url}: {e}")
            return None
    return None

def extract_content_sections(soup):
    """Extract content sections (accordions, images, etc.) from the page."""
    # Try to find post-content first (most common)
    post_content = soup.find('div', class_='post-content')
    
    # If no post-content, try to find the main content area
    if not post_content:
        post_content = soup.find('main') or soup.find('div', id='content') or soup.find('section', class_='full-width')
    
    if not post_content:
        return None
    
    # Find all fusion-fullwidth boxes
    fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
    
    # Need at least 2 boxes (title + at least one content section)
    if len(fullwidth_boxes) <= 1:
        return None
    
    # Get all boxes except the first one (which is title/description)
    content_sections = fullwidth_boxes[1:]
    
    return content_sections if content_sections else None

def needs_restoration(file_path):
    """Check if a page needs content restoration."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        post_content = soup.find('div', class_='post-content')
        
        if not post_content:
            return True
        
        # Check if there are multiple fusion-fullwidth sections
        fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
        
        # If there's only one box (title/description), it needs restoration
        if len(fullwidth_boxes) <= 1:
            return True
        
        # Check if content sections have actual content (not just title/description)
        content_boxes = fullwidth_boxes[1:]
        has_real_content = False
        
        for box in content_boxes:
            # Check for images, accordions, or substantial text content
            if box.find('img') or box.find('div', class_=re.compile(r'accordian|accordion', re.I)):
                has_real_content = True
                break
            # Check for substantial text (more than just a few words)
            text = box.get_text(strip=True)
            if len(text) > 200:  # More than just title/description
                has_real_content = True
                break
        
        return not has_real_content
    
    except Exception as e:
        print(f"    [ERROR] Error checking {file_path}: {e}")
        return True

def restore_content_from_live_site(file_path):
    """Fetch and restore content from live blackpropeller.com site."""
    try:
        # Skip homepage
        if is_skip_page(file_path):
            return 'skipped_homepage'
        
        # Check if page needs restoration
        if not needs_restoration(file_path):
            return 'skipped_already_has_content'
        
        # Get URL
        url = get_url_from_file_path(file_path)
        print(f"    Fetching from: {url}")
        
        # Fetch HTML
        live_html = fetch_html_from_url(url)
        if not live_html:
            return 'skipped_fetch_failed'
        
        # Parse live HTML
        live_soup = BeautifulSoup(live_html, 'html.parser')
        
        # Extract content sections
        content_sections = extract_content_sections(live_soup)
        if not content_sections:
            # Debug for service pages
            file_str = str(file_path).replace('\\', '/')
            if '/services/' in file_str:
                post_content = live_soup.find('div', class_='post-content')
                if post_content:
                    boxes = post_content.find_all('div', class_='fusion-fullwidth')
                    print(f"    [DEBUG] Found {len(boxes)} fusion-fullwidth boxes in post-content")
                else:
                    print(f"    [DEBUG] No post-content found")
            return 'skipped_no_content'
        
        print(f"    Found {len(content_sections)} content sections to restore")
        
        # Read current page
        with open(file_path, 'r', encoding='utf-8') as f:
            current_html = f.read()
        
        current_soup = BeautifulSoup(current_html, 'html.parser')
        
        # Find post-content - try multiple methods
        post_content = current_soup.find('div', class_='post-content')
        if not post_content:
            # Try to find main content area
            post_content = current_soup.find('main')
        if not post_content:
            post_content = current_soup.find('div', id='content')
        if not post_content:
            post_content = current_soup.find('section', class_='full-width')
        if not post_content:
            # Try finding section with id="content"
            post_content = current_soup.find('section', id='content')
        if not post_content:
            # Last resort: find any section or div that contains fusion-fullwidth
            all_sections = current_soup.find_all(['section', 'div'], class_=re.compile(r'content|main|post', re.I))
            for section in all_sections:
                if section.find('div', class_='fusion-fullwidth'):
                    post_content = section
                    break
        
        if not post_content:
            return 'skipped_no_post_content'
        
        # Find the first fusion-fullwidth (title/description)
        first_fullwidth = post_content.find('div', class_='fusion-fullwidth')
        if not first_fullwidth:
            # If no fusion-fullwidth in post_content, try to find it anywhere in the page
            first_fullwidth = current_soup.find('div', class_='fusion-fullwidth')
            if first_fullwidth:
                # Use the parent of first_fullwidth as post_content
                post_content = first_fullwidth.find_parent(['div', 'section', 'main'])
        
        if not first_fullwidth:
            return 'skipped_no_fullwidth'
        
        # Remove all content after the first fullwidth
        for sibling in list(first_fullwidth.next_siblings):
            if hasattr(sibling, 'extract'):
                sibling.extract()
        
        # Insert the fetched content sections
        for section in content_sections:
            # Clone the section - convert to string and parse to get a fresh copy
            section_str = str(section)
            section_soup = BeautifulSoup(section_str, 'html.parser')
            # Get the root element (should be the fusion-fullwidth div)
            section_element = section_soup.find('div', class_='fusion-fullwidth')
            if section_element:
                first_fullwidth.insert_after(section_element)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(current_soup))
        
        return 'restored'
    
    except Exception as e:
        print(f"    [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return 'error'

def main():
    """Main restoration process."""
    print(f"{'='*70}")
    print(f"Restore All Missing Pages from Live Site")
    print(f"{'='*70}")
    print(f"Pages to skip:")
    print(f"  - Homepage (index.html)")
    print(f"  - Pages that already have full content")
    print()
    
    base_dir = Path('blackpropeller.com')
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} pages to check\n")
    
    stats = {
        'restored': 0,
        'skipped_homepage': 0,
        'skipped_already_has_content': 0,
        'skipped_fetch_failed': 0,
        'skipped_no_content': 0,
        'skipped_no_post_content': 0,
        'skipped_no_fullwidth': 0,
        'error': 0
    }
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        result = restore_content_from_live_site(html_file)
        
        if result == 'restored':
            stats['restored'] += 1
            print(f"    [OK] Restored content from live site")
        elif result == 'skipped_homepage':
            stats['skipped_homepage'] += 1
            print(f"    - Skipped (homepage)")
        elif result == 'skipped_already_has_content':
            stats['skipped_already_has_content'] += 1
            print(f"    - Skipped (already has content)")
        elif result == 'skipped_fetch_failed':
            stats['skipped_fetch_failed'] += 1
            print(f"    - Skipped (failed to fetch)")
        elif result == 'skipped_no_content':
            stats['skipped_no_content'] += 1
            print(f"    - Skipped (no content sections found)")
        elif result == 'skipped_no_post_content':
            stats['skipped_no_post_content'] += 1
            print(f"    - Skipped (no post-content div)")
        elif result == 'skipped_no_fullwidth':
            stats['skipped_no_fullwidth'] += 1
            print(f"    - Skipped (no fusion-fullwidth found)")
        elif result == 'error':
            stats['error'] += 1
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  [OK] Restored: {stats['restored']} pages")
    print(f"  - Skipped (homepage): {stats['skipped_homepage']} pages")
    print(f"  - Skipped (already has content): {stats['skipped_already_has_content']} pages")
    print(f"  - Skipped (fetch failed): {stats['skipped_fetch_failed']} pages")
    print(f"  - Skipped (no content): {stats['skipped_no_content']} pages")
    print(f"  - Skipped (structure issues): {stats['skipped_no_post_content'] + stats['skipped_no_fullwidth']} pages")
    if stats['error'] > 0:
        print(f"  [ERROR] Errors: {stats['error']} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

