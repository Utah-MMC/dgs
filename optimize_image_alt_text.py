#!/usr/bin/env python3
"""
Optimize image alt text across all HTML pages to be keyword-rich for SEO.
Analyzes page context (title, headings, URL, nearby text) to generate relevant alt text.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Keyword mappings based on URL paths
PATH_KEYWORDS = {
    'seo': ['SEO', 'search engine optimization', 'organic search', 'search rankings'],
    'paid-search': ['PPC', 'paid search', 'Google Ads', 'pay-per-click', 'search advertising'],
    'paid-social': ['paid social', 'social media advertising', 'Facebook Ads', 'Instagram Ads', 'social ads'],
    'creative': ['performance creative', 'ad creative', 'marketing creative', 'advertising design'],
    'amazon': ['Amazon Ads', 'Amazon advertising', 'Amazon PPC', 'ecommerce advertising'],
    'hostgator': ['HostGator', 'web hosting', 'hosting services'],
    'packages': ['marketing packages', 'digital marketing packages', 'service packages'],
    'company': ['Digital Growth Studios', 'about us', 'digital marketing agency'],
    'team': ['team', 'marketing team', 'digital marketing experts'],
    'blog': ['digital marketing', 'marketing tips', 'SEO tips', 'PPC tips'],
    'results': ['case study', 'success story', 'client results', 'marketing results'],
    'contact': ['contact', 'get in touch', 'digital marketing consultation'],
}

# Service-specific keywords
SERVICE_KEYWORDS = {
    'local-seo': ['local SEO', 'local search optimization', 'local business SEO'],
    'national-seo': ['national SEO', 'enterprise SEO', 'large-scale SEO'],
    'enterprise-seo': ['enterprise SEO', 'enterprise search optimization', 'large business SEO'],
    'ecommerce-seo': ['ecommerce SEO', 'online store SEO', 'ecommerce search optimization'],
    'aio': ['AI search optimization', 'AI SEO', 'artificial intelligence SEO'],
    'youtube-video-seo': ['YouTube SEO', 'video SEO', 'video search optimization'],
}

def extract_keywords_from_path(file_path):
    """Extract relevant keywords from the file path."""
    path_str = str(file_path).lower()
    keywords = []
    
    # Check for service keywords
    for key, words in SERVICE_KEYWORDS.items():
        if key in path_str:
            keywords.extend(words)
    
    # Check for path keywords
    for key, words in PATH_KEYWORDS.items():
        if key in path_str:
            keywords.extend(words)
    
    return keywords

def extract_page_context(soup, file_path):
    """Extract context from the page (title, headings, etc.)."""
    context = {
        'title': '',
        'headings': [],
        'keywords': extract_keywords_from_path(file_path),
        'page_type': 'general'
    }
    
    # Get page title
    title_tag = soup.find('title')
    if title_tag:
        context['title'] = title_tag.get_text().strip()
    
    # Extract main keywords from title
    if context['title']:
        title_lower = context['title'].lower()
        if 'seo' in title_lower:
            context['keywords'].append('SEO')
        if 'ppc' in title_lower or 'paid search' in title_lower:
            context['keywords'].append('PPC')
        if 'social' in title_lower:
            context['keywords'].append('social media marketing')
        if 'creative' in title_lower:
            context['keywords'].append('creative services')
    
    # Get main headings
    for tag in ['h1', 'h2', 'h3']:
        headings = soup.find_all(tag)
        for heading in headings[:5]:  # Limit to first 5
            text = heading.get_text().strip()
            if text and len(text) < 100:  # Skip very long headings
                context['headings'].append(text)
    
    # Determine page type
    path_str = str(file_path).lower()
    if 'services' in path_str:
        context['page_type'] = 'service'
    elif 'blog' in path_str:
        context['page_type'] = 'blog'
    elif 'results' in path_str or 'case-studies' in path_str:
        context['page_type'] = 'case_study'
    elif 'company' in path_str or 'team' in path_str:
        context['page_type'] = 'about'
    
    return context

def extract_image_context(img_tag, soup):
    """Extract context around a specific image."""
    context = {
        'nearby_text': '',
        'parent_heading': '',
        'filename': '',
        'existing_alt': img_tag.get('alt', '')
    }
    
    # Get image filename
    src = img_tag.get('src', '')
    if src:
        filename = os.path.basename(src)
        context['filename'] = filename.lower()
    
    # Find nearby headings
    parent = img_tag.parent
    for _ in range(5):  # Go up 5 levels
        if parent:
            heading = parent.find(['h1', 'h2', 'h3', 'h4'])
            if heading:
                context['parent_heading'] = heading.get_text().strip()
                break
            parent = parent.parent
    
    # Find nearby text (siblings or parent text)
    parent = img_tag.parent
    if parent:
        # Get text from parent and siblings
        text_parts = []
        for sibling in list(parent.previous_siblings)[:2] + list(parent.next_siblings)[:2]:
            if hasattr(sibling, 'get_text'):
                text = sibling.get_text().strip()
                if text and len(text) < 200:
                    text_parts.append(text)
        
        if text_parts:
            context['nearby_text'] = ' '.join(text_parts[:2])
    
    return context

def generate_alt_text(img_tag, page_context, image_context):
    """Generate keyword-rich alt text for an image."""
    # Skip if it's a logo (usually already has good alt text)
    src = img_tag.get('src', '').lower()
    if 'logo' in src or 'digital-growth-studios-logo' in src:
        if image_context['existing_alt']:
            return image_context['existing_alt']
        return 'Digital Growth Studios logo - Full-service digital marketing agency'
    
    # Skip decorative images with empty alt (they should stay empty)
    if image_context['existing_alt'] == '' and 'decorative' in image_context.get('class', ''):
        return ''
    
    # Build keyword list
    keywords = list(set(page_context['keywords']))
    
    # Add keywords from filename
    filename = image_context['filename']
    if filename:
        # Extract meaningful words from filename
        filename_words = re.sub(r'[^a-z0-9\s]', ' ', filename)
        filename_words = [w for w in filename_words.split() if len(w) > 3]
        if filename_words:
            # Use descriptive words from filename
            if 'gemini' in filename or 'generated' in filename:
                # AI-generated images - use context instead
                pass
            else:
                keywords.extend(filename_words[:2])
    
    # Add keywords from nearby heading
    if image_context['parent_heading']:
        heading_lower = image_context['parent_heading'].lower()
        if 'seo' in heading_lower:
            keywords.append('SEO')
        if 'ppc' in heading_lower or 'paid' in heading_lower:
            keywords.append('PPC')
        if 'social' in heading_lower:
            keywords.append('social media')
        if 'creative' in heading_lower:
            keywords.append('creative')
    
    # Generate alt text based on context
    alt_parts = []
    
    # Determine image type from context
    if image_context['parent_heading']:
        alt_parts.append(image_context['parent_heading'])
    
    # Add service keywords
    if keywords:
        # Use most relevant keywords
        main_keywords = keywords[:2]
        if main_keywords:
            keyword_str = ' '.join(main_keywords)
            if keyword_str not in alt_parts:
                alt_parts.append(keyword_str)
    
    # Add descriptive terms based on page type
    if page_context['page_type'] == 'service':
        if not any('service' in part.lower() for part in alt_parts):
            alt_parts.append('digital marketing service')
    elif page_context['page_type'] == 'case_study':
        if not any('case study' in part.lower() or 'results' in part.lower() for part in alt_parts):
            alt_parts.append('marketing case study results')
    elif page_context['page_type'] == 'blog':
        if not any('marketing' in part.lower() for part in alt_parts):
            alt_parts.append('digital marketing')
    
    # Add company name for branding
    if 'Digital Growth Studios' not in ' '.join(alt_parts):
        alt_parts.append('by Digital Growth Studios')
    
    # Combine parts
    if alt_parts:
        alt_text = ' - '.join(alt_parts)
        # Clean up
        alt_text = re.sub(r'\s+', ' ', alt_text)
        alt_text = alt_text.strip()
        
        # Ensure reasonable length (125 chars max for SEO)
        if len(alt_text) > 125:
            alt_text = alt_text[:122] + '...'
        
        return alt_text
    
    # Fallback: use existing alt or generate from filename
    if image_context['existing_alt'] and len(image_context['existing_alt']) > 3:
        return image_context['existing_alt']
    
    # Last resort: generic but keyword-rich
    if keywords:
        return f"{' '.join(keywords[:2])} - Digital Growth Studios"
    
    return 'Digital marketing image - Digital Growth Studios'

def optimize_images_in_file(file_path):
    """Optimize alt text for all images in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        page_context = extract_page_context(soup, file_path)
        
        images = soup.find_all('img')
        updated_count = 0
        
        for img in images:
            # Skip if it's a tracking pixel or very small image
            src = img.get('src', '')
            if '1x1' in src or 'pixel' in src.lower() or 'spacer' in src.lower():
                continue
            
            image_context = extract_image_context(img, soup)
            new_alt = generate_alt_text(img, page_context, image_context)
            
            old_alt = img.get('alt', '')
            
            # Only update if alt text is missing, too short, or not keyword-rich
            should_update = False
            
            if not old_alt or len(old_alt) < 5:
                should_update = True
            elif old_alt.lower() in ['image', 'img', 'photo', 'picture', 'slide', 'services']:
                should_update = True
            elif not any(keyword.lower() in old_alt.lower() for keyword in page_context['keywords'] if keyword):
                # Current alt doesn't have relevant keywords
                should_update = True
            
            if should_update and new_alt:
                img['alt'] = new_alt
                updated_count += 1
        
        if updated_count > 0:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return updated_count
        
        return 0
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Main function to optimize all images."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    print("=" * 70)
    print("Image Alt Text Optimization Script")
    print("=" * 70)
    print("Scanning HTML files for images...\n")
    
    html_files = [f for f in base_dir.rglob('*.html') if 'node_modules' not in str(f)]
    total_files = len(html_files)
    total_updated = 0
    files_modified = 0
    
    for i, html_file in enumerate(html_files, 1):
        updated = optimize_images_in_file(html_file)
        if updated > 0:
            files_modified += 1
            total_updated += updated
            rel_path = html_file.relative_to(base_dir)
            print(f"[{i}/{total_files}] {rel_path}: Updated {updated} image(s)")
    
    print(f"\n{'=' * 70}")
    print(f"Optimization Complete!")
    print(f"  Files processed: {total_files}")
    print(f"  Files modified: {files_modified}")
    print(f"  Total images updated: {total_updated}")
    print(f"{'=' * 70}")

if __name__ == '__main__':
    main()

