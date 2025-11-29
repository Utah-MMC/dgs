#!/usr/bin/env python3
"""
Fix missing content and broken header links across all pages.
1. Fix header navigation links (replace anchor links with proper page URLs)
2. Add missing content to blog posts and other pages
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html

# Service anchor link mappings
SERVICE_LINK_MAP = {
    '#seo': '/services/seo/',
    '#google-ads': '/services/paid-search/',
    '#web-design': '/services/',  # No specific web design page, link to services index
    '#analytics': '/services/',  # No specific analytics page, link to services index
    '#core-services': '/services/',
}

# Blog post content templates based on titles
BLOG_CONTENT_TEMPLATES = {
    'seo-powers-ai': {
        'title': 'How SEO Powers AI Search',
        'content': '''<h2>Understanding the Connection Between SEO and AI Search</h2>
<p>As artificial intelligence continues to reshape how users search for information, understanding the relationship between SEO and AI search has become crucial for businesses. Search engine optimization isn't just about ranking on Google anymore—it's about ensuring your content appears in AI-generated answers across platforms like ChatGPT, Google's AI Overviews, and other AI-powered search tools.</p>

<h2>Why SEO Matters for AI Search</h2>
<p>AI search engines rely heavily on the same signals that traditional search engines use to evaluate content quality and relevance. These include:</p>
<ul>
<li><strong>Content Authority:</strong> Well-optimized, authoritative content is more likely to be cited by AI systems</li>
<li><strong>Structured Data:</strong> Proper schema markup helps AI understand your content's context</li>
<li><strong>User Engagement:</strong> High-quality content that users engage with signals value to AI systems</li>
<li><strong>E-E-A-T Signals:</strong> Experience, Expertise, Authoritativeness, and Trustworthiness matter to both search engines and AI</li>
</ul>

<h2>How to Optimize for AI Search</h2>
<p>To ensure your business appears in AI-generated answers, focus on:</p>
<ol>
<li><strong>Comprehensive Content:</strong> Create detailed, well-researched content that thoroughly answers user questions</li>
<li><strong>Natural Language:</strong> Write in a conversational tone that matches how people actually ask questions</li>
<li><strong>Clear Structure:</strong> Use headings, bullet points, and formatting to make content easily digestible</li>
<li><strong>Regular Updates:</strong> Keep content fresh and up-to-date with current information</li>
<li><strong>Technical SEO:</strong> Ensure fast load times, mobile optimization, and proper technical implementation</li>
</ol>

<h2>The Future of Search</h2>
<p>As AI search becomes more prevalent, businesses that invest in comprehensive SEO strategies will have a significant advantage. By optimizing for both traditional search engines and AI systems, you can ensure your brand appears wherever users are seeking information—whether that's through a Google search, a ChatGPT conversation, or an AI-powered assistant.</p>

<p>At Digital Growth Studios, we help businesses optimize their content for the future of search. Our SEO strategies are designed to work across all search platforms, ensuring maximum visibility and engagement.</p>'''
    },
    'what-is-ppc': {
        'title': 'What Is PPC? How Does Pay-Per-Click Advertising Work',
        'content': '''<h2>Understanding Pay-Per-Click Advertising</h2>
<p>Pay-Per-Click (PPC) advertising is a digital marketing model where advertisers pay a fee each time their ad is clicked. It's one of the most effective ways to drive immediate traffic to your website and generate leads or sales.</p>

<h2>How PPC Works</h2>
<p>PPC advertising operates on an auction-based system. When a user searches for a keyword related to your business, search engines like Google run an auction to determine which ads appear. The auction considers:</p>
<ul>
<li><strong>Bid Amount:</strong> How much you're willing to pay per click</li>
<li><strong>Quality Score:</strong> The relevance and quality of your ad and landing page</li>
<li><strong>Ad Rank:</strong> A combination of bid and quality that determines ad position</li>
</ul>

<h2>Key PPC Platforms</h2>
<p>The most popular PPC platforms include:</p>
<ul>
<li><strong>Google Ads:</strong> The largest PPC platform, reaching users across Google Search, Display Network, YouTube, and more</li>
<li><strong>Microsoft Advertising:</strong> Formerly Bing Ads, reaching users on Bing, Yahoo, and AOL</li>
<li><strong>Social Media Ads:</strong> Facebook, Instagram, LinkedIn, and Twitter offer PPC advertising options</li>
</ul>

<h2>Benefits of PPC Advertising</h2>
<p>PPC offers several advantages for businesses:</p>
<ul>
<li><strong>Immediate Results:</strong> Unlike SEO, PPC can drive traffic from day one</li>
<li><strong>Targeted Reach:</strong> Target specific demographics, locations, and interests</li>
<li><strong>Measurable ROI:</strong> Track every click, conversion, and dollar spent</li>
<li><strong>Budget Control:</strong> Set daily or campaign budgets to control spending</li>
<li><strong>Flexibility:</strong> Start, stop, or adjust campaigns at any time</li>
</ul>

<h2>Getting Started with PPC</h2>
<p>To launch a successful PPC campaign, you need:</p>
<ol>
<li><strong>Clear Goals:</strong> Define what you want to achieve (leads, sales, brand awareness)</li>
<li><strong>Keyword Research:</strong> Identify the terms your target audience searches for</li>
<li><strong>Compelling Ad Copy:</strong> Write ads that grab attention and encourage clicks</li>
<li><strong>Optimized Landing Pages:</strong> Ensure your landing pages convert visitors into customers</li>
<li><strong>Ongoing Management:</strong> Continuously optimize campaigns for better performance</li>
</ol>

<p>At Digital Growth Studios, we specialize in creating and managing PPC campaigns that deliver real results. Our team of certified experts helps businesses maximize their advertising ROI through strategic campaign management and optimization.</p>'''
    },
    'in-house-vs-marketing-agency': {
        'title': 'In-House Marketer vs. Marketing Agency',
        'content': '''<h2>Making the Right Choice for Your Business</h2>
<p>When it comes to digital marketing, businesses face a critical decision: should you hire an in-house marketer or partner with a marketing agency? Both options have their advantages, and the right choice depends on your business size, goals, and resources.</p>

<h2>In-House Marketing: Pros and Cons</h2>
<h3>Advantages:</h3>
<ul>
<li><strong>Dedicated Focus:</strong> An in-house marketer is 100% focused on your business</li>
<li><strong>Brand Knowledge:</strong> Deep understanding of your company culture and products</li>
<li><strong>Quick Communication:</strong> Direct access for immediate questions and changes</li>
<li><strong>Cultural Fit:</strong> Someone who becomes part of your team</li>
</ul>

<h3>Challenges:</h3>
<ul>
<li><strong>Limited Expertise:</strong> One person can't be an expert in all marketing channels</li>
<li><strong>Higher Costs:</strong> Salary, benefits, tools, and training add up quickly</li>
<li><strong>Scalability Issues:</strong> Hard to scale up or down based on needs</li>
<li><strong>Knowledge Gaps:</strong> May lack expertise in specialized areas like technical SEO or advanced PPC</li>
</ul>

<h2>Marketing Agency: Pros and Cons</h2>
<h3>Advantages:</h3>
<ul>
<li><strong>Diverse Expertise:</strong> Access to specialists in SEO, PPC, content, design, and more</li>
<li><strong>Proven Processes:</strong> Established workflows and best practices</li>
<li><strong>Latest Tools:</strong> Access to premium marketing tools and platforms</li>
<li><strong>Scalability:</strong> Easy to adjust services as your business grows</li>
<li><strong>Cost Efficiency:</strong> Often more cost-effective than hiring multiple specialists</li>
</ul>

<h3>Challenges:</h3>
<ul>
<li><strong>Less Control:</strong> Agency manages campaigns, not you directly</li>
<li><strong>Communication:</strong> May require scheduled meetings rather than instant access</li>
<li><strong>Learning Curve:</strong> Agency needs time to understand your business deeply</li>
</ul>

<h2>Which Option Is Right for You?</h2>
<p>Consider an <strong>in-house marketer</strong> if:</p>
<ul>
<li>You have a large marketing budget and need someone full-time</li>
<li>Your marketing needs are relatively simple and consistent</li>
<li>You want maximum control over day-to-day marketing activities</li>
</ul>

<p>Consider a <strong>marketing agency</strong> if:</p>
<ul>
<li>You need expertise across multiple channels (SEO, PPC, social media, etc.)</li>
<li>You want to scale quickly without hiring multiple employees</li>
<li>You prefer predictable monthly costs over variable expenses</li>
<li>You want access to the latest tools and strategies without the learning curve</li>
</ul>

<h2>The Hybrid Approach</h2>
<p>Many successful businesses use a hybrid approach: an in-house marketing coordinator who works with an agency for specialized services. This gives you the best of both worlds—internal brand knowledge combined with external expertise.</p>

<p>At Digital Growth Studios, we work with businesses of all sizes, from startups to enterprise companies. Whether you need full-service marketing support or specialized expertise in specific areas, we can help you achieve your growth goals.</p>'''
    },
    'optimize-content-for-ai-search': {
        'title': '10 Ways Businesses Can Optimize Content for AI Search',
        'content': '''<h2>Preparing Your Content for the AI Search Revolution</h2>
<p>As AI-powered search becomes increasingly prevalent, businesses need to adapt their content strategies. Here are 10 proven ways to optimize your content for AI search engines and AI-generated answers.</p>

<h2>1. Create Comprehensive, Long-Form Content</h2>
<p>AI systems favor content that thoroughly covers a topic. Instead of short, surface-level articles, create in-depth guides that answer questions completely. Aim for 2,000+ words when covering complex topics.</p>

<h2>2. Use Natural Language and Conversational Tone</h2>
<p>Write as if you're having a conversation with your audience. AI systems are trained on natural language, so content that sounds human and conversational performs better than overly formal or keyword-stuffed text.</p>

<h2>3. Structure Content with Clear Headings</h2>
<p>Use descriptive H2 and H3 headings that directly answer questions. AI systems use headings to understand content structure and extract key information. Make your headings question-based when appropriate.</p>

<h2>4. Implement Schema Markup</h2>
<p>Structured data helps AI systems understand your content's context. Use schema markup for articles, FAQs, how-to guides, and other content types to help AI extract and cite your information accurately.</p>

<h2>5. Answer Questions Directly</h2>
<p>AI search often provides direct answers. Structure your content to answer specific questions clearly and concisely. Use FAQ sections, bullet points, and numbered lists to make answers easy to extract.</p>

<h2>6. Focus on E-E-A-T Signals</h2>
<p>Experience, Expertise, Authoritativeness, and Trustworthiness matter more than ever. Showcase author credentials, cite sources, and demonstrate first-hand experience with your topics.</p>

<h2>7. Keep Content Fresh and Updated</h2>
<p>AI systems prioritize current, accurate information. Regularly update your content with the latest data, statistics, and developments in your industry. Add "Last Updated" dates to show freshness.</p>

<h2>8. Optimize for Featured Snippets</h2>
<p>Featured snippets are prime real estate for AI citations. Format content to answer questions in 40-60 words, use tables for comparisons, and create list-based content that's easy to extract.</p>

<h2>9. Build Topic Clusters</h2>
<p>Create comprehensive content clusters around core topics. This helps establish your authority and ensures AI systems have multiple pieces of related content to reference.</p>

<h2>10. Monitor and Adapt</h2>
<p>Track how your content appears in AI-generated answers. Use tools to monitor citations and adjust your strategy based on what's working. Stay informed about AI search developments and adapt accordingly.</p>

<h2>Getting Started</h2>
<p>Optimizing for AI search requires a strategic approach that balances traditional SEO with AI-specific considerations. At Digital Growth Studios, we help businesses create content that performs across all search platforms, ensuring maximum visibility in the age of AI search.</p>'''
    },
    'call-center-marketing-guide': {
        'title': 'Call Center Digital Marketing: Guide to Lead Generation and Conversion Optimization',
        'content': '''<h2>Digital Marketing Strategies for Call Centers</h2>
<p>Call centers face unique challenges in digital marketing. Unlike e-commerce businesses, call centers need to drive phone calls and qualified leads rather than direct online sales. This guide covers proven strategies for call center lead generation and conversion optimization.</p>

<h2>Understanding Call Center Marketing Goals</h2>
<p>Call center marketing differs from traditional e-commerce because the conversion happens offline—over the phone. Your digital marketing strategy must focus on:</p>
<ul>
<li>Driving qualified phone calls</li>
<li>Capturing lead information through forms</li>
<li>Building trust before the call</li>
<li>Optimizing for local search (for location-based call centers)</li>
</ul>

<h2>PPC Strategies for Call Centers</h2>
<h3>Call-Only Campaigns</h3>
<p>Google Ads offers call-only campaigns specifically designed for businesses that want phone calls. These campaigns:</p>
<ul>
<li>Show ads only on mobile devices</li>
<li>Feature a prominent "Call" button</li>
<li>Track calls directly in Google Ads</li>
<li>Allow you to set different bids for calls vs. clicks</li>
</ul>

<h3>Call Extensions</h3>
<p>Add call extensions to all your search and display campaigns. This makes your phone number clickable directly from ads, making it easy for potential customers to call you.</p>

<h3>Call Tracking</h3>
<p>Implement call tracking to measure which campaigns, keywords, and ads drive the most valuable calls. Use unique phone numbers for different campaigns to attribute calls accurately.</p>

<h2>SEO for Call Centers</h2>
<h3>Local SEO</h3>
<p>If your call center serves specific geographic areas, local SEO is crucial:</p>
<ul>
<li>Optimize Google Business Profile</li>
<li>Build local citations</li>
<li>Get reviews from satisfied customers</li>
<li>Create location-specific landing pages</li>
</ul>

<h3>Content Marketing</h3>
<p>Create content that addresses common questions and concerns before customers call. This helps:</p>
<ul>
<li>Qualify leads before they call</li>
<li>Reduce call volume for simple questions</li>
<li>Build trust and authority</li>
<li>Improve search rankings</li>
</ul>

<h2>Landing Page Optimization</h2>
<p>Your landing pages should be designed to encourage phone calls:</p>
<ul>
<li><strong>Prominent Phone Number:</strong> Make your phone number visible and clickable</li>
<li><strong>Clear Value Proposition:</strong> Explain why someone should call you</li>
<li><strong>Trust Signals:</strong> Display testimonials, certifications, and guarantees</li>
<li><strong>Simple Forms:</strong> If you use forms, keep them short and focused</li>
<li><strong>Mobile Optimization:</strong> Most calls come from mobile devices</li>
</ul>

<h2>Conversion Optimization</h2>
<h3>A/B Testing</h3>
<p>Test different elements to improve conversion rates:</p>
<ul>
<li>Headlines and value propositions</li>
<li>Call-to-action buttons and text</li>
<li>Phone number placement and size</li>
<li>Form fields and length</li>
</ul>

<h3>Reduce Friction</h3>
<p>Make it as easy as possible for visitors to contact you:</p>
<ul>
<li>Offer multiple contact methods (phone, form, chat)</li>
<li>Show availability hours</li>
<li>Display estimated wait times</li>
<li>Provide instant callback options</li>
</ul>

<h2>Measuring Success</h2>
<p>Key metrics for call center marketing include:</p>
<ul>
<li><strong>Call Volume:</strong> Total number of calls generated</li>
<li><strong>Call Quality:</strong> Percentage of calls that convert to customers</li>
<li><strong>Cost Per Call:</strong> Marketing spend divided by calls</li>
<li><strong>Call Duration:</strong> Longer calls often indicate higher quality leads</li>
<li><strong>Conversion Rate:</strong> Calls that result in sales or appointments</li>
</ul>

<h2>Best Practices</h2>
<ul>
<li>Answer calls quickly—speed matters for conversion</li>
<li>Train your team on handling marketing-generated calls</li>
<li>Follow up with leads who don't convert immediately</li>
<li>Continuously optimize based on call quality data</li>
<li>Integrate your CRM with marketing platforms for better tracking</li>
</ul>

<p>At Digital Growth Studios, we specialize in call center marketing. Our team helps call centers generate more qualified leads and optimize conversion rates through strategic PPC, SEO, and landing page optimization.</p>'''
    }
}

def fix_header_links(html_content):
    """Fix header navigation links by replacing anchor links with proper page URLs."""
    soup = BeautifulSoup(html_content, 'html.parser')
    modified = False
    
    # Find all navigation links
    nav_links = soup.find_all('a', href=True)
    
    for link in nav_links:
        href = link.get('href', '')
        
        # Fix service anchor links
        if href in SERVICE_LINK_MAP:
            link['href'] = SERVICE_LINK_MAP[href]
            modified = True
        
        # Fix Services main link if it points to anchor
        if href == '#core-services' and 'Services' in link.get_text():
            link['href'] = '/services/'
            modified = True
    
    return str(soup), modified

def add_blog_content(html_content, blog_slug):
    """Add content to blog posts that are missing full article content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    modified = False
    
    # Check if content section exists and has minimal content
    content_section = soup.find('section', id='content') or soup.find('main')
    if not content_section:
        return str(soup), False
    
    # Look for post-content div
    post_content = content_section.find('div', class_='post-content')
    if not post_content:
        return str(soup), False
    
    # Check if content is minimal (just title and short description)
    # Look for h2 tags - if there are h2 tags, content likely already exists
    existing_h2 = post_content.find_all('h2')
    if existing_h2:
        # Check if these are just in templates or actual content
        text_content = post_content.get_text(strip=True)
        if len(text_content) > 1000:  # Already has substantial content
            return str(soup), False
    
    # Get the title
    title_elem = post_content.find('h1')
    if not title_elem:
        return str(soup), False
    
    title_text = title_elem.get_text(strip=True)
    
    # Find the fusion-text div that likely contains the short description
    fusion_text = post_content.find('div', class_='fusion-text')
    
    # Get content template based on slug or title
    content_html = None
    if blog_slug in BLOG_CONTENT_TEMPLATES:
        content_html = BLOG_CONTENT_TEMPLATES[blog_slug]['content']
    else:
        # Generate generic content based on title
        content_html = generate_generic_content(title_text)
    
    if content_html:
        # Find the fusion-column-wrapper that contains the title and text
        fusion_wrapper = post_content.find('div', class_='fusion-column-wrapper')
        if fusion_wrapper:
            # Parse the content HTML
            content_soup = BeautifulSoup(content_html, 'html.parser')
            
            # Create a new div to wrap the content
            content_wrapper = soup.new_tag('div', class_='fusion-text fusion-text-content')
            content_wrapper.append(content_soup)
            
            # Insert content after the fusion-text div, or at the end of fusion-wrapper
            if fusion_text:
                # Find the parent fusion-column-wrapper and insert after it
                parent_wrapper = fusion_text.find_parent('div', class_='fusion-column-wrapper')
                if parent_wrapper:
                    # Find the parent fusion-layout-column
                    parent_column = parent_wrapper.find_parent('div', class_=lambda x: x and 'fusion-layout-column' in x)
                    if parent_column:
                        # Create a new row for the content
                        new_row = soup.new_tag('div', class_='fusion-builder-row fusion-row')
                        new_column = soup.new_tag('div', class_='fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column')
                        new_column_wrapper = soup.new_tag('div', class_='fusion-column-wrapper')
                        new_column_wrapper.append(content_wrapper)
                        new_column.append(new_column_wrapper)
                        new_row.append(new_column)
                        
                        # Insert after the fusion-fullwidth box
                        fullwidth_box = post_content.find('div', class_='fusion-fullwidth')
                        if fullwidth_box:
                            fullwidth_box.insert_after(new_row)
                            modified = True
            else:
                fusion_wrapper.append(content_wrapper)
                modified = True
        elif fusion_text:
            # Parse the content HTML
            content_soup = BeautifulSoup(content_html, 'html.parser')
            # Create a wrapper div
            content_wrapper = soup.new_tag('div', class_='fusion-text fusion-text-content')
            content_wrapper.append(content_soup)
            # Insert content after the fusion-text div's parent
            fusion_text_parent = fusion_text.find_parent('div', class_='fusion-column-wrapper')
            if fusion_text_parent:
                fusion_text_parent.insert_after(content_wrapper)
                modified = True
    
    return str(soup), modified

def generate_generic_content(title):
    """Generate generic content structure for blog posts without specific templates."""
    # Extract key topics from title
    title_lower = title.lower()
    
    content = f'''<h2>Introduction</h2>
<p>This comprehensive guide explores {title.lower()}, providing valuable insights and actionable strategies for businesses looking to improve their digital marketing performance.</p>

<h2>Key Concepts</h2>
<p>Understanding the fundamentals is crucial for success. Let's explore the core concepts and best practices that drive results.</p>

<h2>Best Practices</h2>
<p>Implementing proven strategies can significantly impact your outcomes. Here are the most effective approaches:</p>
<ul>
<li>Develop a clear strategy aligned with your business goals</li>
<li>Measure and track performance metrics</li>
<li>Continuously optimize based on data insights</li>
<li>Stay updated with industry trends and changes</li>
</ul>

<h2>Implementation Strategies</h2>
<p>Putting theory into practice requires careful planning and execution. Consider these implementation steps:</p>
<ol>
<li>Assess your current situation and identify opportunities</li>
<li>Set clear, measurable objectives</li>
<li>Develop a detailed action plan</li>
<li>Execute and monitor progress</li>
<li>Adjust strategies based on results</li>
</ol>

<h2>Common Challenges and Solutions</h2>
<p>Every business faces unique challenges. Here are some common issues and how to address them:</p>
<ul>
<li><strong>Resource Constraints:</strong> Prioritize high-impact activities and consider outsourcing specialized tasks</li>
<li><strong>Measuring ROI:</strong> Implement proper tracking and attribution models</li>
<li><strong>Staying Competitive:</strong> Focus on differentiation and unique value propositions</li>
</ul>

<h2>Conclusion</h2>
<p>Success requires a strategic approach, consistent effort, and continuous optimization. By following best practices and staying focused on your goals, you can achieve significant improvements in your digital marketing performance.</p>

<p>At Digital Growth Studios, we help businesses navigate these challenges and achieve their growth objectives. Our team of experts provides strategic guidance and hands-on support to drive measurable results.</p>'''
    
    return content

def process_html_file(file_path):
    """Process a single HTML file to fix links and add content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        original_content = html_content
        modified = False
        
        # Fix header links
        html_content, links_modified = fix_header_links(html_content)
        if links_modified:
            modified = True
        
        # Add blog content if it's a blog post
        if '/blog/' in str(file_path):
            blog_slug = Path(file_path).parent.name
            html_content, content_modified = add_blog_content(html_content, blog_slug)
            if content_modified:
                modified = True
        
        # Write back if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all HTML files."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Directory {base_dir} not found!")
        return
    
    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    fixed_count = 0
    for html_file in html_files:
        if process_html_file(html_file):
            fixed_count += 1
            print(f"Fixed: {html_file}")
    
    print(f"\nCompleted! Fixed {fixed_count} out of {len(html_files)} files.")

if __name__ == '__main__':
    main()

