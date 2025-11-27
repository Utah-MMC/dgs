# Header and Footer Includes

This directory contains reusable header and footer components for the website.

## Files

- `footer.html` - Standard footer HTML that matches the homepage footer
- `load-includes.js` - JavaScript loader for dynamically loading includes (optional, for future use)

## Usage

### Updating All Footers

To update all footers across all pages to match the homepage footer, run:

```bash
node update-footers.js
```

This script will:
1. Find all HTML files in the site
2. Replace any existing footer with the standard footer from `includes/footer.html`
3. Ensure FontAwesome CDN is included in the `<head>` section
4. Add necessary CSS for proper footer styling

### Manual Updates

If you need to update the footer manually:

1. Edit `includes/footer.html` with your changes
2. Run `node update-footers.js` to apply changes to all pages

### Footer Structure

The standard footer includes:
- **Contact Section**: Address and phone number with social media icons (40px x 40px)
- **Company Links**: Team, Careers, Agency, Results, Blog, Contact
- **Services Links**: SEO, Google Ads, Web Design, Analytics & Strategy, Core Services Overview, Book a Call
- **Copyright**: "COPYRIGHT © [YEAR] DIGITAL GROWTH STUDIOS" at the bottom

### Social Media Icons

All social icons are:
- 40px x 40px in size
- Use FontAwesome icons
- Properly styled with brand colors
- Include proper accessibility attributes

## Notes

- The footer is directly embedded in HTML files (not loaded dynamically)
- Changes to `footer.html` require running the update script to propagate
- The script preserves all other content in each HTML file
- FontAwesome CDN is automatically added if missing

