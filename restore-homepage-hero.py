#!/usr/bin/env python3
"""
Restore the hero section on the homepage by fetching it from the live site.
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

def extract_hero_section(soup):
    """Extract the hero section (fusion-builder-row-2) from the soup."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return None
    
    # Find fusion-builder-row-2 (hero section)
    hero = post_content.find('div', class_='fusion-fullwidth', 
                             attrs={'style': lambda x: x and 'fusion-builder-row-2' in str(x) if x else False})
    
    if not hero:
        # Try finding by class pattern
        for div in post_content.find_all('div', class_='fusion-fullwidth'):
            style = div.get('style', '')
            if 'fusion-builder-row-2' in style or 'padding-top:180px' in style:
                return div
    
    return hero

def restore_hero_section():
    """Restore the hero section on the homepage."""
    homepage_path = Path('blackpropeller.com/index.html')
    
    if not homepage_path.exists():
        print("Homepage not found!")
        return
    
    print("Fetching homepage from live site...")
    fetched_html = fetch_homepage()
    
    if not fetched_html:
        print("Failed to fetch homepage")
        return
    
    print("Extracting hero section...")
    fetched_soup = BeautifulSoup(fetched_html, 'html.parser')
    fetched_hero = extract_hero_section(fetched_soup)
    
    if not fetched_hero:
        print("Could not find hero section in fetched homepage")
        return
    
    print("Reading local homepage...")
    with open(homepage_path, 'r', encoding='utf-8') as f:
        local_html = f.read()
    
    local_soup = BeautifulSoup(local_html, 'html.parser')
    post_content = local_soup.find('div', class_='post-content')
    
    if not post_content:
        print("Could not find post-content in local homepage")
        return
    
    # Check if hero section exists
    local_hero = None
    for div in post_content.find_all('div', class_='fusion-fullwidth'):
        style = div.get('style', '')
        if 'fusion-builder-row-2' in style or 'padding-top:180px' in style:
            local_hero = div
            break
    
    if local_hero:
        print("Hero section exists, replacing with fetched version...")
        # Replace existing hero
        local_hero.replace_with(fetched_hero)
    else:
        print("Hero section missing, inserting before first section...")
        # Find first section (should be brand logos - fusion-builder-row-3)
        first_section = post_content.find('div', class_='fusion-fullwidth')
        if first_section:
            first_section.insert_before(fetched_hero)
        else:
            # Just append to post-content
            post_content.append(fetched_hero)
    
    print("Saving homepage...")
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(str(local_soup))
    
    print("Hero section restored!")

if __name__ == '__main__':
    restore_hero_section()

