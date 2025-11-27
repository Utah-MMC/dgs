const fs = require('fs');
const path = require('path');

// Read the standard footer
const standardFooter = fs.readFileSync(path.join(__dirname, 'includes', 'footer.html'), 'utf8');

// Function to find all HTML files recursively
function findHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      // Skip node_modules, includes, and other non-content directories
      if (!['node_modules', 'includes', 'wp-content', 'wp-includes', 'wp-json', 'assets'].includes(file)) {
        findHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html') && file !== 'index.html.backup') {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Function to replace footer in a file
function replaceFooter(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    // Find the footer section - look for fusion-tb-footer
    const footerRegex = /<div class="fusion-tb-footer fusion-footer">[\s\S]*?<\/div><\/div>\s*<\/div><\/div>/;
    
    if (footerRegex.test(content)) {
      // Replace the first footer
      content = content.replace(footerRegex, standardFooter);
      
      // Remove any duplicate footer sections that appear after the main footer
      // Look for additional fusion-tb-footer sections
      const allFooters = content.match(/<div class="fusion-tb-footer fusion-footer">[\s\S]*?<\/div><\/div>\s*<\/div><\/div>/g);
      if (allFooters && allFooters.length > 1) {
        // Keep only the first one (which we just replaced), remove the rest
        let footerCount = 0;
        content = content.replace(/<div class="fusion-tb-footer fusion-footer">[\s\S]*?<\/div><\/div>\s*<\/div><\/div>/g, (match) => {
          footerCount++;
          if (footerCount === 1) {
            return standardFooter; // Keep the first (standard) footer
          }
          return ''; // Remove duplicates
        });
      }
      
      // Remove Clutch widget scripts and divs
      content = content.replace(/<script type="text\/javascript" src="https:\/\/widget\.clutch\.co[^>]*><\/script>/gi, '');
      content = content.replace(/<div class="clutch-widget"[^>]*><\/div>/gi, '');
      
      // Remove "We Mean Business" column sections that contain Clutch
      // This pattern matches the entire column div containing "We Mean Business"
      const clutchColumnRegex = /<div class="fusion-layout-column[^>]*fusion_builder_column-[^>]*1_4[^>]*>[\s\S]*?We Mean Business[\s\S]*?<\/div><\/div><\/div><\/div>/gi;
      content = content.replace(clutchColumnRegex, '');
      
      // Remove any extra footer sections that appear after the main footer
      // Look for patterns like: </div></div></div></div></div><div class="fusion-fullwidth...fusion-builder-row-5 or 6
      const extraFooterPattern = /<\/div><\/div>\s*<\/div><\/div>\s*<\/div><div class="fusion-fullwidth[^>]*fusion-builder-row-[56][^>]*>[\s\S]*?(?:fusion-tb-footer|clutch-widget|We Mean Business)[\s\S]*?<\/div><\/div>\s*<\/div><\/div>/gi;
      let previousContent;
      do {
        previousContent = content;
        content = content.replace(extraFooterPattern, '');
      } while (content !== previousContent);
      
      // Also ensure FontAwesome CDN is in the head if not present
      if (!content.includes('cdnjs.cloudflare.com/ajax/libs/font-awesome')) {
        const headEndRegex = /<\/head>/;
        if (headEndRegex.test(content)) {
          const fontAwesomeLink = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />\n';
          content = content.replace(headEndRegex, fontAwesomeLink + '</head>');
        }
      }
      
      // Add footer styling if not present
      if (!content.includes('.fusion-social-network-icon')) {
        const styleBlock = `
<style>
  .fusion-social-network-icon {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 40px !important;
    height: 40px !important;
    font-size: 20px !important;
    line-height: 40px !important;
  }
  .fusion-social-network-icon i {
    font-size: 20px !important;
  }
  .fusion-builder-row-19 {
    padding-top: 40px !important;
    padding-bottom: 40px !important;
  }
</style>
`;
        const headEndRegex = /<\/head>/;
        if (headEndRegex.test(content)) {
          content = content.replace(headEndRegex, styleBlock + '</head>');
        }
      }
      
      // Only write if content changed
      if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Updated: ${filePath}`);
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
const rootDir = __dirname;
const htmlFiles = findHtmlFiles(rootDir);

console.log(`Found ${htmlFiles.length} HTML files`);
console.log('Updating footers...\n');

let updatedCount = 0;
htmlFiles.forEach(file => {
  if (replaceFooter(file)) {
    updatedCount++;
  }
});

console.log(`\nCompleted! Updated ${updatedCount} files.`);
