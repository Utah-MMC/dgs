const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 8000;
const ROOT_DIR = __dirname;

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.xml': 'application/xml',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'application/vnd.ms-fontobject'
};

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url);
  let pathname = parsedUrl.pathname;
  
  // Default to index.html for root
  if (pathname === '/') {
    pathname = '/index.html';
  }
  
  // Parse URL to get pathname and query
  const urlObj = url.parse(req.url, true);
  let cleanPathname = urlObj.pathname;
  
  // Helper function to check if file exists
  function fileExistsSync(filePath) {
    try {
      return fs.statSync(filePath).isFile();
    } catch (e) {
      return false;
    }
  }
  
  // Remove leading slash and build initial file path
  let filePath = path.join(ROOT_DIR, cleanPathname.replace(/^\//, ''));
  let foundFile = fileExistsSync(filePath);
  
  // For CSS/JS files with query params, ignore query params and serve the file directly
  // Example: /wp-content/uploads/fusion-styles/file.css?ver=3.10.1 -> /wp-content/uploads/fusion-styles/file.css
  if (!foundFile && urlObj.query && Object.keys(urlObj.query).length > 0) {
    // Try the file without query params first (this is the correct approach)
    if (fileExistsSync(filePath)) {
      foundFile = true;
    } else {
      // Fallback: try @ format if file doesn't exist (for edge cases)
      const ext = path.extname(filePath);
      const queryStr = Object.keys(urlObj.query).map(k => `${k}=${urlObj.query[k]}`).join('&');
      const altPath = filePath + '@' + queryStr + ext;
      if (fileExistsSync(altPath)) {
        filePath = altPath;
        foundFile = true;
      }
    }
  }
  
  // Get file extension for content type
  const ext = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[ext] || 'application/octet-stream';
  
  // Serve file if found, otherwise try directory with index.html
  if (foundFile) {
    serveFile(filePath, contentType, res);
  } else {
    // Try with index.html if it's a directory
    const indexPath = path.join(filePath, 'index.html');
    fs.stat(indexPath, (err2, stats2) => {
      if (err2 || !stats2.isFile()) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found: ' + cleanPathname);
      } else {
        serveFile(indexPath, 'text/html', res);
      }
    });
  }
});

function serveFile(filePath, contentType, res) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('500 Internal Server Error: ' + err.message);
    } else {
      // Remove UTF-8 BOM if present (first 3 bytes: EF BB BF)
      if (data.length >= 3 && data[0] === 0xEF && data[1] === 0xBB && data[2] === 0xBF) {
        data = data.slice(3);
      }
      
      // Add charset for text/html and text/css files
      let finalContentType = contentType;
      if (contentType === 'text/html') {
        finalContentType = 'text/html; charset=utf-8';
      } else if (contentType === 'text/css') {
        finalContentType = 'text/css; charset=utf-8';
      }
      
      // Add CORS headers for fonts and external resources
      const headers = { 'Content-Type': finalContentType };
      if (contentType.startsWith('font/') || contentType === 'application/javascript') {
        headers['Access-Control-Allow-Origin'] = '*';
      }
      
      res.writeHead(200, headers);
      res.end(data);
    }
  });
}

server.listen(PORT, 'localhost', () => {
  console.log(`\n🚀 Server running at http://localhost:${PORT}`);
  console.log(`📁 Serving files from: ${ROOT_DIR}`);
  console.log(`\nPress Ctrl+C to stop the server\n`);
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`\n❌ Port ${PORT} is already in use.`);
    console.error(`Please stop the other process or use a different port.\n`);
  } else {
    console.error(`\n❌ Server error: ${err.message}\n`);
  }
  process.exit(1);
});

// Handle uncaught errors
process.on('uncaughtException', (err) => {
  console.error(`\n❌ Uncaught Exception: ${err.message}\n`);
  console.error(err.stack);
  process.exit(1);
});
