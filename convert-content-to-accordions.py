#!/usr/bin/env python3
"""
Convert text content into accordion format matching the SEO page structure.
This will add accordions to service pages that currently only have plain text.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings
import hashlib

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# Core pages to skip
CORE_PAGES = {
    'services/seo/index.html',
    'services/paid-search/index.html',
    'services/creative/index.html',
    'services/hubspot/index.html',
}

def is_core_page(file_path):
    """Check if this is one of the 4 core pages."""
    rel_path = str(file_path.relative_to(Path('blackpropeller.com')))
    return rel_path.replace('\\', '/') in CORE_PAGES

def generate_unique_id(text):
    """Generate a unique ID from text."""
    return hashlib.md5(text.encode()).hexdigest()[:12]

def convert_text_to_accordion(soup, content_text):
    """Convert text content into accordion format."""
    # Parse the text to identify sections
    lines = content_text.split('\n')
    
    # Find h2 headings and group content under them
    sections = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a heading (h2 tag or text that looks like a heading)
        if line.startswith('<h2>') or (len(line) < 100 and not line.endswith('.') and not line.startswith('<p>')):
            # Save previous section
            if current_section:
                sections.append(current_section)
            
            # Start new section
            heading_text = line.replace('<h2>', '').replace('</h2>', '').strip()
            if not heading_text:
                continue
            current_section = {
                'heading': heading_text,
                'content': []
            }
        elif current_section:
            # Add content to current section
            current_section['content'].append(line)
    
    # Add last section
    if current_section:
        sections.append(current_section)
    
    if not sections:
        return None
    
    # Create accordion HTML structure
    accordion_id = f"accordion-{generate_unique_id(str(soup))}"
    
    accordion_html = f'''<div class="accordian fusion-accordian service-container" style="--awb-border-size:1px;--awb-icon-size:40px;--awb-content-font-size:var(--awb-custom_typography_1-font-size);--awb-icon-alignment:right;--awb-hover-color:var(--awb-color2);--awb-border-color:var(--awb-color2);--awb-background-color:var(--awb-color7);--awb-divider-color:var(--awb-color2);--awb-divider-hover-color:var(--awb-color2);--awb-icon-color:var(--awb-color6);--awb-title-color:var(--awb-color4);--awb-content-color:var(--awb-color4);--awb-icon-box-color:var(--awb-color4);--awb-toggle-hover-accent-color:var(--awb-color4);--awb-title-font-family:var(--awb-typography2-font-family);--awb-title-font-weight:var(--awb-typography2-font-weight);--awb-title-font-style:var(--awb-typography2-font-style);--awb-title-font-size:var(--awb-typography2-font-size);--awb-title-letter-spacing:var(--awb-typography2-letter-spacing);--awb-title-line-height:var(--awb-typography2-line-height);--awb-title-text-transform:var(--awb-typography2-text-transform);--awb-content-font-family:var(--awb-custom_typography_1-font-family);--awb-content-font-weight:var(--awb-custom_typography_1-font-weight);--awb-content-font-style:var(--awb-custom_typography_1-font-style);">
<div class="panel-group fusion-toggle-icon-right fusion-toggle-icon-unboxed" id="{accordion_id}">'''
    
    for i, section in enumerate(sections):
        panel_id = generate_unique_id(section['heading'])
        toggle_id = f"toggle_{panel_id}"
        collapse_id = panel_id
        
        # Combine content
        content_html = '\n'.join(section['content'])
        # Wrap paragraphs if needed
        if '<p>' not in content_html:
            paragraphs = [p.strip() for p in content_html.split('\n') if p.strip()]
            content_html = '\n'.join([f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs])
        
        accordion_html += f'''
<div class="fusion-panel panel-default panel-{panel_id} fusion-toggle-has-divider" style="--awb-title-color:var(--awb-color4);">
<div class="panel-heading">
<h2 class="panel-title toggle" id="{toggle_id}">
<a aria-controls="{collapse_id}" aria-expanded="false" data-parent="#{accordion_id}" data-target="#{collapse_id}" data-toggle="collapse" href="#{collapse_id}" role="button">
<span aria-hidden="true" class="fusion-toggle-icon-wrapper">
<i aria-hidden="true" class="fa-fusion-box active-icon awb-icon-minus"></i>
<i aria-hidden="true" class="fa-fusion-box inactive-icon awb-icon-plus"></i>
</span>
<span class="fusion-toggle-heading">{section['heading']}</span>
</a>
</h2>
</div>
<div aria-labelledby="{toggle_id}" class="panel-collapse collapse" id="{collapse_id}">
<div class="panel-body toggle-content fusion-clearfix">
<div class="fusion-text">
{content_html}
</div>
</div>
</div>
</div>'''
    
    accordion_html += '''
</div>
</div>'''
    
    return accordion_html

def convert_page_to_accordions(file_path):
    """Convert a page's text content to accordion format."""
    try:
        # Skip core pages
        if is_core_page(file_path):
            return 'skipped_core'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        post_content = soup.find('div', class_='post-content')
        if not post_content:
            return 'skipped_no_post_content'
        
        # Find all fusion-fullwidth boxes
        fullwidth_boxes = post_content.find_all('div', class_='fusion-fullwidth')
        
        modified = False
        
        for box in fullwidth_boxes:
            # Skip the first box (title/description)
            if box == fullwidth_boxes[0]:
                continue
            
            # Check if this box has plain text content (h2, p tags) but no accordion
            fusion_text = box.find('div', class_='fusion-text')
            if fusion_text:
                # Check if it already has accordion
                if box.find('div', class_='accordian') or box.find('div', class_='fusion-accordian'):
                    continue
                
                # Get the text content
                text_content = str(fusion_text)
                
                # Check if it has h2 tags (indicating sections that could be accordions)
                h2_tags = fusion_text.find_all('h2')
                if len(h2_tags) >= 2:  # At least 2 sections to make an accordion worthwhile
                    # Convert to accordion
                    accordion_html = convert_text_to_accordion(soup, text_content)
                    
                    if accordion_html:
                        # Replace fusion-text with accordion
                        accordion_soup = BeautifulSoup(accordion_html, 'html.parser')
                        fusion_text.replace_with(accordion_soup)
                        modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return 'converted'
        
        return 'skipped_no_sections'
    
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return 'error'

def main():
    """Main conversion process."""
    print(f"{'='*70}")
    print(f"Convert Text Content to Accordions")
    print(f"{'='*70}")
    print(f"Core pages to skip:")
    print(f"  - /services/seo/")
    print(f"  - /services/paid-search/")
    print(f"  - /services/creative/")
    print(f"  - /services/hubspot/")
    print()
    
    base_dir = Path('blackpropeller.com')
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} pages to check\n")
    
    stats = {
        'converted': 0,
        'skipped_core': 0,
        'skipped_no_post_content': 0,
        'skipped_no_sections': 0,
        'error': 0
    }
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        result = convert_page_to_accordions(html_file)
        
        if result == 'converted':
            stats['converted'] += 1
            print(f"  [OK] Converted to accordion format")
        elif result == 'skipped_core':
            stats['skipped_core'] += 1
            print(f"  - Skipped (core page)")
        elif result == 'skipped_no_post_content':
            stats['skipped_no_post_content'] += 1
            print(f"  - Skipped (no post-content div)")
        elif result == 'skipped_no_sections':
            stats['skipped_no_sections'] += 1
            print(f"  - Skipped (no sections to convert)")
        elif result == 'error':
            stats['error'] += 1
    
    print(f"\n{'='*70}")
    print(f"Conversion Complete!")
    print(f"  [OK] Converted: {stats['converted']} pages")
    print(f"  - Skipped (core pages): {stats['skipped_core']} pages")
    print(f"  - Skipped (no sections): {stats['skipped_no_sections']} pages")
    if stats['error'] > 0:
        print(f"  [ERROR] Errors: {stats['error']} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

