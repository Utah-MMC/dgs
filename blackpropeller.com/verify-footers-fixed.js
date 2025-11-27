const fs = require('fs');
const path = require('path');

// Function to check if a file has duplicate footers (more accurate)
function checkForDuplicates(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Find all actual copyright notices in footer context
    // Look for COPYRIGHT followed by DIGITAL GROWTH STUDIOS or Digital Growth Studios
    const copyrightPattern = /COPYRIGHT\s*©\s*(?:<script[^>]*>.*?<\/script>)?\s*(?:DIGITAL GROWTH STUDIOS|Digital Growth Studios)/gi;
    const matches = content.match(copyrightPattern);
    
    if (!matches) {
      return { hasDuplicates: false, count: 0 };
    }
    
    const count = matches.length;
    
    // Also check for multiple footer sections between main footer and wrapper
    const mainFooterEnd = content.search(/DIGITAL GROWTH STUDIOS<\/p>\s*<\/div><\/div><\/div><\/div><\/div>\s*<\/div><\/div>/i);
    const wrapperClose = content.indexOf('</div> <!-- wrapper -->');
    
    if (mainFooterEnd !== -1 && wrapperClose !== -1 && wrapperClose > mainFooterEnd) {
      const sectionBetween = content.substring(mainFooterEnd, wrapperClose);
      const copyrightInBetween = (sectionBetween.match(copyrightPattern) || []).length;
      
      if (copyrightInBetween > 0) {
        return { hasDuplicates: true, count: copyrightInBetween + 1, reason: 'copyright in duplicate section' };
      }
    }
    
    // If there's more than 1 copyright, it's likely duplicates
    if (count > 1) {
      return { hasDuplicates: true, count };
    }
    
    return { hasDuplicates: false, count };
  } catch (error) {
    return { error: error.message };
  }
}

// Function to find all HTML files recursively
function findHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      if (!file.startsWith('.') && file !== 'node_modules') {
        findHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Main execution
const baseDir = __dirname;
console.log('Verifying all HTML files for duplicate footers...\n');

const htmlFiles = findHtmlFiles(baseDir);
console.log(`Found ${htmlFiles.length} HTML files\n`);

let duplicateCount = 0;
const filesWithDuplicates = [];

htmlFiles.forEach((filePath) => {
  const relativePath = path.relative(baseDir, filePath);
  const result = checkForDuplicates(filePath);
  
  if (result.hasDuplicates) {
    duplicateCount++;
    filesWithDuplicates.push({ path: relativePath, count: result.count, reason: result.reason });
    console.log(`[${duplicateCount}] ${relativePath} - ${result.count} copyright notices${result.reason ? ' (' + result.reason + ')' : ''}`);
  }
});

console.log(`\n=== Summary ===`);
console.log(`Total files checked: ${htmlFiles.length}`);
console.log(`Files with duplicates: ${duplicateCount}`);

if (filesWithDuplicates.length === 0) {
  console.log(`\n✓ All pages are fixed! No duplicate footers found.`);
} else {
  console.log(`\nFiles that still need fixing:`);
  filesWithDuplicates.forEach(f => console.log(`  - ${f.path}`));
}

