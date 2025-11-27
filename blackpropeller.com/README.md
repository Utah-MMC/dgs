# Digital Growth Studios Local Development Server

This is a static website that can be served locally using one of several methods.

## Quick Start

### Option 1: Node.js Server (Recommended)
```bash
npm start
```
or
```bash
node server.js
```

The server will start on **http://localhost:8000**

### Option 2: PowerShell Server
```powershell
.\start-server.ps1
```

### Option 3: Python Server
```bash
python -m http.server 8000
```

### Option 4: Batch File
```bash
server.bat
```

## Accessing the Site

Once the server is running, open your browser and navigate to:
- **http://localhost:8000**

## Stopping the Server

- **Node.js/Python**: Press `Ctrl+C` in the terminal
- **PowerShell**: Press `Ctrl+C` in the terminal
- To kill all Node processes: `Get-Process node | Stop-Process`

## Notes

- The server runs on port 8000 by default
- All files are served from the `digitalgrowthstudios.com` directory
- The site is a static HTML website (WordPress export/mirror)

