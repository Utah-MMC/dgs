#!/usr/bin/env python3
"""Clean up the results page by removing everything after </html>"""

file_path = 'blackpropeller.com/results/index.html'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find the position of </html> (even if it has content after it)
html_end = content.find('</html>')
if html_end != -1:
    # Keep only up to and including </html> and a newline
    content = content[:html_end + 7] + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Cleaned up {file_path}")
    print(f"   File now ends at position {len(content)} characters")
else:
    print("❌ Could not find </html> tag")

