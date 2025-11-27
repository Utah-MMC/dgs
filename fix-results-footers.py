#!/usr/bin/env python3
"""
Fix footer on results pages to match homepage footer structure
"""

import re
from pathlib import Path

def get_homepage_footer():
    """Get the footer HTML from index.html"""
    index_path = Path('blackpropeller.com/index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract footer - the fusion-builder-row-19 section with footer content
    footer_match = re.search(
        r'(<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19[^>]*>.*?COPYRIGHT.*?DIGITAL GROWTH STUDIOS.*?</div></div></div>)',
        content,
        re.DOTALL
    )
    return footer_match.group(1).strip() if footer_match else None

def fix_results_footer(file_path, footer_content):
    """Fix footer on a results page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Check if it has bp-footer or results-footer (different footer structure)
        if '<div class="bp-footer">' in content or '<footer class="results-footer">' in content:
            # Find the wrapper closing tag
            wrapper_end = content.rfind('</div> <!-- wrapper -->')
            if wrapper_end < 0:
                wrapper_end = content.rfind('</div> <!-- #boxed-wrapper -->')
            
            if wrapper_end > 0:
                # Find the footer (bp-footer or results-footer)
                bp_footer_match = re.search(r'<div class="bp-footer">.*?</div>', content, re.DOTALL)
                results_footer_match = re.search(r'<footer class="results-footer">.*?</footer>', content, re.DOTALL)
                
                footer_to_remove = None
                if bp_footer_match:
                    footer_to_remove = bp_footer_match
                elif results_footer_match:
                    footer_to_remove = results_footer_match
                
                if footer_to_remove:
                    # Remove the old footer
                    content = content[:footer_to_remove.start()] + content[footer_to_remove.end():]
                    
                    # Insert new footer before wrapper closing
                    # Find the right place - should be before </div> <!-- wrapper -->
                    insert_pos = wrapper_end
                    # Make sure we're inserting in the right place (before closing divs)
                    content = content[:insert_pos] + '\n\t\t' + footer_content + '\n\t\t' + content[insert_pos:]
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error with {file_path}: {e}")
        return False

def main():
    """Fix footers on results pages"""
    footer_content = get_homepage_footer()
    if not footer_content:
        print("ERROR: Could not extract footer from index.html")
        return
    
    base_dir = Path('blackpropeller.com/results')
    html_files = list(base_dir.rglob('*.html'))
    
    fixed = 0
    for html_file in html_files:
        if fix_results_footer(html_file, footer_content):
            print(f"Fixed footer: {html_file}")
            fixed += 1
    
    print(f"\nFixed {fixed} files")

if __name__ == '__main__':
    main()

