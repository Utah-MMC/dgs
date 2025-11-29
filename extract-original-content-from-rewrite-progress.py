#!/usr/bin/env python3
"""
Extract original scraped content from rewrite_progress.json and restore it to blog posts.
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def load_rewrite_progress():
    """Load the rewrite progress JSON file."""
    progress_file = Path('blackpropeller.com/rewrite_progress.json')
    
    if not progress_file.exists():
        print(f"Error: {progress_file} not found!")
        return None
    
    print(f"Loading rewrite progress from {progress_file}...")
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    data = None
    
    for encoding in encodings:
        try:
            with open(progress_file, 'r', encoding=encoding, errors='replace') as f:
                data = json.load(f)
            print(f"Successfully loaded with {encoding} encoding")
            break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    
    if data is None:
        print("Error: Could not load JSON file with any encoding!")
        return None
    
    return data

def extract_blog_content_from_progress(progress_data, blog_slug):
    """Extract original content for a specific blog post from rewrite progress."""
    if 'rewritten' not in progress_data:
        return None
    
    # Build a map of original content by file path
    content_map = {}
    
    for item in progress_data['rewritten']:
        file_path = item.get('file', '')
        
        # Check if this is for the blog post we're looking for
        if blog_slug in file_path.lower() or f'blog/{blog_slug}' in file_path.lower():
            tag = item.get('tag', '')
            original = item.get('original', '')
            
            if original and len(original) > 50:  # Only substantial content
                if file_path not in content_map:
                    content_map[file_path] = []
                content_map[file_path].append({
                    'tag': tag,
                    'content': original
                })
    
    return content_map

def restore_blog_from_original_content(blog_file_path, progress_data):
    """Restore a blog post using original content from rewrite progress."""
    blog_slug = blog_file_path.parent.name
    
    # Extract original content
    content_map = extract_blog_content_from_progress(progress_data, blog_slug)
    
    if not content_map:
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
    
    # Collect all original content pieces
    all_content = []
    for file_path, items in content_map.items():
        for item in items:
            content = item['content'].strip()
            if content and len(content) > 50:
                all_content.append(content)
    
    if not all_content:
        return False
    
    # Combine content and structure it
    # Try to identify headings and paragraphs
    structured_content = []
    
    for content in all_content:
        # Check if it looks like a heading
        if len(content) < 100 and not content.endswith('.'):
            # Might be a heading
            structured_content.append(f'<div class="fusion-title title"><h2 class="title-heading-left">{content}</h2></div>')
        else:
            # Likely a paragraph
            # Split into sentences if it's very long
            if len(content) > 500:
                sentences = content.split('. ')
                for i, sentence in enumerate(sentences):
                    if sentence.strip():
                        if not sentence.endswith('.'):
                            sentence += '.'
                        structured_content.append(f'<div class="fusion-text"><p>{sentence.strip()}</p></div>')
            else:
                structured_content.append(f'<div class="fusion-text"><p>{content}</p></div>')
    
    if not structured_content:
        return False
    
    # Create new content HTML
    new_content_html = '\n'.join(structured_content)
    new_content_soup = BeautifulSoup(new_content_html, 'html.parser')
    
    # Insert after the first fusion-text div
    first_text_div.insert_after(new_content_soup)
    
    # Write back
    with open(blog_file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return True

def main():
    """Main function to restore blog posts from original scraped content."""
    print(f"{'='*70}")
    print(f"Restore Blog Posts from Original Scraped Content")
    print(f"{'='*70}\n")
    
    # Load rewrite progress
    progress_data = load_rewrite_progress()
    if not progress_data:
        return
    
    print(f"Loaded rewrite progress with {len(progress_data.get('rewritten', []))} items\n")
    
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
        
        if restore_blog_from_original_content(blog_file, progress_data):
            restored_count += 1
            print(f"  ✓ Restored from original content")
        else:
            skipped_count += 1
            print(f"  - No original content found in rewrite progress")
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  Restored: {restored_count} blog posts")
    print(f"  Skipped: {skipped_count} blog posts")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

