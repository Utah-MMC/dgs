#!/usr/bin/env python3
"""
Comprehensive content restoration script.
Scans pages, extracts titles/descriptions, generates content, and paraphrases it.
"""

import os
import re
import json
import random
from pathlib import Path
from bs4 import BeautifulSoup
import time

def paraphrase_text(text, context=""):
    """
    Paraphrase text using AI. 
    This function will use OpenAI if available, otherwise it provides a placeholder
    for your custom paraphrasing tool integration.
    """
    # Skip very short text
    if len(text.strip()) < 20:
        return text
    
    # Try OpenAI if available
    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using cheaper model for bulk processing
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional content writer. Paraphrase the following text while maintaining the original meaning, tone, and key information. Make it natural, engaging, and professionally written. Do not change technical terms, brand names, or specific numbers."
                    },
                    {
                        "role": "user", 
                        "content": f"Paraphrase this text for a digital marketing website:\n\n{text}\n\nContext: {context}\n\nProvide only the paraphrased text, no explanations."
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )
            paraphrased = response.choices[0].message.content.strip()
            # Remove quotes if AI wrapped the response
            if paraphrased.startswith('"') and paraphrased.endswith('"'):
                paraphrased = paraphrased[1:-1]
            return paraphrased
    except ImportError:
        pass
    except Exception as e:
        print(f"    AI paraphrasing failed: {e}")
    
    # TODO: Integrate your custom paraphrasing tool here
    # Example:
    # return your_paraphrasing_api(text, context)
    # or
    # return your_local_paraphrasing_function(text)
    
    # Basic fallback - simple word substitution (not ideal, but better than nothing)
    # This should be replaced with your actual tool
    word_replacements = {
        r'\bwe\b': 'our team',
        r'\bour\b': 'we' if random.random() > 0.5 else 'our',
        r'\bhelp\b': 'assist',
        r'\bservices\b': 'solutions',
        r'\bbusiness\b': 'company',
        r'\bcompanies\b': 'organizations',
        r'\bprovide\b': 'deliver',
        r'\bensure\b': 'guarantee',
    }
    
    result = text
    for pattern, replacement in word_replacements.items():
        if random.random() > 0.6:  # Only apply some replacements
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result if result != text else text

def generate_comprehensive_content(title, description, page_type="service"):
    """
    Generate comprehensive content structure based on title and description.
    The content will then be paraphrased.
    """
    
    # Clean title for use in content
    clean_title = title.replace(' - Digital Growth Studios', '').strip()
    
    if page_type == "blog":
        content = f"""<h2>Introduction</h2>
<p>{description}</p>

<h2>Understanding {clean_title}</h2>
<p>In today's digital landscape, {clean_title.lower()} has become increasingly important for businesses looking to grow and succeed. This comprehensive guide explores the key concepts, strategies, and best practices that can help you achieve your goals.</p>

<h2>Key Concepts and Fundamentals</h2>
<p>Before diving into implementation, it's essential to understand the core principles of {clean_title.lower()}. These fundamentals form the foundation for successful strategies:</p>
<ul>
<li>Strategic planning and goal alignment</li>
<li>Data-driven decision making</li>
<li>Continuous optimization and improvement</li>
<li>Measurement and performance tracking</li>
</ul>

<h2>Benefits and Advantages</h2>
<p>Implementing effective {clean_title.lower()} strategies offers numerous benefits:</p>
<ul>
<li><strong>Improved Performance:</strong> Better results and higher ROI</li>
<li><strong>Competitive Advantage:</strong> Stay ahead of competitors</li>
<li><strong>Scalability:</strong> Grow your business efficiently</li>
<li><strong>Expertise Access:</strong> Leverage professional knowledge and tools</li>
</ul>

<h2>Best Practices and Strategies</h2>
<p>To maximize success with {clean_title.lower()}, follow these proven approaches:</p>
<ol>
<li><strong>Develop a Clear Strategy:</strong> Define your objectives and create a roadmap</li>
<li><strong>Implement Proper Tracking:</strong> Set up measurement systems from the start</li>
<li><strong>Focus on Quality:</strong> Prioritize high-impact activities over quantity</li>
<li><strong>Continuously Optimize:</strong> Regularly review and improve your approach</li>
<li><strong>Stay Updated:</strong> Keep abreast of industry changes and trends</li>
</ol>

<h2>Implementation Guide</h2>
<p>Getting started with {clean_title.lower()} requires careful planning:</p>
<ul>
<li><strong>Assessment Phase:</strong> Evaluate your current situation and identify opportunities</li>
<li><strong>Planning Phase:</strong> Develop a detailed strategy with clear milestones</li>
<li><strong>Execution Phase:</strong> Implement your plan with proper tracking</li>
<li><strong>Optimization Phase:</strong> Refine your approach based on data and results</li>
</ul>

<h2>Common Challenges and Solutions</h2>
<p>Many businesses face similar challenges when implementing {clean_title.lower()}. Here's how to address them:</p>
<ul>
<li><strong>Resource Limitations:</strong> Focus on high-impact activities and consider strategic partnerships</li>
<li><strong>Measuring ROI:</strong> Implement comprehensive tracking and attribution models</li>
<li><strong>Staying Competitive:</strong> Differentiate through unique value propositions and innovation</li>
<li><strong>Scaling Effectively:</strong> Build systems that can grow with your business</li>
</ul>

<h2>Why Choose Professional Services</h2>
<p>Working with experienced professionals for {clean_title.lower()} provides significant advantages:</p>
<ul>
<li>Access to specialized expertise and knowledge</li>
<li>Proven methodologies and best practices</li>
<li>Advanced tools and technologies</li>
<li>Dedicated support and ongoing optimization</li>
</ul>

<h2>Conclusion</h2>
<p>Success with {clean_title.lower()} requires a strategic approach, consistent effort, and continuous optimization. By following best practices and leveraging professional expertise, you can achieve significant improvements in your digital marketing performance.</p>

<p>At Digital Growth Studios, we specialize in helping businesses succeed with {clean_title.lower()}. Our team of experts provides strategic guidance, hands-on implementation, and ongoing support to drive measurable results. Contact us today to learn how we can help you achieve your growth objectives.</p>"""
    
    else:  # service or other page
        content = f"""<h2>About {clean_title}</h2>
<p>{description}</p>

<h2>Why Choose Our {clean_title} Services?</h2>
<p>Our {clean_title.lower()} services are designed to deliver measurable results for businesses of all sizes. We combine strategic thinking with tactical execution to help you achieve your marketing and growth objectives.</p>

<h2>Our Comprehensive Approach</h2>
<p>We take a holistic approach to {clean_title.lower()}, ensuring every aspect is optimized for success:</p>
<ul>
<li><strong>Strategic Planning:</strong> We develop customized strategies tailored to your specific business needs and goals</li>
<li><strong>Expert Execution:</strong> Our team of certified professionals handles implementation with precision and care</li>
<li><strong>Continuous Optimization:</strong> We regularly monitor performance and make data-driven improvements</li>
<li><strong>Transparent Reporting:</strong> You'll receive detailed reports on progress, results, and recommendations</li>
</ul>

<h2>What We Offer</h2>
<p>Our {clean_title.lower()} services include a comprehensive range of solutions:</p>
<ul>
<li><strong>Strategy Development:</strong> Custom strategies aligned with your business objectives</li>
<li><strong>Implementation Services:</strong> Hands-on execution by experienced professionals</li>
<li><strong>Performance Monitoring:</strong> Ongoing tracking and analysis of key metrics</li>
<li><strong>Optimization Services:</strong> Continuous refinement to improve results</li>
<li><strong>Reporting and Analytics:</strong> Regular insights into performance and opportunities</li>
</ul>

<h2>Key Benefits</h2>
<p>When you partner with us for {clean_title.lower()}, you'll experience:</p>
<ul>
<li><strong>Increased Visibility:</strong> Enhanced brand awareness and online presence</li>
<li><strong>Better Results:</strong> Improved conversion rates and return on investment</li>
<li><strong>Access to Tools:</strong> Premium platforms and technologies at your disposal</li>
<li><strong>Expert Support:</strong> Dedicated professionals focused on your success</li>
<li><strong>Scalable Growth:</strong> Solutions that grow with your business</li>
</ul>

<h2>Our Process</h2>
<p>We follow a proven process to ensure success:</p>
<ol>
<li><strong>Discovery:</strong> We start by understanding your business, goals, and challenges</li>
<li><strong>Strategy:</strong> We develop a customized plan tailored to your needs</li>
<li><strong>Implementation:</strong> We execute the strategy with attention to detail</li>
<li><strong>Optimization:</strong> We continuously refine and improve performance</li>
<li><strong>Reporting:</strong> We provide regular updates on progress and results</li>
</ol>

<h2>Industries We Serve</h2>
<p>Our {clean_title.lower()} services benefit businesses across various industries, including:</p>
<ul>
<li>E-commerce and retail</li>
<li>Healthcare and wellness</li>
<li>Professional services</li>
<li>Technology and SaaS</li>
<li>Home services</li>
<li>And many more</li>
</ul>

<h2>Getting Started</h2>
<p>Ready to improve your {clean_title.lower()} performance? Contact us today to discuss your needs and learn how we can help you achieve your goals. Our team is ready to provide a customized solution that drives real, measurable results.</p>

<p>At Digital Growth Studios, we've helped hundreds of businesses succeed with {clean_title.lower()}. With our expertise, proven methodologies, and dedicated support, we can help you achieve your growth objectives. Let's start a conversation about how we can help your business thrive.</p>"""
    
    return content

def extract_page_metadata(html_content):
    """Extract title, description, and determine page type."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else ""
    title = title.replace(' - Digital Growth Studios', '').replace('Digital Growth Studios - ', '').strip()
    
    # Get description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag.get('content', '') if desc_tag else ""
    
    return title, description

def needs_content_restoration(html_content):
    """Check if page needs content restoration."""
    soup = BeautifulSoup(html_content, 'html.parser')
    post_content = soup.find('div', class_='post-content')
    
    if not post_content:
        return False
    
    # Check for substantial content
    h2_tags = post_content.find_all('h2')
    text_content = post_content.get_text(strip=True)
    
    # Missing content if no h2 tags and text is short
    return len(h2_tags) == 0 and len(text_content) < 500

def restore_page_content(file_path):
    """Restore content to a single page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if restoration needed
        if not needs_content_restoration(html_content):
            return False
        
        # Extract metadata
        title, description = extract_page_metadata(html_content)
        
        if not title or not description:
            print(f"  Skipping {file_path}: Missing title or description")
            return False
        
        # Determine page type
        file_str = str(file_path)
        if '/blog/' in file_str:
            page_type = "blog"
        elif '/services/' in file_str:
            page_type = "service"
        elif '/company/' in file_str or '/team/' in file_str or '/careers/' in file_str:
            page_type = "company"
        elif '/results/' in file_str or '/case-studies/' in file_str:
            page_type = "case-study"
        else:
            page_type = "page"
        
        # Generate content
        content_html = generate_comprehensive_content(title, description, page_type)
        
        # Parse the generated content
        content_soup = BeautifulSoup(content_html, 'html.parser')
        
        # Paraphrase all text content (paragraphs and list items)
        for element in content_soup.find_all(['p', 'li']):
            # Get all text nodes in this element
            for text_node in element.find_all(string=True, recursive=False):
                original = str(text_node).strip()
                if len(original) > 30:  # Only paraphrase substantial text
                    paraphrased = paraphrase_text(original, context=f"{title}: {description}")
                    if paraphrased and paraphrased != original:
                        text_node.replace_with(paraphrased)
            
            # Also check for text directly in the element
            if element.string and len(element.string.strip()) > 30:
                original = element.string.strip()
                paraphrased = paraphrase_text(original, context=f"{title}: {description}")
                if paraphrased and paraphrased != original:
                    element.string = paraphrased
        
        # Now insert into page
        soup = BeautifulSoup(html_content, 'html.parser')
        post_content = soup.find('div', class_='post-content')
        
        if not post_content:
            return False
        
        # Find first fusion-fullwidth box
        first_fullwidth = post_content.find('div', class_='fusion-fullwidth')
        if not first_fullwidth:
            return False
        
        # Create new content section with proper attributes
        new_fullwidth = soup.new_tag('div')
        new_fullwidth['class'] = 'fusion-fullwidth fullwidth-box'
        new_row = soup.new_tag('div')
        new_row['class'] = 'fusion-builder-row fusion-row'
        new_column = soup.new_tag('div')
        new_column['class'] = 'fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column'
        new_wrapper = soup.new_tag('div')
        new_wrapper['class'] = 'fusion-column-wrapper'
        
        # Insert paraphrased content
        new_wrapper.append(content_soup)
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
        print(f"Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main restoration process."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    # Find all index.html files (excluding wp-content, wp-includes, etc.)
    html_files = []
    for html_file in base_dir.rglob('index.html'):
        file_str = str(html_file)
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"{'='*70}")
    print(f"Content Restoration Script")
    print(f"{'='*70}")
    print(f"Found {len(html_files)} pages to check")
    print(f"\nNote: Make sure to integrate your paraphrasing tool in the")
    print(f"      paraphrase_text() function before running this script.")
    print(f"{'='*70}\n")
    
    restored = 0
    skipped = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Checking: {rel_path}")
        
        if restore_page_content(html_file):
            restored += 1
            print(f"  ✓ Content restored")
        else:
            skipped += 1
            print(f"  - Skipped (content already exists or missing metadata)")
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  Restored: {restored} pages")
    print(f"  Skipped: {skipped} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

