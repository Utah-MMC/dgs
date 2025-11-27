@echo off
cd /d "%~dp0"
echo Starting HTTP server on http://localhost:8000
echo Press Ctrl+C to stop the server
python -m http.server 8000
pause

