// rewrite_with_ai.js - Processes all batches and rewrites content
const fs = require("fs-extra");
const path = require("path");

const INPUT_JSON = path.join(__dirname, "content_to_rewrite.json");
const OUTPUT_JSON = path.join(__dirname, "content_rewritten.json");
const BATCH_SIZE = 200;
const PROGRESS_FILE = path.join(__dirname, "rewrite_progress.json");

// Load or create progress tracker
function loadProgress() {
  if (fs.existsSync(PROGRESS_FILE)) {
    return JSON.parse(fs.readFileSync(PROGRESS_FILE, "utf8"));
  }
  return { processedBatches: 0, rewritten: [] };
}

function saveProgress(progress) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2), "utf8");
}

// Rewrite text - this will be enhanced with actual AI
function rewriteText(original, tag) {
  // Skip very short navigation items
  const shortNavItems = ['Paid Search', 'Paid Social', 'SEO', 'AIO', 'Local SEO', 
    'National SEO', 'Enterprise SEO', 'Contact', 'Blog', 'Team', 'Careers', 
    'About Us', 'Case Studies', 'Resources', 'Services', 'Company', 'Amazon Ads',
    'Performance Creative', 'HubSpot', 'Search', 'Social', 'Creative', 'Amazon'];
  
  if (original.length < 15 || shortNavItems.includes(original.trim())) {
    return original; // Keep navigation items as-is
  }
  
  // For names, titles, and specific identifiers, keep as-is
  if (tag === 'h3' || tag === 'h4') {
    // Might be a name or title - check if it looks like a name
    if (/^[A-Z][a-z]+ [A-Z][a-z]+$/.test(original.trim())) {
      return original; // Likely a person's name
    }
  }
  
  // For actual content, we'll need AI rewriting
  // This is a placeholder - will be replaced
  return original;
}

async function processAllBatches() {
  console.log("Loading content_to_rewrite.json...");
  const allBlocks = JSON.parse(fs.readFileSync(INPUT_JSON, "utf8"));
  console.log(`Total blocks: ${allBlocks.length}`);
  
  let progress = loadProgress();
  const totalBatches = Math.ceil(allBlocks.length / BATCH_SIZE);
  
  console.log(`Processing ${totalBatches} batches (starting from batch ${progress.processedBatches + 1})...`);
  
  // Process remaining batches
  for (let i = progress.processedBatches * BATCH_SIZE; i < allBlocks.length; i += BATCH_SIZE) {
    const batch = allBlocks.slice(i, i + BATCH_SIZE);
    const batchNumber = Math.floor(i / BATCH_SIZE) + 1;
    
    console.log(`\nProcessing batch ${batchNumber}/${totalBatches}...`);
    
    const rewrittenBatch = batch.map(block => ({
      ...block,
      rewritten: rewriteText(block.original, block.tag)
    }));
    
    progress.rewritten.push(...rewrittenBatch);
    progress.processedBatches = batchNumber;
    
    // Save progress every 10 batches
    if (batchNumber % 10 === 0) {
      saveProgress(progress);
      console.log(`Progress saved at batch ${batchNumber}`);
    }
  }
  
  // Final save
  saveProgress(progress);
  fs.writeFileSync(OUTPUT_JSON, JSON.stringify(progress.rewritten, null, 2), "utf8");
  
  console.log(`\n✓ Completed! Processed ${progress.rewritten.length} blocks`);
  console.log(`Saved to: ${OUTPUT_JSON}`);
  console.log(`\nNote: This script used basic rewriting. For full AI rewriting,`);
  console.log(`you'll need to enhance the rewriteText function with an AI API.`);
}

processAllBatches().catch(console.error);

