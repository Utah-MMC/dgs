#!/usr/bin/env python3
"""
Script to add Google Tag (gtag.js) to all HTML pages in the website.
Adds the tag immediately after the <head> element if it's not already present.
"""

import os
import re
from pathlib import Path

# Google Tag code to insert
GOOGLE_TAG_CODE = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K2QTGJ1VLC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-K2QTGJ1VLC');
</script>
"""

def has_google_tag(content):
    """Check if the HTML content already has the Google tag."""
    # Check for the tracking ID or the gtag.js script
    return 'G-K2QTGJ1VLC' in content or 'googletagmanager.com/gtag/js' in content

def add_google_tag_to_file(file_path):
    """Add Google tag to a single HTML file if it doesn't already have it."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Skip if already has the tag
        if has_google_tag(content):
            return False
        
        # Find the <head> tag (case-insensitive, handle various formats)
        head_pattern = r'(<head[^>]*>)'
        match = re.search(head_pattern, content, re.IGNORECASE)
        
        if not match:
            print(f"  ⚠️  Warning: No <head> tag found in {file_path}")
            return False
        
        # Insert the Google tag right after <head>
        head_end = match.end()
        new_content = content[:head_end] + '\n' + GOOGLE_TAG_CODE + content[head_end:]
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all HTML files."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"❌ Directory {base_dir} not found!")
        return
    
    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))
    
    print(f"Found {len(html_files)} HTML files")
    print("Processing files...\n")
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for html_file in html_files:
        relative_path = html_file.relative_to(base_dir)
        print(f"Processing: {relative_path}")
        
        if add_google_tag_to_file(html_file):
            print(f"  ✅ Added Google tag")
            updated_count += 1
        else:
            # Check if it was skipped because it already has the tag
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if has_google_tag(content):
                    print(f"  ⏭️  Already has Google tag, skipped")
                    skipped_count += 1
                else:
                    error_count += 1
            except:
                error_count += 1
    
    print("\n" + "="*60)
    print("Summary:")
    print(f"  ✅ Updated: {updated_count} files")
    print(f"  ⏭️  Skipped (already has tag): {skipped_count} files")
    print(f"  ❌ Errors: {error_count} files")
    print(f"  📊 Total: {len(html_files)} files")
    print("="*60)

if __name__ == '__main__':
    main()

