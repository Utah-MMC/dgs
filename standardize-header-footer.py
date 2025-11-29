#!/usr/bin/env python3
"""
Standardize header and footer across all pages to match homepage exactly.
"""

import re
from pathlib import Path

def extract_header_footer():
    """Extract header and footer from index.html"""
    index_path = Path('blackpropeller.com/index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract header - everything between <div class="fusion-tb-header"> and </div> before sliders
    header_match = re.search(
        r'<div class="fusion-tb-header">(.*?)</div>\s*<div id="sliders-container"',
        content,
        re.DOTALL
    )
    header_content = header_match.group(1).strip() if header_match else None
    
    # Extract footer - find the footer section (fusion-builder-row-19 with footer content)
    # Look for the footer section that contains Company, Services, and Copyright
    footer_match = re.search(
        r'(<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19[^>]*>.*?COPYRIGHT.*?DIGITAL GROWTH STUDIOS.*?</div></div></div>)',
        content,
        re.DOTALL
    )
    footer_content = footer_match.group(1).strip() if footer_match else None
    
    return header_content, footer_content

def standardize_page(file_path, header_content, footer_content):
    """Standardize a single page's header and footer"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Replace header
        if header_content:
            # Find existing header
            header_pattern = r'<div class="fusion-tb-header">.*?</div>\s*<div id="sliders-container"'
            if re.search(header_pattern, content, re.DOTALL):
                new_header = f'<div class="fusion-tb-header">{header_content}</div>'
                content = re.sub(header_pattern, new_header + '\n\t\t<div id="sliders-container"', content, flags=re.DOTALL)
                modified = True
        
        # Replace footer - find the footer section and replace it
        if footer_content:
            # Look for existing footer patterns
            footer_patterns = [
                r'<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19[^>]*>.*?COPYRIGHT.*?DIGITAL GROWTH STUDIOS.*?</div></div></div>',
                r'<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19[^>]*>.*?</div></div></div>\s*</div></div>',
            ]
            
            for pattern in footer_patterns:
                if re.search(pattern, content, re.DOTALL):
                    # Find where main content ends (before footer)
                    main_end = content.rfind('</main>')
                    if main_end > 0:
                        # Find the start of the footer section
                        footer_start_match = re.search(r'<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19', content[main_end:], re.DOTALL)
                        if footer_start_match:
                            footer_start_pos = main_end + footer_start_match.start()
                            # Find the end of the footer (look for closing divs after copyright)
                            footer_end_match = re.search(r'COPYRIGHT.*?DIGITAL GROWTH STUDIOS.*?</div></div></div>', content[footer_start_pos:], re.DOTALL)
                            if footer_end_match:
                                footer_end_pos = footer_start_pos + footer_end_match.end()
                                # Replace the footer
                                content = content[:footer_start_pos] + footer_content + content[footer_end_pos:]
                                modified = True
                                break
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error with {file_path}: {e}")
        return False

def main():
    """Standardize all pages"""
    header_content, footer_content = extract_header_footer()
    
    if not header_content:
        print("ERROR: Could not extract header from index.html")
        return
    
    if not footer_content:
        print("ERROR: Could not extract footer from index.html")
        return
    
    print(f"Header length: {len(header_content)}")
    print(f"Footer length: {len(footer_content)}")
    
    base_dir = Path('blackpropeller.com')
    html_files = [f for f in base_dir.rglob('*.html') 
                  if f.name != 'index.html' or 'index.html' not in str(f.parent)]
    
    fixed = 0
    for html_file in html_files:
        if standardize_page(html_file, header_content, footer_content):
            print(f"Standardized: {html_file}")
            fixed += 1
    
    print(f"\nStandardized {fixed} files")

if __name__ == '__main__':
    main()


