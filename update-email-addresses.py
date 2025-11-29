#!/usr/bin/env python3
"""
Script to update all email addresses in the codebase to support@digitalgrowthsolutions.com
"""

import os
import re
from pathlib import Path

# Email addresses to replace
EMAIL_REPLACEMENTS = {
    'support@digitalgrowthsolutions.com': 'support@digitalgrowthsolutions.com',
    'support@digitalgrowthsolutions.com': 'support@digitalgrowthsolutions.com',
    'support@digitalgrowthsolutions.com': 'support@digitalgrowthsolutions.com',  # Case variation
}

def update_emails_in_file(file_path):
    """Update email addresses in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        updated = False
        
        # Replace each email address
        for old_email, new_email in EMAIL_REPLACEMENTS.items():
            if old_email in content:
                content = content.replace(old_email, new_email)
                updated = True
        
        # Also handle case-insensitive replacements in JSON/HTML attributes
        # Pattern for email in JSON-LD or HTML attributes
        email_pattern = r'("email"\s*:\s*")[^"]*@digitalgrowthstudios\.com(")'
        matches = re.findall(email_pattern, content, re.IGNORECASE)
        if matches:
            content = re.sub(
                email_pattern,
                r'\1support@digitalgrowthsolutions.com\2',
                content,
                flags=re.IGNORECASE
            )
            updated = True
        
        # Pattern for mailto: links
        mailto_pattern = r'(mailto:)[^"\'@]*@digitalgrowthstudios\.com'
        if re.search(mailto_pattern, content, re.IGNORECASE):
            content = re.sub(
                mailto_pattern,
                r'\1support@digitalgrowthsolutions.com',
                content,
                flags=re.IGNORECASE
            )
            updated = True
        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all files."""
    base_dir = Path('blackpropeller.com')
    
    if not base_dir.exists():
        print(f"❌ Directory {base_dir} not found!")
        return
    
    # Find all HTML files (skip node_modules and other non-essential directories)
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        # Skip node_modules and other non-essential directories
        if 'node_modules' in str(html_file) or 'wp-content/plugins' in str(html_file):
            continue
        html_files.append(html_file)
    
    # Also check Python files in root
    python_files = list(Path('.').glob('*.py'))
    
    print(f"Found {len(html_files)} HTML files and {len(python_files)} Python files")
    print("Processing files...\n")
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    # Process HTML files
    for html_file in html_files:
        relative_path = html_file.relative_to(base_dir)
        print(f"Processing: {relative_path}")
        
        if update_emails_in_file(html_file):
            print(f"  ✅ Updated email addresses")
            updated_count += 1
        else:
            skipped_count += 1
    
    # Process Python files
    for py_file in python_files:
        print(f"Processing: {py_file}")
        if update_emails_in_file(py_file):
            print(f"  ✅ Updated email addresses")
            updated_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "="*60)
    print("Summary:")
    print(f"  ✅ Updated: {updated_count} files")
    print(f"  ⏭️  Skipped (no changes needed): {skipped_count} files")
    print(f"  ❌ Errors: {error_count} files")
    print(f"  📊 Total: {len(html_files) + len(python_files)} files")
    print("="*60)
    print("\nEmail replacements:")
    for old, new in EMAIL_REPLACEMENTS.items():
        print(f"  {old} → {new}")

if __name__ == '__main__':
    main()

