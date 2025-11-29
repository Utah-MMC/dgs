#!/usr/bin/env python3
"""
Restore blog posts from original scraped content in rewrite_progress.json.
Reconstructs the full content by combining all original text elements.
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def load_rewrite_progress():
    """Load the rewrite progress JSON file with proper encoding."""
    progress_file = Path('blackpropeller.com/rewrite_progress.json')
    
    if not progress_file.exists():
        print(f"Error: {progress_file} not found!")
        return None
    
    print(f"Loading rewrite progress from {progress_file}...")
    encodings = ['latin-1', 'cp1252', 'utf-8', 'iso-8859-1']
    data = None
    
    for encoding in encodings:
        try:
            with open(progress_file, 'r', encoding=encoding, errors='replace') as f:
                data = json.load(f)
            print(f"Successfully loaded with {encoding} encoding")
            break
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            continue
    
    if data is None:
        print("Error: Could not load JSON file with any encoding!")
        return None
    
    return data

def extract_blog_content(progress_data, blog_file_path):
    """Extract all original content for a specific blog post."""
    blog_slug = blog_file_path.parent.name
    blog_file_key = f"blog\\{blog_slug}\\index.html"
    
    # Also try with forward slashes
    blog_file_key_alt = f"blog/{blog_slug}/index.html"
    
    if 'rewritten' not in progress_data:
        return []
    
    # Collect all content items for this blog post
    content_items = []
    
    for item in progress_data['rewritten']:
        file_path = item.get('file', '')
        
        # Match the blog file
        if file_path == blog_file_key or file_path == blog_file_key_alt:
            tag = item.get('tag', '')
            original = item.get('original', '').strip()
            
            # Only include substantial content (skip navigation, menus, etc.)
            if original and len(original) > 20:
                # Skip navigation items
                if 'Paid Search' in original and 'Paid Social' in original:
                    continue
                if original in ['Paid Search', 'Paid Social', 'Performance Creative', 'Amazon Ads']:
                    continue
                
                content_items.append({
                    'tag': tag,
                    'content': original,
                    'id': item.get('id', '')
                })
    
    # Sort by ID to maintain order
    content_items.sort(key=lambda x: x['id'])
    
    return content_items

def reconstruct_blog_content(content_items):
    """Reconstruct blog post HTML from content items."""
    if not content_items:
        return None
    
    sections = []
    current_paragraph = []
    
    for item in content_items:
        tag = item['tag']
        content = item['content']
        
        # Skip very short items that are likely navigation
        if len(content) < 30 and tag in ['li', 'a']:
            continue
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # Flush current paragraph
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    sections.append(f'<div class="fusion-text"><p>{para_text.strip()}</p></div>')
                current_paragraph = []
            
            # Add heading
            heading_level = tag[1] if len(tag) > 1 else '2'
            sections.append(f'<div class="fusion-title title"><h{heading_level} class="title-heading-left">{content}</h{heading_level}></div>')
        
        elif tag == 'p':
            # Flush current paragraph
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    sections.append(f'<div class="fusion-text"><p>{para_text.strip()}</p></div>')
                current_paragraph = []
            
            # Add this paragraph
            if content.strip():
                sections.append(f'<div class="fusion-text"><p>{content.strip()}</p></div>')
        
        elif tag in ['li', 'ul', 'ol']:
            # For list items, we'll handle them separately
            if content.strip() and len(content) > 20:
                if not current_paragraph:
                    sections.append('<div class="fusion-text"><ul>')
                sections.append(f'<li>{content.strip()}</li>')
        
        else:
            # Add to current paragraph
            if content.strip():
                current_paragraph.append(content.strip())
    
    # Flush remaining paragraph
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        if para_text.strip():
            sections.append(f'<div class="fusion-text"><p>{para_text.strip()}</p></div>')
    
    # Close any open lists
    html_content = '\n'.join(sections)
    
    return html_content

def restore_blog_post(blog_file_path, progress_data):
    """Restore a single blog post from original scraped content."""
    try:
        # Extract original content
        content_items = extract_blog_content(progress_data, blog_file_path)
        
        if not content_items:
            return False
        
        # Reconstruct HTML
        new_content_html = reconstruct_blog_content(content_items)
        
        if not new_content_html:
            return False
        
        # Read current blog post
        with open(blog_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the content area
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            return False
        
        # Find the first fusion-text div (description)
        first_text_div = post_content.find('div', class_='fusion-text')
        if not first_text_div:
            return False
        
        # Get the parent column wrapper
        parent_column = first_text_div.find_parent('div', class_='fusion-column-wrapper')
        if not parent_column:
            return False
        
        # Parse and insert new content
        new_content_soup = BeautifulSoup(new_content_html, 'html.parser')
        
        # Insert after the first fusion-text div
        first_text_div.insert_after(new_content_soup)
        
        # Write back
        with open(blog_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to restore all blog posts from original scraped content."""
    print(f"{'='*70}")
    print(f"Restore Blog Posts from Original Scraped Content")
    print(f"{'='*70}\n")
    
    # Load rewrite progress
    progress_data = load_rewrite_progress()
    if not progress_data:
        return
    
    total_items = len(progress_data.get('rewritten', []))
    print(f"Loaded rewrite progress with {total_items} items\n")
    
    # Find all blog posts
    blog_dir = Path('blackpropeller.com/blog')
    if not blog_dir.exists():
        print(f"Blog directory {blog_dir} not found!")
        return
    
    blog_files = [f for f in blog_dir.glob('*/index.html') if f.parent.name != 'blog']
    
    print(f"Found {len(blog_files)} blog posts to process\n")
    
    restored_count = 0
    skipped_count = 0
    
    for i, blog_file in enumerate(blog_files, 1):
        blog_slug = blog_file.parent.name
        print(f"[{i}/{len(blog_files)}] Processing: blog/{blog_slug}/")
        
        # Check how many content items we have
        content_items = extract_blog_content(progress_data, blog_file)
        print(f"  Found {len(content_items)} original content items")
        
        if restore_blog_post(blog_file, progress_data):
            restored_count += 1
            print(f"  ✓ Restored from original scraped content")
        else:
            skipped_count += 1
            print(f"  - Could not restore (no content or error)")
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  Restored: {restored_count} blog posts")
    print(f"  Skipped: {skipped_count} blog posts")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

