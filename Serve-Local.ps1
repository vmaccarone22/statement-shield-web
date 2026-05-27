# Fund Pilot — local preview (Apple-inspired marketing page)
# Binds only to 127.0.0.1 — port 8081 (original 3D site uses 8080).
#
# Partners: cloudflared tunnel --url http://127.0.0.1:8081

$ErrorActionPreference = "Stop"
$port = 8081
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "  Fund Pilot — Apple-style site" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:$port  (local only)" -ForegroundColor Green
Write-Host ""
Write-Host "  Original 3D site: ..\website\ on port 8080" -ForegroundColor DarkGray
Write-Host "  Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

py -3 serve_local.py --port $port --bind 127.0.0.1
