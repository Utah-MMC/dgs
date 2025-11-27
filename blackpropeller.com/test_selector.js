// test_selector.js
const fs = require("fs");
const cheerio = require("cheerio");

const html = fs.readFileSync("blog/ultimate-guide-to-setting-up-a-google-ads-campaign/index.html", "utf8");
const $ = cheerio.load(html);

const targetId = "blog\\ultimate-guide-to-setting-up-a-google-ads-campaign\\index.html::24";
console.log("Testing selector for:", targetId);

// Try escaped backslash
const escapedId = targetId.replace(/\\/g, "\\\\");
const selector1 = `[data-rewrite-id="${escapedId}"]`;
const found1 = $(selector1);
console.log(`Escaped selector: ${selector1}`);
console.log("Found:", found1.length);

if (found1.length > 0) {
  console.log("Current text:", found1.text().substring(0, 100));
  console.log("✓ Selector works!");
}

