#!/usr/bin/env python3
"""
Apply standardized content structure to all pages based on the provided template.
This script updates pages with the specified content structure.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html

def add_faq_to_seo_page(soup):
    """Add FAQ section to SEO services page if it doesn't exist."""
    # Check if FAQ already exists
    if soup.find(string=re.compile('Frequently Asked Questions', re.I)):
        return False
    
    # Find the last fusion-fullwidth box before footer
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Find the last row before footer
    all_rows = post_content.find_all('div', class_='fusion-fullwidth')
    if not all_rows:
        return False
    
    # Get the last row to insert after
    last_row = all_rows[-1]
    
    # Create FAQ section
    faq_html = '''
    <div class="fusion-fullwidth fullwidth-box fusion-builder-row-faq" style="--awb-padding-top:100px;--awb-padding-bottom:100px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row fusion-flex-align-items-stretch" style="max-width:1248px;margin-left: calc(-4% / 2 );margin-right: calc(-4% / 2 );">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column" style="--awb-width-large:100%;--awb-margin-top-large:20px;--awb-spacing-right-large:1.92%;--awb-margin-bottom-large:20px;--awb-spacing-left-large:1.92%;">
                <div class="fusion-column-wrapper">
                    <div class="fusion-title title fusion-sep-none fusion-title-center fusion-title-text fusion-title-size-two">
                        <h2 class="title-heading-center" style="margin:0;">Frequently Asked Questions</h2>
                    </div>
                    <div class="accordian fusion-accordian" style="--awb-border-size:1px;--awb-icon-size:40px;--awb-icon-alignment:right;--awb-hover-color:var(--awb-color2);--awb-border-color:var(--awb-color2);--awb-background-color:var(--awb-color7);--awb-divider-color:var(--awb-color2);--awb-icon-color:var(--awb-color6);--awb-title-color:var(--awb-color4);--awb-content-color:var(--awb-color4);">
                        <div class="panel-group fusion-toggle-icon-right fusion-toggle-icon-unboxed" id="accordion-faq">
                            <div class="fusion-panel panel-default fusion-toggle-has-divider">
                                <div class="panel-heading">
                                    <h3 class="panel-title toggle">
                                        <a aria-controls="faq1" aria-expanded="false" data-parent="#accordion-faq" data-target="#faq1" data-toggle="collapse" href="#faq1" role="button">
                                            <span aria-hidden="true" class="fusion-toggle-icon-wrapper">
                                                <i aria-hidden="true" class="fa-fusion-box active-icon awb-icon-minus"></i>
                                                <i aria-hidden="true" class="fa-fusion-box inactive-icon awb-icon-plus"></i>
                                            </span>
                                            <span class="fusion-toggle-heading">How long does it take to see SEO results?</span>
                                        </a>
                                    </h3>
                                </div>
                                <div aria-labelledby="toggle_faq1" class="panel-collapse collapse" id="faq1">
                                    <div class="panel-body toggle-content">
                                        <p>Typically, you'll see initial improvements in 3-6 months, with significant results in 6-12 months depending on your industry and competition. Technical SEO improvements may show results faster, while content and link building take longer to mature.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="fusion-panel panel-default fusion-toggle-has-divider">
                                <div class="panel-heading">
                                    <h3 class="panel-title toggle">
                                        <a aria-controls="faq2" aria-expanded="false" data-parent="#accordion-faq" data-target="#faq2" data-toggle="collapse" href="#faq2" role="button">
                                            <span aria-hidden="true" class="fusion-toggle-icon-wrapper">
                                                <i aria-hidden="true" class="fa-fusion-box active-icon awb-icon-minus"></i>
                                                <i aria-hidden="true" class="fa-fusion-box inactive-icon awb-icon-plus"></i>
                                            </span>
                                            <span class="fusion-toggle-heading">What is included in your SEO services?</span>
                                        </a>
                                    </h3>
                                </div>
                                <div aria-labelledby="toggle_faq2" class="panel-collapse collapse" id="faq2">
                                    <div class="panel-body toggle-content">
                                        <p>Our SEO services include technical SEO audits, on-page optimization, content creation, link building, keyword research, monthly reporting, and ongoing optimization. We also provide AI search optimization to ensure your content appears in AI-generated results.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="fusion-panel panel-default fusion-toggle-has-divider">
                                <div class="panel-heading">
                                    <h3 class="panel-title toggle">
                                        <a aria-controls="faq3" aria-expanded="false" data-parent="#accordion-faq" data-target="#faq3" data-toggle="collapse" href="#faq3" role="button">
                                            <span aria-hidden="true" class="fusion-toggle-icon-wrapper">
                                                <i aria-hidden="true" class="fa-fusion-box active-icon awb-icon-minus"></i>
                                                <i aria-hidden="true" class="fa-fusion-box inactive-icon awb-icon-plus"></i>
                                            </span>
                                            <span class="fusion-toggle-heading">Do you work with businesses in my industry?</span>
                                        </a>
                                    </h3>
                                </div>
                                <div aria-labelledby="toggle_faq3" class="panel-collapse collapse" id="faq3">
                                    <div class="panel-body toggle-content">
                                        <p>Yes, we work with businesses across various industries including e-commerce, healthcare, professional services, SaaS, local businesses, and more. Our SEO strategies are tailored to each industry's unique needs and competitive landscape.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="fusion-panel panel-default fusion-toggle-has-divider">
                                <div class="panel-heading">
                                    <h3 class="panel-title toggle">
                                        <a aria-controls="faq4" aria-expanded="false" data-parent="#accordion-faq" data-target="#faq4" data-toggle="collapse" href="#faq4" role="button">
                                            <span aria-hidden="true" class="fusion-toggle-icon-wrapper">
                                                <i aria-hidden="true" class="fa-fusion-box active-icon awb-icon-minus"></i>
                                                <i aria-hidden="true" class="fa-fusion-box inactive-icon awb-icon-plus"></i>
                                            </span>
                                            <span class="fusion-toggle-heading">How do you measure SEO success?</span>
                                        </a>
                                    </h3>
                                </div>
                                <div aria-labelledby="toggle_faq4" class="panel-collapse collapse" id="faq4">
                                    <div class="panel-body toggle-content">
                                        <p>We measure success through multiple metrics including organic traffic growth, keyword rankings, conversion rate improvements, lead generation, and revenue attribution. We provide monthly reports that track these key performance indicators.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    faq_soup = BeautifulSoup(faq_html, 'html.parser')
    last_row.insert_after(faq_soup)
    return True

def add_content_to_paid_search_page(soup):
    """Add full content structure to paid search/PPC page."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Check if content already exists (more than just title and one paragraph)
    existing_text = post_content.get_text(strip=True)
    if len(existing_text) > 1000:
        print("  - Content already exists, skipping")
        return False
    
    # Find the existing fusion-fullwidth box
    existing_box = post_content.find('div', class_='fusion-fullwidth')
    if not existing_box:
        return False
    
    # Create new content sections
    content_html = '''
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Marketing Channels</h2>
                        <p>We manage PPC campaigns, social media advertising, email marketing, conversion rate optimization (CRO), and comprehensive analytics to drive results across the entire customer journey. Our full-funnel approach ensures every touchpoint is optimized for maximum ROI.</p>
                        <ul style="margin-top:20px;">
                            <li><strong>PPC (Pay-Per-Click):</strong> Google Ads, Microsoft Advertising, and other search platforms</li>
                            <li><strong>Social Media Advertising:</strong> Facebook, Instagram, LinkedIn, and other social platforms</li>
                            <li><strong>Email Marketing:</strong> Automated campaigns and newsletters to nurture leads</li>
                            <li><strong>Conversion Rate Optimization:</strong> A/B testing and landing page optimization</li>
                            <li><strong>Analytics & Reporting:</strong> Comprehensive tracking and performance analysis</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color5);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Example Campaigns & Results</h2>
                        <p>Our campaigns have delivered significant ROI improvements, increased lead generation, and improved conversion rates for clients across various industries. We manage over $5,000,000 in annual ad spend and consistently deliver results that exceed client expectations.</p>
                        <p style="margin-top:20px;">Whether you're looking to increase online sales, generate qualified leads, or improve brand awareness, our data-driven approach ensures your advertising budget is invested where it will deliver the best returns.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Reporting & Communication</h2>
                        <p>We provide regular reporting and maintain open communication with weekly updates, monthly reports, and quarterly strategy reviews to keep you informed of your campaign performance. Our transparent approach ensures you always know how your advertising investment is performing.</p>
                        <ul style="margin-top:20px;">
                            <li><strong>Weekly Updates:</strong> Performance summaries and optimization recommendations</li>
                            <li><strong>Monthly Reports:</strong> Comprehensive analysis with key metrics and insights</li>
                            <li><strong>Quarterly Reviews:</strong> Strategic planning sessions to align campaigns with business goals</li>
                            <li><strong>Real-Time Access:</strong> Dashboard access to view performance anytime</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    content_soup = BeautifulSoup(content_html, 'html.parser')
    existing_box.insert_after(content_soup)
    return True

def add_content_to_web_design_page(soup):
    """Add full content structure to web design/development page."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Check if content already exists
    existing_text = post_content.get_text(strip=True)
    if len(existing_text) > 1000:
        print("  - Content already exists, skipping")
        return False
    
    # Find the existing fusion-fullwidth box
    existing_box = post_content.find('div', class_='fusion-fullwidth')
    if not existing_box:
        return False
    
    # Update H1 if needed
    h1 = existing_box.find('h1')
    if h1:
        h1.string = 'Conversion-Focused Web Design & Development'
    
    # Create new content sections
    content_html = '''
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Types of Sites We Build</h2>
                        <p>We create brochure websites, e-commerce stores, landing pages, SaaS platforms, and custom web applications tailored to your business needs. Every site we build is designed with conversion optimization in mind.</p>
                        <ul style="margin-top:20px;">
                            <li><strong>Brochure Websites:</strong> Professional business websites that showcase your services</li>
                            <li><strong>E-commerce Stores:</strong> Online stores optimized for sales and customer experience</li>
                            <li><strong>Landing Pages:</strong> High-converting pages designed for specific campaigns</li>
                            <li><strong>SaaS Platforms:</strong> Custom web applications for software businesses</li>
                            <li><strong>Custom Applications:</strong> Tailored solutions for unique business requirements</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color5);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Our Tech Stack</h2>
                        <p>We work with WordPress, Webflow, custom development, and modern frameworks to build fast, responsive, and conversion-optimized websites. We choose the right technology for each project based on your specific needs and goals.</p>
                        <ul style="margin-top:20px;">
                            <li><strong>WordPress:</strong> Flexible CMS for content-rich websites</li>
                            <li><strong>Webflow:</strong> Modern no-code platform for custom designs</li>
                            <li><strong>Custom Development:</strong> Tailored solutions using modern frameworks</li>
                            <li><strong>E-commerce Platforms:</strong> Shopify, WooCommerce, and custom solutions</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Our Process</h2>
                        <p>From wireframes to design to development to launch, we follow a proven process that ensures your website meets your business goals. Our collaborative approach keeps you involved at every step.</p>
                        <ol style="margin-top:20px;">
                            <li><strong>Discovery & Planning:</strong> Understanding your goals, audience, and requirements</li>
                            <li><strong>Wireframes:</strong> Creating the structure and layout of your site</li>
                            <li><strong>Design:</strong> Developing the visual design that reflects your brand</li>
                            <li><strong>Development:</strong> Building your site with clean, optimized code</li>
                            <li><strong>Testing & Launch:</strong> Quality assurance and smooth launch process</li>
                            <li><strong>Ongoing Support:</strong> Maintenance and updates to keep your site running smoothly</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color5);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Portfolio</h2>
                        <p>View our portfolio of successful web design and development projects that have driven real results for our clients. Each project showcases our ability to create websites that not only look great but also convert visitors into customers.</p>
                        <p style="margin-top:20px;"><a href="/results/" class="fusion-button button-flat">View Case Studies</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    content_soup = BeautifulSoup(content_html, 'html.parser')
    existing_box.insert_after(content_soup)
    return True

def add_expectations_to_contact_page(soup):
    """Add 'What to expect next' section to contact page."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Check if expectations section already exists
    if soup.find(string=re.compile('What to expect|Next steps', re.I)):
        return False
    
    # Find the form section (fusion-builder-row-3 contains the form)
    form_row = post_content.find('div', class_='fusion-builder-row-3')
    if not form_row:
        # Try to find the last fusion-fullwidth before footer
        all_rows = post_content.find_all('div', class_='fusion-fullwidth')
        if not all_rows:
            return False
        form_row = all_rows[-1]
    
    # Create expectations section
    expectations_html = '''
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>What to Expect Next</h2>
                        <p><strong>Response Time:</strong> We typically respond within 24 hours to all inquiries.</p>
                        <p style="margin-top:20px;"><strong>Next Steps:</strong> After you submit the form, we'll schedule a free strategy call to discuss your goals, understand your business needs, and determine how our SEO, Google Ads, Web Design, and Analytics & Strategy services can help you achieve your objectives. No pressure—just a real conversation about whether it makes sense to work together.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    expectations_soup = BeautifulSoup(expectations_html, 'html.parser')
    form_row.insert_after(expectations_soup)
    return True

def add_content_to_about_page(soup):
    """Add full content structure to about page."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Check if content already exists
    existing_text = post_content.get_text(strip=True)
    if len(existing_text) > 1000:
        print("  - Content already exists, skipping")
        return False
    
    # Find the existing fusion-fullwidth box
    existing_box = post_content.find('div', class_='fusion-fullwidth')
    if not existing_box:
        return False
    
    # Update H1 if needed
    h1 = existing_box.find('h1')
    if h1:
        h1.string = 'About Digital Growth Studios'
    
    # Create new content sections
    content_html = '''
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Our Story</h2>
                        <p>Since 2011, Digital Growth Studios has grown to manage more than $5,000,000 in advertising annually for our clients. We're dedicated to delivering ROI-driven results through expert SEO, web development, and digital marketing services.</p>
                        <p style="margin-top:20px;">What started as a small team focused on helping local businesses grow has evolved into a full-service digital marketing agency serving clients across various industries. Our commitment to results and client success has remained constant throughout our growth.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color5);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Our Mission</h2>
                        <p>To help businesses achieve their growth goals through strategic digital marketing that drives qualified traffic, increases conversions, and delivers measurable ROI. We believe in transparent reporting, data-driven decisions, and building long-term partnerships with our clients.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Team Highlights</h2>
                        <p>Our team consists of experienced SEO specialists, web developers, PPC experts, and digital marketing strategists who are passionate about delivering results for our clients. Each team member brings unique expertise and a commitment to staying current with industry best practices.</p>
                        <p style="margin-top:20px;"><a href="/team/" class="fusion-button button-flat">Meet The Team</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color5);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>Certifications & Partnerships</h2>
                        <p>We maintain partnerships with leading platforms and stay current with industry best practices to ensure we deliver cutting-edge solutions for our clients. Our team regularly participates in training and certification programs to stay ahead of digital marketing trends.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    content_soup = BeautifulSoup(content_html, 'html.parser')
    existing_box.insert_after(content_soup)
    return True

def update_page(file_path, page_type):
    """Update a page with the appropriate content structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        updated = False
        
        if page_type == 'seo_services':
            updated = add_faq_to_seo_page(soup)
        elif page_type == 'paid_search':
            updated = add_content_to_paid_search_page(soup)
        elif page_type == 'web_design':
            updated = add_content_to_web_design_page(soup)
        elif page_type == 'about':
            updated = add_content_to_about_page(soup)
        elif page_type == 'contact':
            updated = add_expectations_to_contact_page(soup)
        else:
            print(f"  ⚠ Unknown page type: {page_type}")
            return False
        
        if updated:
            # Save the updated HTML
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  ✓ Updated {file_path.name}")
            return True
        else:
            print(f"  - No changes made to {file_path.name}")
            return False
        
    except Exception as e:
        print(f"  ✗ Error updating {file_path}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to update all pages."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    # Define pages to update
def add_expectations_to_contact_page(soup):
    """Add 'What to expect next' section to contact page."""
    post_content = soup.find('div', class_='post-content')
    if not post_content:
        return False
    
    # Check if expectations section already exists
    if soup.find(string=re.compile('What to expect|Next steps', re.I)):
        return False
    
    # Find the form section
    form_section = post_content.find('div', class_='fusion-fullwidth', string=re.compile('Send Us A Message', re.I))
    if not form_section:
        # Try to find the last fusion-fullwidth before footer
        all_rows = post_content.find_all('div', class_='fusion-fullwidth')
        if not all_rows:
            return False
        form_section = all_rows[-1]
    
    # Create expectations section
    expectations_html = '''
    <div class="fusion-fullwidth fullwidth-box" style="--awb-padding-top:80px;--awb-padding-bottom:80px;--awb-background-color:var(--awb-color7);">
        <div class="fusion-builder-row fusion-row">
            <div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
                <div class="fusion-column-wrapper">
                    <div class="fusion-text" style="margin-top:40px;">
                        <h2>What to Expect Next</h2>
                        <p><strong>Response Time:</strong> We typically respond within 24 hours to all inquiries.</p>
                        <p style="margin-top:20px;"><strong>Next Steps:</strong> After you submit the form, we'll schedule a free strategy call to discuss your goals, understand your business needs, and determine how our SEO, Google Ads, Web Design, and Analytics & Strategy services can help you achieve your objectives. No pressure—just a real conversation about whether it makes sense to work together.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    expectations_soup = BeautifulSoup(expectations_html, 'html.parser')
    form_section.insert_after(expectations_soup)
    return True

def update_page(file_path, page_type):
    """Update a page with the appropriate content structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        updated = False
        
        if page_type == 'seo_services':
            updated = add_faq_to_seo_page(soup)
        elif page_type == 'paid_search':
            updated = add_content_to_paid_search_page(soup)
        elif page_type == 'web_design':
            updated = add_content_to_web_design_page(soup)
        elif page_type == 'about':
            updated = add_content_to_about_page(soup)
        elif page_type == 'contact':
            updated = add_expectations_to_contact_page(soup)
        else:
            print(f"  ⚠ Unknown page type: {page_type}")
            return False
        
        if updated:
            # Save the updated HTML
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  ✓ Updated {file_path.name}")
            return True
        else:
            print(f"  - No changes made to {file_path.name}")
            return False
        
    except Exception as e:
        print(f"  ✗ Error updating {file_path}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to update all pages."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"Error: {base_dir} not found!")
        return
    
    # Define pages to update
    pages_to_update = [
        {
            'path': base_dir / 'services' / 'seo' / 'index.html',
            'type': 'seo_services',
            'name': 'SEO Services Page (FAQ)'
        },
        {
            'path': base_dir / 'services' / 'paid-search' / 'index.html',
            'type': 'paid_search',
            'name': 'Digital Marketing/PPC Page'
        },
        {
            'path': base_dir / 'services' / 'creative' / 'index.html',
            'type': 'web_design',
            'name': 'Web Design/Development Page'
        },
        {
            'path': base_dir / 'company' / 'index.html',
            'type': 'about',
            'name': 'About Page'
        },
        {
            'path': base_dir / 'contact' / 'index.html',
            'type': 'contact',
            'name': 'Contact Page (Expectations)'
        },
    ]
    
    print(f"{'='*70}")
    print(f"Content Structure Application Script")
    print(f"{'='*70}")
    print(f"Found {len(pages_to_update)} pages to update\n")
    
    updated = 0
    skipped = 0
    errors = 0
    
    for i, page_info in enumerate(pages_to_update, 1):
        page_path = page_info['path']
        page_type = page_info['type']
        page_name = page_info['name']
        
        if not page_path.exists():
            print(f"[{i}/{len(pages_to_update)}] {page_name}")
            print(f"  ✗ File not found: {page_path}")
            errors += 1
            continue
        
        print(f"[{i}/{len(pages_to_update)}] {page_name}")
        if update_page(page_path, page_type):
            updated += 1
        else:
            skipped += 1
    
    print(f"\n{'='*70}")
    print(f"Update Complete!")
    print(f"  Updated: {updated} pages")
    print(f"  Skipped: {skipped} pages")
    print(f"  Errors: {errors} pages")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
