$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8000/")
$listener.Start()
Write-Host "Server running at http://localhost:8000"
Write-Host "Press Ctrl+C to stop"

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    $localPath = $request.Url.LocalPath
    if ($localPath -eq "/") { $localPath = "/index.html" }
    
    $filePath = Join-Path $PSScriptRoot $localPath.TrimStart('/')
    $filePath = $filePath.Replace('/', '\')
    
    if (Test-Path $filePath -PathType Leaf) {
        $content = [System.IO.File]::ReadAllBytes($filePath)
        $response.ContentLength64 = $content.Length
        
        # Set content type
        $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
        $contentTypes = @{
            '.html' = 'text/html'
            '.css' = 'text/css'
            '.js' = 'application/javascript'
            '.png' = 'image/png'
            '.jpg' = 'image/jpeg'
            '.jpeg' = 'image/jpeg'
            '.gif' = 'image/gif'
            '.svg' = 'image/svg+xml'
            '.json' = 'application/json'
            '.xml' = 'application/xml'
        }
        $contentType = $contentTypes[$ext]
        if ($contentType) {
            $response.ContentType = $contentType
        }
        
        $response.OutputStream.Write($content, 0, $content.Length)
    } else {
        $response.StatusCode = 404
        $notFound = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
        $response.ContentLength64 = $notFound.Length
        $response.OutputStream.Write($notFound, 0, $notFound.Length)
    }
    
    $response.Close()
}

