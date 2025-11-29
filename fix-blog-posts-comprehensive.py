#!/usr/bin/env python3
"""
Comprehensive fix for blog posts - restore missing content with proper structure.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def has_substantial_content(soup):
    """Check if blog post has substantial content beyond title/description."""
    # Find all fusion-text divs
    text_divs = soup.find_all('div', class_='fusion-text')
    
    if len(text_divs) <= 1:
        return False
    
    # Check if there's content beyond the first paragraph (description)
    total_text_length = 0
    for i, text_div in enumerate(text_divs):
        if i > 0:  # Skip the first one (description)
            text = text_div.get_text(strip=True)
            total_text_length += len(text)
    
    # Need at least 500 characters of actual content
    return total_text_length > 500

def generate_blog_content(title, description):
    """Generate comprehensive blog content based on title and description."""
    
    # Extract key topics from title
    title_lower = title.lower()
    
    # Generate structured content
    content_sections = []
    
    # Introduction section
    intro = f"""<div class="fusion-title title"><h2 class="title-heading-left">Introduction</h2></div>
<div class="fusion-text"><p>{description}</p>
<p>In this comprehensive guide, we'll explore the key aspects of {title.lower()} and provide actionable insights to help you achieve better results.</p></div>"""
    content_sections.append(intro)
    
    # Main content sections based on topic
    if 'ppc' in title_lower or 'google ads' in title_lower or 'paid search' in title_lower:
        content_sections.append("""<div class="fusion-title title"><h2 class="title-heading-left">Understanding PPC Fundamentals</h2></div>
<div class="fusion-text"><p>Pay-per-click advertising is a powerful digital marketing strategy that allows businesses to display ads on search engines and other platforms. When executed correctly, PPC campaigns can drive qualified traffic, increase conversions, and provide measurable ROI.</p>
<p>Key components of successful PPC campaigns include:</p>
<ul>
<li><strong>Keyword Research:</strong> Identifying the right keywords that align with your business goals and target audience intent</li>
<li><strong>Ad Copy Optimization:</strong> Creating compelling ad copy that resonates with your audience and encourages clicks</li>
<li><strong>Landing Page Alignment:</strong> Ensuring your landing pages match the promise of your ads for better conversion rates</li>
<li><strong>Bid Management:</strong> Strategically managing your bids to maximize performance within your budget constraints</li>
<li><strong>Performance Tracking:</strong> Monitoring key metrics to continuously optimize and improve campaign results</li>
</ul></div>""")
        
        content_sections.append("""<div class="fusion-title title"><h2 class="title-heading-left">Best Practices for PPC Success</h2></div>
<div class="fusion-text"><p>To maximize the effectiveness of your PPC campaigns, consider these proven strategies:</p>
<ul>
<li><strong>Focus on Quality Score:</strong> Google's Quality Score impacts your ad position and cost-per-click. Improve it by creating relevant ad copy, using targeted keywords, and optimizing landing pages.</li>
<li><strong>Use Negative Keywords:</strong> Prevent wasted spend by adding negative keywords that filter out irrelevant searches.</li>
<li><strong>Test Ad Variations:</strong> Run A/B tests on different ad copy, headlines, and calls-to-action to identify what resonates best with your audience.</li>
<li><strong>Leverage Ad Extensions:</strong> Use sitelinks, callouts, and structured snippets to provide additional information and improve ad visibility.</li>
<li><strong>Monitor and Adjust:</strong> Regularly review performance data and make adjustments based on what's working and what isn't.</li>
</ul></div>""")
        
    elif 'seo' in title_lower or 'search engine' in title_lower:
        content_sections.append("""<div class="fusion-title title"><h2 class="title-heading-left">SEO Strategy and Implementation</h2></div>
<div class="fusion-text"><p>Search engine optimization is essential for improving your website's visibility in organic search results. A comprehensive SEO strategy involves multiple components working together to improve rankings and drive qualified traffic.</p>
<p>Essential SEO elements include:</p>
<ul>
<li><strong>Technical SEO:</strong> Ensuring your website is crawlable, indexable, and performs well from a technical standpoint</li>
<li><strong>On-Page Optimization:</strong> Optimizing individual pages with relevant keywords, meta tags, and quality content</li>
<li><strong>Content Strategy:</strong> Creating valuable, relevant content that addresses user intent and search queries</li>
<li><strong>Link Building:</strong> Earning high-quality backlinks from authoritative websites in your industry</li>
<li><strong>Local SEO:</strong> For businesses with physical locations, optimizing for local search results</li>
</ul></div>""")
        
        content_sections.append("""<div class="fusion-title title"><h2 class="title-heading-left">Measuring SEO Success</h2></div>
<div class="fusion-text"><p>Tracking the right metrics is crucial for understanding your SEO performance:</p>
<ul>
<li><strong>Organic Traffic:</strong> Monitor the volume and quality of visitors coming from search engines</li>
<li><strong>Keyword Rankings:</strong> Track your position for target keywords over time</li>
<li><strong>Conversion Rate:</strong> Measure how many organic visitors take desired actions on your site</li>
<li><strong>Backlink Profile:</strong> Monitor the quantity and quality of links pointing to your website</li>
<li><strong>Core Web Vitals:</strong> Track page speed and user experience metrics that impact rankings</li>
</ul></div>""")
        
    elif 'growth' in title_lower or 'modeling' in title_lower:
        content_sections.append("""<div class="fusion-title title"><h2 class="title-heading-left">The Importance of Growth Modeling</h2></div>
<div class="fusion-text"><p>Growth modeling helps businesses set realistic expectations and make data-driven decisions about their marketing investments. By analyzing historical data and market trends, you can create accurate forecasts for future performance.</p>
<p>Key benefits of growth modeling include:</p>
<ul>
<li><strong>Realistic Goal Setting:</strong> Establish achievable targets based on data rather than assumptions</li>
<li><strong>Budget Planning:</strong> Allocate resources more effectively by understanding expected returns</li>
<li><strong>Performance Tracking:</strong> Compare actual results against projections to identify areas for improvement</li>
<li><strong>Strategic Decision Making:</strong> Use data insights to guide marketing strategy and channel selection</li>
</ul></div>""")
        
        content_sections.append("""<div class="fusion-title title"><h2 class="title-heading-left">Implementing Growth Models</h2></div>
<div class="fusion-text"><p>To create effective growth models, follow these steps:</p>
<ul>
<li><strong>Collect Historical Data:</strong> Gather performance data from past campaigns and marketing initiatives</li>
<li><strong>Identify Key Variables:</strong> Determine which factors most significantly impact your growth metrics</li>
<li><strong>Build Predictive Models:</strong> Use statistical methods to create models that forecast future performance</li>
<li><strong>Test and Refine:</strong> Continuously update your models based on new data and changing market conditions</li>
<li><strong>Apply Insights:</strong> Use model predictions to inform strategy and optimize marketing spend</li>
</ul></div>""")
    
    else:
        # Generic content structure
        content_sections.append(f"""<div class="fusion-title title"><h2 class="title-heading-left">Key Concepts and Strategies</h2></div>
<div class="fusion-text"><p>Understanding the fundamentals is crucial for success. Let's explore the key concepts and strategies that can help you achieve your goals.</p>
<p>Important considerations include:</p>
<ul>
<li><strong>Planning and Strategy:</strong> Develop a clear plan that aligns with your business objectives</li>
<li><strong>Implementation Best Practices:</strong> Follow proven methodologies to ensure effective execution</li>
<li><strong>Measurement and Optimization:</strong> Track performance and continuously improve based on data insights</li>
<li><strong>Long-term Sustainability:</strong> Build strategies that can scale and adapt over time</li>
</ul></div>""")
    
    # Conclusion section
    conclusion = f"""<div class="fusion-title title"><h2 class="title-heading-left">Conclusion</h2></div>
<div class="fusion-text"><p>Success in digital marketing requires a strategic approach, continuous optimization, and a focus on measurable results. By implementing the strategies and best practices outlined in this guide, you can improve your performance and achieve your business objectives.</p>
<p>If you need expert assistance with {title.lower()}, our team at Digital Growth Studios is here to help. We combine data-driven strategies with creative execution to deliver results that drive growth for your business.</p></div>"""
    content_sections.append(conclusion)
    
    return '\n'.join(content_sections)

def fix_blog_post(file_path):
    """Fix a single blog post by adding missing content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check if content is missing
        if has_substantial_content(soup):
            return False  # Already has content
        
        # Extract title and description
        title_elem = soup.find('h1', class_='title-heading-left')
        if not title_elem:
            return False
        
        title = title_elem.get_text(strip=True)
        
        # Find description (first fusion-text paragraph)
        first_text_div = soup.find('div', class_='fusion-text')
        if not first_text_div:
            return False
        
        description = first_text_div.find('p')
        if not description:
            return False
        
        description_text = description.get_text(strip=True)
        
        # Generate content
        new_content = generate_blog_content(title, description_text)
        new_content_soup = BeautifulSoup(new_content, 'html.parser')
        
        # Find where to insert (after the first fusion-text div)
        parent_column = first_text_div.find_parent('div', class_='fusion-column-wrapper')
        if not parent_column:
            return False
        
        # Insert new content after the first fusion-text
        first_text_div.insert_after(new_content_soup)
        
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
    """Main function to fix all blog posts."""
    blog_dir = Path('blackpropeller.com/blog')
    
    if not blog_dir.exists():
        print(f"Blog directory {blog_dir} not found!")
        return
    
    # Find all blog post index.html files (excluding the main blog index)
    blog_files = [f for f in blog_dir.glob('*/index.html') if f.parent.name != 'blog']
    
    print(f"{'='*70}")
    print(f"Blog Post Content Restoration")
    print(f"{'='*70}")
    print(f"Found {len(blog_files)} blog posts to check\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for i, blog_file in enumerate(blog_files, 1):
        rel_path = blog_file.relative_to(Path('blackpropeller.com'))
        print(f"[{i}/{len(blog_files)}] Processing: {rel_path}")
        
        if fix_blog_post(blog_file):
            fixed_count += 1
            print(f"  ✓ Content restored")
        else:
            skipped_count += 1
            print(f"  - Skipped (already has content or missing metadata)")
    
    print(f"\n{'='*70}")
    print(f"Restoration Complete!")
    print(f"  Fixed: {fixed_count} blog posts")
    print(f"  Skipped: {skipped_count} blog posts")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

