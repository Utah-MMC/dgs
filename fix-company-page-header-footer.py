import re
from pathlib import Path

def fix_company_page(file_path):
    """Fix header background color and footer on company page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Add CSS for header background color (before </head>)
        header_css = '''<style type="text/css" id="header-background-fix">
/* Ensure header has background color from the start */
.fusion-tb-header .fusion-fullwidth {
  background-color: var(--awb-color4) !important;
}
</style>'''
        
        # Check if CSS already exists
        if 'header-background-fix' not in content:
            # Insert before </head>
            head_end_match = re.search(r'</head>', content)
            if head_end_match:
                content = content[:head_end_match.start()] + header_css + '\n' + content[head_end_match.start():]
        
        # 2. Replace the simple copyright footer with the full footer from homepage
        homepage_path = Path('blackpropeller.com/index.html')
        with open(homepage_path, 'r', encoding='utf-8') as f:
            homepage_content = f.read()
        
        # Extract full footer from homepage
        footer_match = re.search(r'(<div class="fusion-tb-footer fusion-footer">.*?</div></div>)', homepage_content, re.DOTALL)
        if footer_match:
            homepage_footer = footer_match.group(1)
            
            # Find the simple copyright footer on company page (line 76)
            # Pattern: <div class="fusion-fullwidth...fusion-builder-row-19...>...COPYRIGHT...</div></div>
            simple_footer_pattern = r'<div class="fusion-fullwidth fullwidth-box fusion-builder-row-19[^>]*>.*?COPYRIGHT.*?</div></div></div></div>'
            simple_footer_match = re.search(simple_footer_pattern, content, re.DOTALL)
            
            if simple_footer_match:
                # Replace simple footer with full footer
                # Need to insert before </main> or before wrapper closing
                # Find where to insert (before </main> or before wrapper closing)
                main_end_match = re.search(r'</main>', content)
                if main_end_match:
                    # Remove the simple footer
                    content = content[:simple_footer_match.start()] + content[simple_footer_match.end():]
                    # Insert full footer before </main>
                    content = content[:main_end_match.start()] + '\n\t\t' + homepage_footer + '\n' + content[main_end_match.start():]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    company_page = Path('blackpropeller.com/company/index.html')
    if fix_company_page(company_page):
        print(f"Fixed: {company_page}")
    else:
        print(f"Failed to fix: {company_page}")

if __name__ == '__main__':
    main()



