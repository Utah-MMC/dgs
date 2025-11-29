#!/usr/bin/env python3
"""
Fix the broken blog page by fetching the original content from the live site.
"""

import urllib.request
import ssl
from bs4 import BeautifulSoup
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_blog_page():
    """Fetch the blog page from the live site."""
    url = 'https://blackpropeller.com/blog/'
    
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
        print(f"Error fetching blog page: {e}")
        return None

def extract_blog_content(live_html):
    """Extract the main content from the live blog page."""
    soup = BeautifulSoup(live_html, 'html.parser')
    
    # Find post-content
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        post_content = soup.find('main') or soup.find('div', id='content') or soup.find('section', class_='full-width')
    
    if not post_content:
        return None
    
    # Find all fusion-fullwidth boxes
    fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
    
    # Return all boxes (we'll replace everything after the hero section)
    return fullwidth_boxes

def fix_blog_page():
    """Fix the blog page by restoring content from live site."""
    blog_file = Path('blackpropeller.com/blog/index.html')
    
    if not blog_file.exists():
        print("Blog page not found")
        return
    
    print("Fetching blog page from live site...")
    live_html = fetch_blog_page()
    if not live_html:
        print("Failed to fetch blog page")
        return
    
    print("Extracting content...")
    content_sections = extract_blog_content(live_html)
    if not content_sections:
        print("No content sections found")
        return
    
    print(f"Found {len(content_sections)} content sections")
    
    # Read current blog page
    with open(blog_file, 'r', encoding='utf-8') as f:
        current_html = f.read()
    
    current_soup = BeautifulSoup(current_html, 'html.parser')
    
    # Find post-content
    post_content = current_soup.find('div', class_='post-content')
    if not post_content:
        post_content = current_soup.find('main') or current_soup.find('div', id='content') or current_soup.find('section', class_='full-width')
    
    if not post_content:
        print("Could not find post-content in current page")
        return
    
    # Find the hero section (fusion-builder-row-2 with title "Search")
    hero_section = None
    for box in post_content.find_all('div', class_='fusion-fullwidth'):
        if 'fusion-builder-row-2' in box.get('class', []):
            # Check if it contains the title "Search"
            if box.find('h1') and 'Search' in box.find('h1').get_text():
                hero_section = box
                break
    
    if not hero_section:
        # Try to find first fullwidth box
        hero_section = post_content.find('div', class_='fusion-fullwidth')
    
    if not hero_section:
        print("Could not find hero section")
        return
    
    # Remove all content after the hero section
    for sibling in list(hero_section.next_siblings):
        if hasattr(sibling, 'extract'):
            sibling.extract()
    
    # Insert the fetched content sections (skip the first one if it's the hero)
    # We want to keep our hero section, so we'll insert all sections from the live site
    # but we'll skip the first one if it's also a hero section
    start_idx = 0
    if content_sections:
        first_live_section = content_sections[0]
        # Check if first section is a hero section
        if first_live_section.find('h1') and 'Search' in first_live_section.find('h1').get_text():
            start_idx = 1  # Skip the hero section from live site
    
    # Insert all content sections after the hero
    for i, section in enumerate(content_sections[start_idx:], start=start_idx):
        section_str = str(section)
        section_soup = BeautifulSoup(section_str, 'html.parser')
        section_element = section_soup.find('div', class_='fusion-fullwidth')
        if section_element:
            hero_section.insert_after(section_element)
    
    # Write back
    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(str(current_soup))
    
    print("Blog page fixed!")

if __name__ == '__main__':
    fix_blog_page()

