#!/usr/bin/env python3
"""
Comprehensive fix for all broken HTML pages.
Adds missing main content wrapper and fixes HTML structure.
"""

import os
import re
from pathlib import Path

def extract_page_info(content):
    """Extract page title and description from HTML"""
    title_match = re.search(r'<title>(.*?)</title>', content)
    page_title = title_match.group(1) if title_match else 'Page'
    # Clean up title
    page_title = page_title.replace(' - Digital Growth Studios', '').replace('Digital Growth Studios - ', '').strip()
    
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', content)
    page_desc = desc_match.group(1) if desc_match else ''
    # Unescape HTML entities
    page_desc = page_desc.replace('&amp;', '&').replace('&#039;', "'")
    
    return page_title, page_desc

def fix_broken_page(file_path):
    """Fix a single broken HTML page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has main wrapper
        if '<main id="main"' in content:
            return False
        
        # Check if page has broken structure
        if '<div class="fusion-tb-header">' in content:
            # Find header div
            header_pattern = r'(<div class="fusion-tb-header">\s*)'
            header_match = re.search(header_pattern, content)
            
            if header_match:
                header_end = header_match.end()
                after_header = content[header_end:].strip()
                
                # Check if it has broken tags or missing main content
                if '</ul></li>' in after_header[:500] or '<ul class="fusion-menu">' in after_header[:500] or not '<main id="main"' in content:
                    # Find where footer/sidebar starts (look for Services section or footer)
                    footer_patterns = [
                        r'(<div class="fusion-layout-column.*fusion_builder_column-43.*Services)',
                        r'(<div class="fusion-fullwidth.*fusion-builder-row-19.*COPYRIGHT)',
                        r'(<div class="fusion-text.*COPYRIGHT)'
                    ]
                    
                    footer_match = None
                    for pattern in footer_patterns:
                        footer_match = re.search(pattern, content)
                        if footer_match:
                            break
                    
                    if footer_match:
                        insert_pos = footer_match.start()
                        
                        # Extract page info
                        page_title, page_desc = extract_page_info(content)
                        
                        # Create main content section
                        main_content = f'''</div>
		<div id="sliders-container" class="fusion-slider-visibility">
		</div>

		<main id="main" class="clearfix width-100">
			<div class="fusion-row" style="max-width:100%;">
				<section id="content" class="full-width">
					<div class="post-content">
						<div class="fusion-fullwidth fullwidth-box">
							<div class="fusion-builder-row fusion-row">
								<div class="fusion-layout-column fusion_builder_column fusion_builder_column_1_1 1_1 fusion-flex-column">
									<div class="fusion-column-wrapper">
										<div class="fusion-title title">
											<h1 class="title-heading-left">{page_title}</h1>
										</div>
										<div class="fusion-text">
											<p>{page_desc}</p>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>
			</div>
		</main>

		<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19 fusion-flex-container has-pattern-background has-mask-background nonhundred-percent-fullwidth non-hundred-percent-height-scrolling" style="--awb-border-radius-top-left:0px;--awb-border-radius-top-right:0px;--awb-border-radius-bottom-right:0px;--awb-border-radius-bottom-left:0px;--awb-padding-top:40px;--awb-padding-bottom:40px;--awb-background-color:var(--awb-color5);" ><div class="fusion-builder-row fusion-row fusion-flex-align-items-flex-start" style="max-width:1248px;margin-left: calc(-4% / 2 );margin-right: calc(-4% / 2 );"><div class="fusion-layout-column fusion_builder_column fusion-builder-column-43 fusion_builder_column_1_5 1_5 fusion-flex-column" style="--awb-bg-size:cover;--awb-width-large:20%;--awb-margin-top-large:20px;--awb-spacing-right-large:9.6%;--awb-margin-bottom-large:20px;--awb-spacing-left-large:9.6%;--awb-width-medium:20%;--awb-order-medium:0;--awb-spacing-right-medium:9.6%;--awb-spacing-left-medium:9.6%;--awb-width-small:100%;--awb-order-small:0;--awb-spacing-right-small:1.92%;--awb-spacing-left-small:1.92%;"><div class="fusion-column-wrapper fusion-column-has-shadow fusion-flex-justify-content-flex-start fusion-content-layout-column"><div class="fusion-title title fusion-title-38 fusion-sep-none fusion-title-text fusion-title-size-four" style="--awb-text-color:var(--awb-color1);"><h4 class="title-heading-left fusion-responsive-typography-calculated" style="margin:0;text-transform:uppercase;--fontSize:20;--minFontSize:20;line-height:var(--awb-typography4-line-height);">Services</h4></div><ul style="--awb-textcolor:var(--awb-color1);--awb-line-height:27.2px;--awb-icon-width:27.2px;--awb-icon-height:27.2px;--awb-icon-margin:11.2px;--awb-content-margin:38.4px;" class="fusion-checklist fusion-checklist-2 fusion-checklist-default type-icons"><li class="fusion-li-item" style=""><span class="icon-wrapper circle-no"><i class="fusion-li-icon fa-angle-right fas" aria-hidden="true"></i></span><div class="fusion-li-item-content">
<p><span style="color: #ffffff;"><a style="color: #ffffff;" href="/company/">Agency</a></span></p>
</div></li>'''
                        
                        # Remove broken header content
                        broken_content = content[header_end:insert_pos]
                        
                        # Clean up broken tags in the content
                        new_content = content[:header_end] + main_content + content[insert_pos:]
                        
                        # Clean up any remaining broken HTML
                        new_content = re.sub(r'<ul class="fusion-menu">\s*<li class="menu-item"></ul></li>', '', new_content)
                        new_content = re.sub(r'</ul></li><li class="fusion-li-item"', '<li class="fusion-li-item"', new_content)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Find and fix all broken HTML pages"""
    base_dir = Path('blackpropeller.com')
    html_files = list(base_dir.rglob('index.html'))
    
    fixed_count = 0
    for html_file in html_files:
        if fix_broken_page(html_file):
            print(f"Fixed: {html_file}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()


