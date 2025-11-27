#!/usr/bin/env python3
"""
Remove duplicate bp-header from results pages - they should only use fusion-tb-header
"""

import re
from pathlib import Path

def remove_bp_header(file_path):
    """Remove the bp-header section from a page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if page has both bp-header and fusion-tb-header
        if '<div class="bp-header">' in content and 'fusion-tb-header' in content:
            # Find the bp-header section start
            bp_start = content.find('<div class="bp-header">')
            if bp_start >= 0:
                # Find the closing </div> for bp-header (it's the second one)
                # First find the end of the mobile menu div
                bp_end = content.find('</div>', bp_start)
                if bp_end > bp_start:
                    # Find the closing </div> for the outer bp-header div
                    bp_end = content.find('</div>', bp_end + 6)
                    if bp_end > bp_start:
                        # Find the script that follows
                        script_start = content.find('<script>', bp_end)
                        if script_start > bp_end:
                            # Find the end of the script
                            script_end = content.find('</script>', script_start)
                            if script_end > script_start:
                                # Remove everything from bp-header to end of script
                                content = content[:bp_start] + content[script_end + 9:]
                                
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                return True
        
        return False
    except Exception as e:
        print(f"Error with {file_path}: {e}")
        return False

def main():
    """Remove duplicate headers from results pages"""
    base_dir = Path('blackpropeller.com/results')
    if not base_dir.exists():
        print("Results directory not found")
        return
    
    html_files = list(base_dir.rglob('*.html'))
    
    fixed = 0
    for html_file in html_files:
        if remove_bp_header(html_file):
            print(f"Removed duplicate header: {html_file}")
            fixed += 1
    
    print(f"\nFixed {fixed} files")

if __name__ == '__main__':
    main()

