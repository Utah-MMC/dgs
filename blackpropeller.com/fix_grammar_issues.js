// fix_grammar_issues.js - Fix specific grammar and punctuation issues
const fs = require("fs-extra");
const path = require("path");

const INPUT_JSON = path.join(__dirname, "content_rewritten.json");

function fixGrammarIssues(text, original) {
  let fixed = text;
  
  // Fix SEO expansion - revert to SEO
  fixed = fixed.replace(/search engine enhancement/gi, 'SEO');
  fixed = fixed.replace(/search engine optimization/gi, 'SEO');
  
  // Fix punctuation issues
  // Remove periods added to short navigation items
  if (original.length < 50 && !original.endsWith('.') && !original.endsWith('!') && !original.endsWith('?')) {
    if (fixed.endsWith('.') && !original.endsWith('.')) {
      fixed = fixed.slice(0, -1);
    }
  }
  
  // Fix double periods
  fixed = fixed.replace(/\.\./g, '.');
  
  // Fix awkward phrases
  fixed = fixed.replace(/construct awareness/gi, 'build awareness');
  fixed = fixed.replace(/constructing awareness/gi, 'building awareness');
  fixed = fixed.replace(/we team /gi, 'we ');
  fixed = fixed.replace(/generaten/gi, 'generated');
  fixed = fixed.replace(/effectiveness Creative/gi, 'Performance Creative');
  
  // Fix spacing issues
  fixed = fixed.replace(/\s+/g, ' ');
  fixed = fixed.trim();
  
  return fixed;
}

async function main() {
  console.log("Loading content_rewritten.json...");
  let jsonContent = fs.readFileSync(INPUT_JSON, "utf8");
  // Remove BOM if present
  if (jsonContent.charCodeAt(0) === 0xFEFF) {
    jsonContent = jsonContent.slice(1);
  }
  const allBlocks = JSON.parse(jsonContent);
  console.log(`Total blocks: ${allBlocks.length}`);
  
  let fixed = 0;
  
  allBlocks.forEach((block, index) => {
    if (block.rewritten) {
      const fixedText = fixGrammarIssues(block.rewritten, block.original);
      if (fixedText !== block.rewritten) {
        allBlocks[index].rewritten = fixedText;
        fixed++;
      }
    }
  });
  
  // Save
  fs.writeFileSync(INPUT_JSON, JSON.stringify(allBlocks, null, 2), "utf8");
  console.log(`\n✓ Fixed ${fixed} blocks with grammar and punctuation corrections`);
  console.log(`Updated: ${INPUT_JSON}`);
  console.log("\nNow run: node apply_rewrites.js");
}

main().catch(console.error);

