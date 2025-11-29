#!/usr/bin/env python3
"""
SEO Optimization Script - Ensure all pages have proper canonical URLs and SEO meta tags.
Sets canonical URLs to https://digitalgrowthstudios.com/[path]
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

BASE_URL = "https://digitalgrowthstudios.com"

def get_canonical_path(file_path):
    """Convert file path to canonical URL path."""
    # Get relative path from blackpropeller.com
    rel_path = file_path.relative_to(Path('blackpropeller.com'))
    
    # Remove index.html
    if rel_path.name == 'index.html':
        rel_path = rel_path.parent
    
    # Convert to URL path
    path_str = str(rel_path).replace('\\', '/')
    
    # Handle root
    if path_str == '.' or path_str == '':
        return '/'
    
    # Ensure leading slash
    if not path_str.startswith('/'):
        path_str = '/' + path_str
    
    # Ensure trailing slash for directories (but not root)
    if path_str != '/' and not path_str.endswith('/'):
        path_str = path_str + '/'
    
    return path_str

def optimize_seo_tags(soup, file_path, canonical_path):
    """Optimize SEO tags in the HTML."""
    head = soup.find('head')
    if not head:
        return False
    
    updated = False
    canonical_url = BASE_URL + canonical_path
    
    # Find or create canonical link
    canonical_link = head.find('link', {'rel': 'canonical'})
    
    if canonical_link:
        current_href = canonical_link.get('href', '')
        # Update if different (handle both relative and absolute URLs)
        # Normalize current href
        if current_href.startswith('/'):
            current_href = BASE_URL + current_href
        elif not current_href.startswith('http'):
            current_href = BASE_URL + '/' + current_href.lstrip('/')
        
        if current_href != canonical_url:
            canonical_link['href'] = canonical_url
            updated = True
    else:
        # Create canonical link - insert after meta description or title
        title_tag = head.find('title')
        if title_tag:
            canonical_link = soup.new_tag('link', rel='canonical', href=canonical_url)
            title_tag.insert_after(canonical_link)
            updated = True
        else:
            # Insert at beginning of head
            canonical_link = soup.new_tag('link', rel='canonical', href=canonical_url)
            head.insert(0, canonical_link)
            updated = True
    
    # Update og:url to match canonical
    og_url = head.find('meta', {'property': 'og:url'})
    if og_url:
        if og_url.get('content') != canonical_url:
            og_url['content'] = canonical_url
            updated = True
    else:
        # Create og:url if og tags exist
        og_type = head.find('meta', {'property': 'og:type'})
        if og_type:
            og_url = soup.new_tag('meta', property='og:url', content=canonical_url)
            og_type.insert_after(og_url)
            updated = True
    
    # Ensure robots meta tag is present and correct
    robots = head.find('meta', {'name': 'robots'})
    if not robots:
        # Create robots meta tag (default: follow, index)
        robots = soup.new_tag('meta', name='robots', content='follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large')
        # Insert after canonical or title
        if canonical_link:
            canonical_link.insert_after(robots)
        else:
            title_tag = head.find('title')
            if title_tag:
                title_tag.insert_after(robots)
            else:
                head.insert(0, robots)
        updated = True
    else:
        # Ensure it has proper content
        content = robots.get('content', '')
        if 'nofollow' in content and 'noindex' not in content:
            # Change nofollow to follow for SEO
            new_content = content.replace('nofollow', 'follow')
            robots['content'] = new_content
            updated = True
    
    # Ensure lang attribute on html tag
    html_tag = soup.find('html')
    if html_tag:
        if not html_tag.get('lang'):
            html_tag['lang'] = 'en-US'
            updated = True
    
    # Ensure charset meta tag (skip if already exists)
    charset = head.find('meta', {'charset': True}) or head.find('meta', {'http-equiv': 'Content-Type'})
    # Don't create if it doesn't exist - it's usually already there
    
    # Ensure viewport meta tag
    viewport = head.find('meta', {'name': 'viewport'})
    if not viewport:
        try:
            viewport = soup.new_tag('meta')
            viewport['name'] = 'viewport'
            viewport['content'] = 'width=device-width, initial-scale=1'
            # Insert after charset or at beginning
            if charset:
                charset.insert_after(viewport)
            else:
                head.insert(0, viewport)
            updated = True
        except Exception:
            pass  # Skip if there's an issue
    
    return updated

def optimize_page(file_path):
    """Optimize SEO for a single page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        canonical_path = get_canonical_path(file_path)
        
        updated = optimize_seo_tags(soup, file_path, canonical_path)
        
        if updated:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to optimize all pages."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    print("=" * 70)
    print("SEO Optimization Script - Canonical URLs & Meta Tags")
    print("=" * 70)
    print(f"Setting canonical URLs to: {BASE_URL}\n")
    
    html_files = [f for f in base_dir.rglob('*.html') if 'node_modules' not in str(f)]
    total_files = len(html_files)
    files_updated = 0
    
    for i, html_file in enumerate(html_files, 1):
        if optimize_page(html_file):
            files_updated += 1
            rel_path = html_file.relative_to(base_dir)
            canonical_path = get_canonical_path(html_file)
            print(f"[{i}/{total_files}] {rel_path}")
            print(f"  → Canonical: {BASE_URL}{canonical_path}")
    
    print(f"\n{'=' * 70}")
    print(f"SEO Optimization Complete!")
    print(f"  Files processed: {total_files}")
    print(f"  Files updated: {files_updated}")
    print(f"{'=' * 70}")

if __name__ == '__main__':
    main()

