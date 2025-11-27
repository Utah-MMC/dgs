const fs = require('fs');
const path = require('path');

// Function to remove ALL duplicate footers from services/seo/index.html
function removeAllDuplicates(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    const originalLength = content.length;
    
    // Find where the main footer ends (first copyright with DIGITAL GROWTH STUDIOS - uppercase)
    const mainFooterEndRegex = /DIGITAL GROWTH STUDIOS<\/p>\s*<\/div><\/div><\/div><\/div><\/div>\s*<\/div><\/div>/;
    const mainFooterMatch = content.match(mainFooterEndRegex);
    
    if (!mainFooterMatch) {
      console.log('Main footer pattern not found');
      return false;
    }
    
    // Find the position where the main footer ends
    const mainFooterEndIndex = content.indexOf(mainFooterMatch[0]) + mainFooterMatch[0].length;
    console.log(`Main footer ends at index: ${mainFooterEndIndex}`);
    
    // Get content after main footer
    const afterMainFooter = content.substring(mainFooterEndIndex);
    
    // Find where the wrapper div closes
    const wrapperCloseIndex = afterMainFooter.indexOf('</div> <!-- wrapper -->');
    
    if (wrapperCloseIndex === -1) {
      console.log('Wrapper close not found');
      return false;
    }
    
    console.log(`Wrapper close at index: ${wrapperCloseIndex} (relative to main footer end)`);
    
    // Get the section between main footer and wrapper close
    let sectionBetween = afterMainFooter.substring(0, wrapperCloseIndex);
    const originalSectionLength = sectionBetween.length;
    console.log(`Section between has length: ${originalSectionLength} bytes`);
    
    // Count copyright notices in this section
    const copyrightCount = (sectionBetween.match(/DIGITAL GROWTH STUDIOS|Digital Growth Studios/gi) || []).length;
    console.log(`Found ${copyrightCount} copyright notices in duplicate section`);
    
    if (copyrightCount === 0) {
      console.log('No duplicates found');
      return false; // No duplicates
    }
    
    // Remove EVERYTHING in this section - it's all duplicates
    // Just keep minimal whitespace for formatting
    const cleanedSection = '\n\n';
    
    // Reconstruct the file
    const beforeMainFooter = content.substring(0, mainFooterEndIndex);
    const afterWrapper = afterMainFooter.substring(wrapperCloseIndex);
    
    content = beforeMainFooter + cleanedSection + afterWrapper;
    
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      const removedKB = ((originalLength - content.length) / 1000).toFixed(2);
      console.log(`Removed ${removedKB}KB of duplicate content`);
      return { fixed: true, removedKB };
    }
    
    return false;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    return { error: error.message };
  }
}

// Process the SEO page
const seoPagePath = path.join(__dirname, 'services', 'seo', 'index.html');
if (fs.existsSync(seoPagePath)) {
  console.log('Removing ALL duplicate footers from services/seo/index.html...\n');
  const result = removeAllDuplicates(seoPagePath);
  if (result && result.fixed) {
    console.log(`\n✓ Fixed! Removed ${result.removedKB}KB of duplicate content\n`);
  } else if (result && result.error) {
    console.log(`\n✗ Error: ${result.error}\n`);
  } else {
    console.log('\nNo duplicates found or file already fixed.\n');
  }
} else {
  console.error('services/seo/index.html not found!');
}

