#!/usr/bin/env python3
"""
Clean up blog post structure - remove navigation items and fix HTML structure.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def is_navigation_text(text):
    """Check if text is navigation/menu content."""
    nav_keywords = [
        'Paid Search', 'Paid Social', 'Performance Creative', 'Amazon Ads',
        'Who We Are', 'About Us', 'Meet The Team', 'Careers',
        'International & Multilingual SEO', 'Franchise & Multi-Location SEO',
        'COPYRIGHT', 'Digital Growth Studios',
        'What We Do', 'SEO', 'AIO', 'Local SEO', 'National SEO',
        'Enterprise SEO', 'Ecommerce SEO', 'YouTube & Video SEO', 'HubSpot'
    ]
    
    text_upper = text.upper()
    for keyword in nav_keywords:
        if keyword.upper() in text_upper:
            return True
    
    return False

def cleanup_blog_post(blog_file_path):
    """Clean up a single blog post."""
    try:
        with open(blog_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the post content area
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            return False
        
        modified = False
        
        # Find all fusion-text and fusion-title divs
        content_divs = post_content.find_all(['div'], class_=['fusion-text', 'fusion-title'])
        
        for div in content_divs:
            text = div.get_text(strip=True)
            
            # Remove navigation items
            if is_navigation_text(text):
                div.decompose()
                modified = True
                continue
            
            # Fix malformed lists - if we have nested ul tags, fix them
            if div.find('ul'):
                ul_tags = div.find_all('ul')
                if len(ul_tags) > 1:
                    # Keep only the first ul, merge content
                    first_ul = ul_tags[0]
                    for ul in ul_tags[1:]:
                        for li in ul.find_all('li'):
                            first_ul.append(li)
                        ul.decompose()
                    modified = True
        
        # Remove empty divs
        for div in post_content.find_all('div', class_=['fusion-text', 'fusion-title']):
            if not div.get_text(strip=True):
                div.decompose()
                modified = True
        
        # Fix nested fusion-text divs
        for div in post_content.find_all('div', class_='fusion-text'):
            nested_text = div.find('div', class_='fusion-text')
            if nested_text:
                # Move content up
                for child in nested_text.children:
                    div.append(child)
                nested_text.decompose()
                modified = True
        
        if modified:
            with open(blog_file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Main function to clean up all blog posts."""
    print(f"{'='*70}")
    print(f"Clean Up Blog Post Structure")
    print(f"{'='*70}\n")
    
    blog_dir = Path('blackpropeller.com/blog')
    if not blog_dir.exists():
        print(f"Blog directory {blog_dir} not found!")
        return
    
    blog_files = [f for f in blog_dir.glob('*/index.html') if f.parent.name != 'blog']
    
    print(f"Found {len(blog_files)} blog posts to clean up\n")
    
    cleaned_count = 0
    
    for i, blog_file in enumerate(blog_files, 1):
        blog_slug = blog_file.parent.name
        print(f"[{i}/{len(blog_files)}] Processing: blog/{blog_slug}/")
        
        if cleanup_blog_post(blog_file):
            cleaned_count += 1
            print(f"  ✓ Cleaned up")
        else:
            print(f"  - No changes needed")
    
    print(f"\n{'='*70}")
    print(f"Cleanup Complete!")
    print(f"  Cleaned: {cleaned_count} blog posts")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

