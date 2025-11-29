#!/usr/bin/env python3
"""
Restore missing content to all pages by:
1. Extracting title and description from each page
2. Expanding content using AI/paraphrasing
3. Restoring expanded content to pages
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import time

# Try to import OpenAI for paraphrasing (optional)
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("Note: OpenAI not installed. Will use built-in paraphrasing.")

def paraphrase_with_ai(text, context=""):
    """
    Paraphrase text using OpenAI API or built-in method.
    """
    if HAS_OPENAI and os.getenv('OPENAI_API_KEY'):
        try:
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional content writer. Paraphrase and expand the given text while maintaining the original meaning and tone. Make it natural and engaging."},
                    {"role": "user", "content": f"Paraphrase and expand this text: {text}\n\nContext: {context}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI paraphrasing failed: {e}, using built-in method")
    
    # Built-in simple paraphrasing (basic word substitution)
    # This is a fallback - you should integrate your actual paraphrasing tool here
    return text  # Placeholder - will be enhanced

def expand_content_from_title_description(title, description, page_type="service"):
    """
    Generate comprehensive content based on title and description.
    This function creates expanded content that can then be paraphrased.
    """
    
    # Determine content structure based on page type
    if page_type == "blog":
        content_structure = f"""
<h2>Introduction</h2>
<p>{description}</p>

<h2>Understanding {title}</h2>
<p>Let's explore the key concepts and strategies related to {title.lower()}. This comprehensive guide will help you understand the fundamentals and best practices.</p>

<h2>Key Benefits and Features</h2>
<p>When it comes to {title.lower()}, there are several important benefits to consider:</p>
<ul>
<li>Strategic implementation drives measurable results</li>
<li>Proper execution maximizes return on investment</li>
<li>Expert guidance ensures optimal performance</li>
<li>Continuous optimization improves outcomes over time</li>
</ul>

<h2>Best Practices</h2>
<p>To achieve success with {title.lower()}, follow these proven strategies:</p>
<ol>
<li>Develop a clear plan aligned with your business objectives</li>
<li>Implement tracking and measurement systems</li>
<li>Continuously monitor and optimize performance</li>
<li>Stay updated with industry trends and changes</li>
</ol>

<h2>Implementation Strategies</h2>
<p>Putting theory into practice requires careful planning. Here's how to get started:</p>
<ul>
<li><strong>Assessment:</strong> Evaluate your current situation and identify opportunities</li>
<li><strong>Planning:</strong> Create a detailed strategy with clear milestones</li>
<li><strong>Execution:</strong> Implement your plan with proper tracking</li>
<li><strong>Optimization:</strong> Refine your approach based on data and results</li>
</ul>

<h2>Common Challenges and Solutions</h2>
<p>Every business faces unique challenges. Here are some common issues and how to address them:</p>
<ul>
<li><strong>Resource Constraints:</strong> Prioritize high-impact activities and consider strategic partnerships</li>
<li><strong>Measuring ROI:</strong> Implement proper tracking and attribution models</li>
<li><strong>Staying Competitive:</strong> Focus on differentiation and unique value propositions</li>
</ul>

<h2>Conclusion</h2>
<p>Success with {title.lower()} requires a strategic approach, consistent effort, and continuous optimization. By following best practices and staying focused on your goals, you can achieve significant improvements in your digital marketing performance.</p>

<p>At Digital Growth Studios, we help businesses navigate these challenges and achieve their growth objectives. Our team of experts provides strategic guidance and hands-on support to drive measurable results.</p>
"""
    else:  # service page
        content_structure = f"""
<h2>About {title}</h2>
<p>{description}</p>

<h2>Why Choose Our {title} Services?</h2>
<p>Our {title.lower()} services are designed to deliver measurable results for businesses of all sizes. We combine strategic thinking with tactical execution to help you achieve your goals.</p>

<h2>Our Approach</h2>
<p>We take a comprehensive approach to {title.lower()}, focusing on:</p>
<ul>
<li>Strategic planning and goal setting</li>
<li>Data-driven decision making</li>
<li>Continuous optimization and improvement</li>
<li>Transparent reporting and communication</li>
</ul>

<h2>What We Offer</h2>
<p>Our {title.lower()} services include:</p>
<ul>
<li><strong>Comprehensive Strategy:</strong> We develop customized strategies tailored to your business needs</li>
<li><strong>Expert Execution:</strong> Our team of certified professionals handles implementation</li>
<li><strong>Ongoing Optimization:</strong> We continuously refine and improve performance</li>
<li><strong>Detailed Reporting:</strong> You'll receive regular reports on progress and results</li>
</ul>

<h2>Key Benefits</h2>
<p>When you work with us for {title.lower()}, you'll benefit from:</p>
<ul>
<li>Increased visibility and brand awareness</li>
<li>Improved conversion rates and ROI</li>
<li>Access to the latest tools and technologies</li>
<li>Dedicated support from experienced professionals</li>
</ul>

<h2>Getting Started</h2>
<p>Ready to improve your {title.lower()} performance? Contact us today to discuss your needs and learn how we can help you achieve your goals. Our team is ready to provide a customized solution that drives real results.</p>

<p>At Digital Growth Studios, we've helped hundreds of businesses succeed with {title.lower()}. Let us help you achieve your growth objectives.</p>
"""
    
    return content_structure.strip()

def extract_page_info(html_content):
    """Extract title, description, and page type from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else ""
    title = title.replace(' - Digital Growth Studios', '').replace('Digital Growth Studios - ', '').strip()
    
    # Get description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag.get('content', '') if desc_tag else ""
    
    # Determine page type from URL structure
    return title, description

def check_if_content_missing(html_content):
    """Check if page is missing substantial content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find post-content section
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Check for substantial content (h2 tags or long text)
    h2_tags = post_content.find_all('h2')
    text_content = post_content.get_text(strip=True)
    
    # If there are no h2 tags and text is short, content is missing
    if not h2_tags and len(text_content) < 500:
        return True
    
    return False

def restore_content_to_page(file_path):
    """Restore content to a single page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if content is missing
        if not check_if_content_missing(html_content):
            return False
        
        # Extract page info
        title, description = extract_page_info(html_content)
        
        if not title or not description:
            return False
        
        # Determine page type
        file_str = str(file_path)
        if '/blog/' in file_str:
            page_type = "blog"
        elif '/services/' in file_str:
            page_type = "service"
        elif '/company/' in file_str:
            page_type = "company"
        else:
            page_type = "page"
        
        # Generate expanded content
        expanded_content = expand_content_from_title_description(title, description, page_type)
        
        # Paraphrase the content
        # Split into sections and paraphrase each
        soup_content = BeautifulSoup(expanded_content, 'html.parser')
        
        # Paraphrase paragraphs
        for p_tag in soup_content.find_all('p'):
            original_text = p_tag.get_text()
            if len(original_text) > 50:  # Only paraphrase substantial paragraphs
                paraphrased = paraphrase_with_ai(original_text, context=f"Page about: {title}")
                if paraphrased and paraphrased != original_text:
                    p_tag.string = paraphrased
        
        # Paraphrase list items
        for li_tag in soup_content.find_all('li'):
            original_text = li_tag.get_text()
            if len(original_text) > 30:
                paraphrased = paraphrase_with_ai(original_text, context=f"Page about: {title}")
                if paraphrased and paraphrased != original_text:
                    li_tag.string = paraphrased
        
        # Now insert into the page
        soup = BeautifulSoup(html_content, 'html.parser')
        post_content = soup.find('div', class_='post-content')
        
        if not post_content:
            return False
        
        # Find the first fusion-fullwidth box
        first_fullwidth = post_content.find('div', class_='fusion-fullwidth')
        if first_fullwidth:
            # Create a new fusion-fullwidth box for the content
            new_fullwidth = soup.new_tag('div', class_='fusion-fullwidth fullwidth-box')
            new_row = soup.new_tag('div', class_='fusion-builder-row fusion-row')
            new_column = soup.new_tag('div', class_='fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column')
            new_wrapper = soup.new_tag('div', class_='fusion-column-wrapper')
            
            # Insert the paraphrased content
            new_wrapper.append(soup_content)
            new_column.append(new_wrapper)
            new_row.append(new_column)
            new_fullwidth.append(new_row)
            
            # Insert after the first fullwidth box
            first_fullwidth.insert_after(new_fullwidth)
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to restore content to all pages."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Directory {base_dir} not found!")
        return
    
    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))
    
    # Filter to only pages that likely need content (exclude wp-content, wp-includes, etc.)
    pages_to_process = [
        f for f in html_files 
        if 'wp-content' not in str(f) and 'wp-includes' not in str(f) 
        and 'index.html' in str(f) and f.parent.name not in ['wp-content', 'wp-includes', 'wp-json']
    ]
    
    print(f"Found {len(pages_to_process)} pages to process...")
    print("Starting content restoration...\n")
    
    restored_count = 0
    for i, html_file in enumerate(pages_to_process, 1):
        if restore_content_to_page(html_file):
            restored_count += 1
            print(f"[{i}/{len(pages_to_process)}] Restored: {html_file}")
        
        # Rate limiting for AI API
        if HAS_OPENAI and i % 10 == 0:
            time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"Completed! Restored content to {restored_count} out of {len(pages_to_process)} pages.")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

