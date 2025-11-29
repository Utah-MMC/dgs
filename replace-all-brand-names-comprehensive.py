#!/usr/bin/env python3
"""
Comprehensively replace "Black Propeller" and "#TeamBP" with "Digital Growth Studios" and "#TeamDGS"
throughout all HTML files, including in attributes, text content, and all variations.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

def replace_brand_names_comprehensive(file_path):
    """Replace brand names comprehensively in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all variations (case-insensitive):
        # "Black Propeller" -> "Digital Growth Studios"
        content = re.sub(r'Black\s+Propeller', 'Digital Growth Studios', content, flags=re.IGNORECASE)
        
        # "#TeamBP" -> "#TeamDGS"
        content = re.sub(r'#TeamBP', '#TeamDGS', content, flags=re.IGNORECASE)
        
        # "TeamBP" (without #) -> "TeamDGS"
        # But be careful not to replace "#TeamDGS" -> "#TeamTeamDGS"
        # Use word boundaries to avoid partial matches
        content = re.sub(r'\bTeamBP\b', 'TeamDGS', content, flags=re.IGNORECASE)
        
        # Also handle in HTML attributes and other contexts
        # Replace in alt text, title attributes, etc.
        content = re.sub(r'black\s+propeller', 'Digital Growth Studios', content, flags=re.IGNORECASE)
        
        # Handle variations like "BlackPropeller" (no space)
        content = re.sub(r'BlackPropeller', 'Digital Growth Studios', content, flags=re.IGNORECASE)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing {file_path}: {e}")
        return False

def replace_in_soup(file_path):
    """Also use BeautifulSoup to replace in text nodes and attributes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        modified = False
        
        # Replace in all text nodes
        for text_node in soup.find_all(string=True):
            if text_node.parent and text_node.parent.name in ['script', 'style']:
                continue  # Skip script and style tags
            
            original_text = str(text_node)
            new_text = original_text
            
            # Replace "Black Propeller" -> "Digital Growth Studios"
            new_text = re.sub(r'Black\s+Propeller', 'Digital Growth Studios', new_text, flags=re.IGNORECASE)
            new_text = re.sub(r'BlackPropeller', 'Digital Growth Studios', new_text, flags=re.IGNORECASE)
            
            # Replace "#TeamBP" -> "#TeamDGS"
            new_text = re.sub(r'#TeamBP', '#TeamDGS', new_text, flags=re.IGNORECASE)
            
            # Replace "TeamBP" -> "TeamDGS" (but not if it's part of "#TeamDGS")
            new_text = re.sub(r'\bTeamBP\b', 'TeamDGS', new_text, flags=re.IGNORECASE)
            
            if new_text != original_text:
                text_node.replace_with(new_text)
                modified = True
        
        # Replace in attributes
        for tag in soup.find_all(True):  # Find all tags
            for attr_name, attr_value in tag.attrs.items():
                if isinstance(attr_value, str):
                    original_value = attr_value
                    new_value = original_value
                    
                    # Replace in attribute values
                    new_value = re.sub(r'Black\s+Propeller', 'Digital Growth Studios', new_value, flags=re.IGNORECASE)
                    new_value = re.sub(r'BlackPropeller', 'Digital Growth Studios', new_value, flags=re.IGNORECASE)
                    new_value = re.sub(r'#TeamBP', '#TeamDGS', new_value, flags=re.IGNORECASE)
                    new_value = re.sub(r'\bTeamBP\b', 'TeamDGS', new_value, flags=re.IGNORECASE)
                    
                    if new_value != original_value:
                        tag.attrs[attr_name] = new_value
                        modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
        return False
    
    except Exception as e:
        print(f"  [ERROR] Error processing with BeautifulSoup {file_path}: {e}")
        return False

def main():
    """Main replacement process."""
    print(f"{'='*70}")
    print(f"Comprehensive Brand Name Replacement")
    print(f"{'='*70}")
    print(f"Replacing:")
    print(f"  - 'Black Propeller' -> 'Digital Growth Studios'")
    print(f"  - 'BlackPropeller' -> 'Digital Growth Studios'")
    print(f"  - '#TeamBP' -> '#TeamDGS'")
    print(f"  - 'TeamBP' -> 'TeamDGS'")
    print()
    
    base_dir = Path('blackpropeller.com')
    
    # Find all HTML files
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        file_str = str(html_file)
        # Skip wp-content, wp-includes, etc.
        if 'wp-content' not in file_str and 'wp-includes' not in file_str and 'wp-json' not in file_str:
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    replaced_count = 0
    skipped_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        rel_path = html_file.relative_to(base_dir)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path}")
        
        # First do regex replacement
        regex_changed = replace_brand_names_comprehensive(html_file)
        
        # Then do BeautifulSoup replacement for text nodes and attributes
        soup_changed = replace_in_soup(html_file)
        
        if regex_changed or soup_changed:
            replaced_count += 1
            print(f"  [OK] Replaced brand names")
        else:
            skipped_count += 1
            print(f"  - No replacements needed")
    
    print(f"\n{'='*70}")
    print(f"Replacement Complete!")
    print(f"  [OK] Files updated: {replaced_count}")
    print(f"  - Files unchanged: {skipped_count}")
    print(f"{'='*70}")
    
    # Final verification
    print(f"\nVerifying replacements...")
    remaining = []
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'Black\s+Propeller|BlackPropeller|#TeamBP|\bTeamBP\b', content, re.IGNORECASE):
                remaining.append(str(html_file.relative_to(base_dir)))
    
    if remaining:
        print(f"  [WARNING] Found remaining instances in {len(remaining)} files:")
        for file in remaining[:10]:  # Show first 10
            print(f"    - {file}")
        if len(remaining) > 10:
            print(f"    ... and {len(remaining) - 10} more")
    else:
        print(f"  [OK] No remaining instances found!")

if __name__ == '__main__':
    main()

