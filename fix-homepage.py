#!/usr/bin/env python3
"""
Fix the broken homepage by fetching the original content from the live site.
"""

import urllib.request
import ssl
from bs4 import BeautifulSoup
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_homepage():
    """Fetch the homepage from the live site."""
    url = 'https://blackpropeller.com/'
    
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
        print(f"Error fetching homepage: {e}")
        return None

def extract_homepage_content(fetched_html):
    """Extract the main content from the fetched homepage."""
    soup = BeautifulSoup(fetched_html, 'html.parser')
    
    # Find the post-content div which contains the main page content
    post_content = soup.find('div', class_='post-content')
    
    if post_content:
        return post_content
    else:
        # Try alternative containers
        main = soup.find('main')
        if main:
            return main.find('div', class_='post-content') or main
        
        content_div = soup.find('div', id='content')
        if content_div:
            return content_div.find('div', class_='post-content') or content_div
        
        return None

def fix_homepage():
    """Fix the homepage by replacing content with the original from live site."""
    homepage_path = Path('blackpropeller.com/index.html')
    
    if not homepage_path.exists():
        print(f"Error: {homepage_path} not found!")
        return
    
    print("Fetching homepage from live site...")
    fetched_html = fetch_homepage()
    
    if not fetched_html:
        print("Failed to fetch homepage from live site")
        return
    
    print("Extracting content from fetched homepage...")
    fetched_content = extract_homepage_content(fetched_html)
    
    if not fetched_content:
        print("Could not find content in fetched homepage")
        return
    
    print("Reading local homepage...")
    with open(homepage_path, 'r', encoding='utf-8') as f:
        local_html = f.read()
    
    local_soup = BeautifulSoup(local_html, 'html.parser')
    
    # Find the post-content div in the local file
    local_post_content = local_soup.find('div', class_='post-content')
    
    if not local_post_content:
        # Try to find main tag
        main = local_soup.find('main')
        if main:
            # Find or create post-content
            local_post_content = main.find('div', class_='post-content')
            if not local_post_content:
                # Create post-content div
                local_post_content = local_soup.new_tag('div', class_='post-content')
                section = main.find('section', class_='full-width') or main.find('section', id='content')
                if section:
                    section.append(local_post_content)
                else:
                    main.append(local_post_content)
    
    if not local_post_content:
        print("Could not find or create post-content in local homepage")
        return
    
    print("Replacing content...")
    # Replace the content
    local_post_content.clear()
    for element in fetched_content.children:
        local_post_content.append(element)
    
    print("Saving fixed homepage...")
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(str(local_soup))
    
    print("Homepage fixed successfully!")

if __name__ == '__main__':
    fix_homepage()

