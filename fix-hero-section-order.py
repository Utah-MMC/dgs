#!/usr/bin/env python3
"""
Fix the order of the hero section on the homepage - it should be first, before brand logos.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def fix_hero_order():
    """Fix the order of sections on homepage."""
    homepage = Path('blackpropeller.com/index.html')
    
    if not homepage.exists():
        print("Homepage not found")
        return
    
    with open(homepage, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    post_content = soup.find('div', class_='post-content')
    
    if not post_content:
        print("Could not find post-content")
        return
    
    # Find hero section (fusion-builder-row-2)
    hero_section = None
    brand_logos_section = None
    
    for div in post_content.find_all('div', class_='fusion-fullwidth'):
        style = div.get('style', '')
        if 'fusion-builder-row-2' in style or ('padding-top:180px' in style and hero_section is None):
            hero_section = div
        elif 'fusion-builder-row-3' in style:
            brand_logos_section = div
    
    if not hero_section:
        print("Hero section not found")
        return
    
    if not brand_logos_section:
        print("Brand logos section not found")
        return
    
    # Check if hero is already before brand logos
    hero_index = None
    brand_index = None
    
    for i, child in enumerate(post_content.children):
        if child == hero_section:
            hero_index = i
        elif child == brand_logos_section:
            brand_index = i
    
    if hero_index is not None and brand_index is not None and hero_index < brand_index:
        print("Hero section is already in correct position")
        return
    
    # Move hero section before brand logos
    print("Moving hero section before brand logos section...")
    hero_section.extract()
    brand_logos_section.insert_before(hero_section)
    
    with open(homepage, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("Hero section order fixed!")

if __name__ == '__main__':
    fix_hero_order()

