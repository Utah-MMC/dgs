const fs = require('fs');
const path = require('path');

// Function to find all HTML files recursively
function findHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      if (!['node_modules', 'includes', 'wp-content', 'wp-includes', 'wp-json', 'assets'].includes(file)) {
        findHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html') && file !== 'index.html.backup') {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Function to remove duplicate footer sections
function removeDuplicateFooters(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    // Find all instances of fusion-builder-row-18 that appear after the main footer
    // These are duplicate footer sections
    const footerEndMarker = '</div></div>\n</div></div>';
    const mainFooterEnd = content.lastIndexOf(footerEndMarker);
    if (mainFooterEnd === -1) return false;
    
    // Get content after main footer
    const afterFooter = content.substring(mainFooterEnd + footerEndMarker.length);
    
    // Remove all duplicate footer sections (fusion-builder-row-18 followed by Contact/Company/Services)
    // Pattern: </div><div class="fusion-fullwidth...fusion-builder-row-18...>...Contact...Company...Services...fusion-builder-row-6...Digital Growth Studios...</div></div>
    const duplicatePattern = /<\/div><div class="fusion-fullwidth[^>]*fusion-builder-row-18[^>]*>[\s\S]*?fusion_builder_column-41[\s\S]*?Contact[\s\S]*?Company[\s\S]*?Services[\s\S]*?fusion-builder-row-19[\s\S]*?DIGITAL GROWTH STUDIOS[\s\S]*?<\/div><\/div>\s*<\/div><\/div>\s*<\/div><div class="fusion-fullwidth[^>]*fusion-builder-row-6[^>]*>[\s\S]*?Digital Growth Studios[\s\S]*?<\/div><\/div>\s*<\/div><\/div>/gi;
    
    let newAfterFooter = afterFooter.replace(duplicatePattern, '');
    
    // Also remove any standalone duplicate sections
    const standaloneDuplicate = /<\/div><div class="fusion-fullwidth[^>]*fusion-builder-row-18[^>]*>[\s\S]*?fusion_builder_column-41[\s\S]*?<\/div><\/div>\s*<\/div><\/div>/gi;
    newAfterFooter = newAfterFooter.replace(standaloneDuplicate, '');
    
    // Remove Clutch widget references
    newAfterFooter = newAfterFooter.replace(/<script type="text\/javascript" src="https:\/\/widget\.clutch\.co[^>]*><\/script>/gi, '');
    newAfterFooter = newAfterFooter.replace(/<div class="clutch-widget"[^>]*><\/div>/gi, '');
    
    if (newAfterFooter !== afterFooter) {
      content = content.substring(0, mainFooterEnd + footerEndMarker.length) + newAfterFooter;
      
      if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Removed duplicate footer from: ${filePath}`);
        return true;
      }
    }
    
    return false;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    return false;
  }
}

// Main execution
const rootDir = path.join(__dirname);
const htmlFiles = findHtmlFiles(rootDir);

console.log(`Found ${htmlFiles.length} HTML files`);
console.log('Removing duplicate footers...\n');

let updatedCount = 0;
htmlFiles.forEach(file => {
  if (removeDuplicateFooters(file)) {
    updatedCount++;
  }
});

console.log(`\nCompleted! Removed duplicates from ${updatedCount} files.`);

