#!/usr/bin/env python3
"""
Fix HTML structure issues and restore content with proper AI paraphrasing.
This script:
1. Fixes broken HTML (class_= instead of class=)
2. Extracts content from pages or generates based on title/description
3. Uses AI to paraphrase the content
4. Restores it to pages
"""

import os
import re
import json
import random
from pathlib import Path
from bs4 import BeautifulSoup
import time
import warnings

# Suppress BeautifulSoup warnings
warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def paraphrase_with_ai(text, context=""):
    """
    Paraphrase text using OpenAI API.
    Replace this function to use your custom paraphrasing tool.
    """
    # Try OpenAI if available
    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional content writer. Paraphrase the following text while maintaining the original meaning, tone, and key information. Make it natural, engaging, and professionally written. Preserve technical terms, brand names, and specific numbers exactly as they appear."
                    },
                    {
                        "role": "user",
                        "content": f"Paraphrase this text for a digital marketing agency website:\n\n{text}\n\nContext: {context}\n\nProvide only the paraphrased text, no explanations or quotes."
                    }
                ],
                temperature=0.75,
                max_tokens=500
            )
            result = response.choices[0].message.content.strip()
            # Clean up if AI wrapped in quotes
            if result.startswith('"') and result.endswith('"'):
                result = result[1:-1]
            if result.startswith("'") and result.endswith("'"):
                result = result[1:-1]
            return result
    except ImportError:
        pass
    except Exception as e:
        print(f"    AI error: {str(e)[:50]}")
    
    # TODO: Replace this with your custom paraphrasing tool
    # Example: return your_paraphrasing_tool(text, context)
    
    # Basic fallback (not ideal - should use your tool)
    return text

def fix_broken_html(html_content):
    """Fix broken HTML attributes (class_= to class=)."""
    # Fix class_= to class=
    html_content = re.sub(r'class_="([^"]*)"', r'class="\1"', html_content)
    html_content = re.sub(r"class_='([^']*)'", r"class='\1'", html_content)
    
    return html_content

def extract_content_from_backup(file_path):
    """
    Try to extract original content from backup files or similar pages.
    Returns None if no backup content found.
    """
    # Check for backup file
    backup_path = file_path.parent / f"{file_path.stem}.backup"
    if backup_path.exists():
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            soup = BeautifulSoup(backup_content, 'html.parser')
            post_content = soup.find('div', class_='post-content')
            if post_content:
                # Extract substantial content
                h2_tags = post_content.find_all('h2')
                if h2_tags:
                    return str(post_content)
        except:
            pass
    
    return None

def generate_comprehensive_content(title, description, page_type="service"):
    """Generate comprehensive content based on title and description."""
    clean_title = title.replace(' - Digital Growth Studios', '').strip()
    
    if page_type == "blog":
        sections = [
            ("Introduction", description),
            (f"Understanding {clean_title}", f"In today's digital landscape, {clean_title.lower()} plays a crucial role in business success. This comprehensive guide explores key concepts, strategies, and best practices."),
            ("Key Concepts", "Before implementation, understanding core principles is essential. These fundamentals form the foundation for successful strategies."),
            ("Benefits", "Implementing effective strategies offers numerous advantages including improved performance, competitive advantage, and scalability."),
            ("Best Practices", "To maximize success, follow proven approaches: develop clear strategies, implement proper tracking, focus on quality, and continuously optimize."),
            ("Implementation Guide", "Getting started requires careful planning through assessment, strategy development, execution, and optimization phases."),
            ("Common Challenges", "Many businesses face similar challenges. Address resource limitations, ROI measurement, and competitive positioning strategically."),
            ("Conclusion", f"Success with {clean_title.lower()} requires strategic approach and continuous optimization. At Digital Growth Studios, we help businesses achieve their growth objectives.")
        ]
    else:
        sections = [
            (f"About {clean_title}", description),
            (f"Why Choose Our {clean_title} Services?", f"Our {clean_title.lower()} services deliver measurable results. We combine strategic thinking with tactical execution."),
            ("Our Comprehensive Approach", "We take a holistic approach ensuring every aspect is optimized: strategic planning, expert execution, continuous optimization, and transparent reporting."),
            ("What We Offer", "Our services include strategy development, implementation, performance monitoring, optimization, and detailed reporting."),
            ("Key Benefits", "Partner with us to experience increased visibility, better results, access to premium tools, expert support, and scalable growth."),
            ("Our Process", "We follow a proven process: discovery, strategy development, implementation, optimization, and regular reporting."),
            ("Getting Started", f"Ready to improve your {clean_title.lower()} performance? Contact us to discuss your needs and learn how we can help achieve your goals.")
        ]
    
    content_html = ""
    for heading, paragraph in sections:
        content_html += f'<h2>{heading}</h2>\n<p>{paragraph}</p>\n\n'
    
    # Add some list sections
    if page_type == "service":
        content_html += '''<h2>Industries We Serve</h2>
<p>Our services benefit businesses across various industries:</p>
<ul>
<li>E-commerce and retail</li>
<li>Healthcare and wellness</li>
<li>Professional services</li>
<li>Technology and SaaS</li>
<li>Home services</li>
<li>And many more</li>
</ul>'''
    
    return content_html

def restore_page_content(file_path):
    """Restore content to a single page with proper HTML structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Fix broken HTML first
        html_content = fix_broken_html(html_content)
        
        # Check if content restoration needed
        soup = BeautifulSoup(html_content, 'html.parser')
        post_content = soup.find('div', class_='post-content')
        
        if not post_content:
            return False
        
        # Check for substantial content
        h2_tags = post_content.find_all('h2')
        text_content = post_content.get_text(strip=True)
        
        # Skip if already has content
        if h2_tags and len(text_content) > 800:
            return False
        
        # Extract metadata
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else ""
        title = title.replace(' - Digital Growth Studios', '').replace('Digital Growth Studios - ', '').strip()
        
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        description = desc_tag.get('content', '') if desc_tag else ""
        
        if not title or not description:
            return False
        
        # Determine page type
        file_str = str(file_path)
        if '/blog/' in file_str:
            page_type = "blog"
        elif '/services/' in file_str:
            page_type = "service"
        else:
            page_type = "page"
        
        # Try to get content from backup first
        backup_content = extract_content_from_backup(file_path)
        
        if backup_content:
            # Use backup content and paraphrase it
            backup_soup = BeautifulSoup(backup_content, 'html.parser')
            # Paraphrase paragraphs
            for p in backup_soup.find_all('p'):
                if p.string and len(p.string.strip()) > 50:
                    paraphrased = paraphrase_with_ai(p.string.strip(), context=f"{title}: {description}")
                    if paraphrased:
                        p.string = paraphrased
            content_html = str(backup_soup)
        else:
            # Generate new content
            content_html = generate_comprehensive_content(title, description, page_type)
            content_soup = BeautifulSoup(content_html, 'html.parser')
            
            # Paraphrase all paragraphs
            for p in content_soup.find_all('p'):
                if p.string and len(p.string.strip()) > 30:
                    paraphrased = paraphrase_with_ai(p.string.strip(), context=f"{title}: {description}")
                    if paraphrased:
                        p.string = paraphrased
            
            content_html = str(content_soup)
        
        # Parse the content
        new_content_soup = BeautifulSoup(content_html, 'html.parser')
        
        # Find first fusion-fullwidth in post-content
        first_fullwidth = post_content.find('div', class_='fusion-fullwidth')
        if not first_fullwidth:
            return False
        
        # Create new content section with proper HTML
        new_fullwidth = soup.new_tag('div')
        new_fullwidth['class'] = 'fusion-fullwidth fullwidth-box'
        
        new_row = soup.new_tag('div')
        new_row['class'] = 'fusion-builder-row fusion-row'
        
        new_column = soup.new_tag('div')
        new_column['class'] = 'fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column'
        
        new_wrapper = soup.new_tag('div')
        new_wrapper['class'] = 'fusion-column-wrapper'
        
        # Insert the paraphrased content
        for element in new_content_soup.children:
            new_wrapper.append(element)
        
        new_column.append(new_wrapper)
        new_row.append(new_column)
        new_fullwidth.append(new_row)
        
        # Insert after first fullwidth
        first_fullwidth.insert_after(new_fullwidth)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error: {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main restoration process."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    # Find all index.html files
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"{'='*70}")
    print(f"Content Restoration with AI Paraphrasing")
    print(f"{'='*70}")
    print(f"Found {len(html_files)} pages to process")
    print(f"\nNote: Using OpenAI API for paraphrasing (set OPENAI_API_KEY env var)")
    print(f"      Or modify paraphrase_with_ai() to use your custom tool")
    print(f"{'='*70}\n")
    
    restored = 0
    fixed_html = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        # Check if HTML needs fixing
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'class_=' in content:
            fixed_html += 1
        
        if restore_page_content(html_file):
            restored += 1
            print(f"  ✓ Content restored")
        else:
            print(f"  - Skipped")
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  Restored: {restored} pages")
    print(f"  HTML fixed: {fixed_html} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

