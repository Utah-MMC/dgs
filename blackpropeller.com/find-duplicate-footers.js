const fs = require('fs');
const path = require('path');

// Function to find files with duplicate footers
function findDuplicates(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Count copyright notices
    const copyrightMatches = content.match(/COPYRIGHT.*?(?:DIGITAL GROWTH STUDIOS|Digital Growth Studios)/gi);
    const count = copyrightMatches ? copyrightMatches.length : 0;
    
    if (count > 1) {
      return { hasDuplicates: true, count };
    }
    
    // Also check for multiple footer sections
    const footerRowMatches = content.match(/fusion-builder-row-1[3489]/g);
    const footerCount = footerRowMatches ? footerRowMatches.length : 0;
    
    // If there are multiple footer rows after the main footer, it might be duplicates
    if (footerCount > 2) {
      return { hasDuplicates: true, count: footerCount, reason: 'multiple footer rows' };
    }
    
    return { hasDuplicates: false };
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
console.log('Finding all HTML files with duplicate footers...\n');

const htmlFiles = findHtmlFiles(baseDir);
console.log(`Found ${htmlFiles.length} HTML files\n`);

let duplicateCount = 0;
const filesWithDuplicates = [];

htmlFiles.forEach((filePath) => {
  const relativePath = path.relative(baseDir, filePath);
  const result = findDuplicates(filePath);
  
  if (result.hasDuplicates) {
    duplicateCount++;
    filesWithDuplicates.push({ path: relativePath, count: result.count, reason: result.reason });
    console.log(`[${duplicateCount}] ${relativePath} - ${result.count} copyright notices${result.reason ? ' (' + result.reason + ')' : ''}`);
  }
});

console.log(`\n=== Summary ===`);
console.log(`Total files checked: ${htmlFiles.length}`);
console.log(`Files with duplicates: ${duplicateCount}`);

if (filesWithDuplicates.length > 0) {
  console.log(`\nFiles that need fixing:`);
  filesWithDuplicates.forEach(f => console.log(`  - ${f.path}`));
}

