#!/usr/bin/env python3
"""
Fix broken HTML pages - add missing opening tags and main content wrapper.
Pages start with </ul></li> which means opening <ul><li> tags are missing.
"""

import os
import re
from pathlib import Path

def fix_broken_page(file_path):
    """Fix a single broken HTML page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page is broken (starts with </ul></li> after wrapper)
        if '</ul></li>' in content:
            # Find where the broken content starts (after wrapper/header)
            # Look for pattern: wrapper/header followed by </ul></li>
            pattern = r'(<div class="fusion-tb-header">\s*)(</ul></li>)'
            match = re.search(pattern, content)
            
            if match:
                # Insert opening <ul> before the closing tags
                insert_pos = match.end(1)
                opening_tags = '<ul class="fusion-menu">\n<li class="menu-item">'
                
                new_content = content[:insert_pos] + opening_tags + content[insert_pos:]
                
                # Also need to add main content wrapper if missing
                if '<main id="main"' not in new_content:
                    # Find where main content should start (after footer/sidebar content)
                    # Look for closing wrapper tags before </body>
                    body_close_match = re.search(r'</body>', new_content)
                    if body_close_match:
                        # Insert main wrapper before closing wrapper
                        # Find the last </div> before </body> that closes wrapper
                        before_body = new_content[:body_close_match.start()]
                        
                        # Check if we need to add main wrapper
                        if '<main id="main"' not in before_body:
                            # Find where to insert - before the closing wrapper divs
                            # Look for pattern: </div></div></div> <!-- wrapper -->
                            wrapper_close_pattern = r'(</div>\s*</div>\s*</div>\s*<!-- wrapper -->)'
                            wrapper_match = re.search(wrapper_close_pattern, before_body)
                            
                            if wrapper_match:
                                # Insert main wrapper before closing wrapper
                                main_wrapper = '''\t\t</div> <!-- wrapper -->
	</div> <!-- #boxed-wrapper -->
	<a class="skip-link screen-reader-text" href="#content">Skip to content</a>

	<div id="boxed-wrapper">
		<div id="wrapper" class="fusion-wrapper">
			<div id="home" style="position:relative;top:-1px;"></div>
			<main id="main" class="clearfix width-100">
				<div class="fusion-row" style="max-width:100%;">
					<section id="content" class="full-width">
						<div class="post-content">'''
                                
                                insert_pos = wrapper_match.start()
                                new_content = before_body[:insert_pos] + main_wrapper + before_body[insert_pos:] + new_content[body_close_match.start():]
                                
                                # Also need to close main wrapper before </body>
                                body_close_pos = new_content.rfind('</body>')
                                if body_close_pos > 0:
                                    main_close = '''						</div> <!-- post-content -->
					</section> <!-- content -->
				</div> <!-- fusion-row -->
			</main> <!-- main -->'''
                                    new_content = new_content[:body_close_pos] + main_close + '\n' + new_content[body_close_pos:]
                
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
    html_files = list(base_dir.rglob('*.html'))
    
    fixed_count = 0
    for html_file in html_files:
        if fix_broken_page(html_file):
            print(f"Fixed: {html_file}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()



