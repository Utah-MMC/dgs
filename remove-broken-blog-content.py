#!/usr/bin/env python3
"""
Remove the broken concatenated text content from the blog page.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def remove_broken_content():
    """Remove broken content from blog page."""
    blog_file = Path('blackpropeller.com/blog/index.html')
    
    if not blog_file.exists():
        print("Blog page not found")
        return
    
    with open(blog_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find post-content
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        print("Could not find post-content")
        return
    
    # Find all fusion-fullwidth boxes
    fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
    
    # Find and remove boxes with broken concatenated text
    removed_count = 0
    for box in fullwidth_boxes:
        # Check if this box contains the broken text pattern
        text = box.get_text()
        if 'What We DoPaid SearchPaid' in text or 'SocialPerformance CreativeAmazon' in text:
            print(f"Found broken content section, removing...")
            box.extract()
            removed_count += 1
    
    if removed_count > 0:
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Removed {removed_count} broken content section(s)")
    else:
        print("No broken content found")

if __name__ == '__main__':
    remove_broken_content()

