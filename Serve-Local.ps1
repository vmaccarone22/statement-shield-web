# Statement Shield — local preview (NOT exposed to the internet by itself).
# Binds only to 127.0.0.1 so nothing off your PC can hit this port directly.
#
# For partners: install cloudflared (winget install Cloudflare.cloudflared), then
# in a second terminal run:
#   cloudflared tunnel --url http://127.0.0.1:8080
# Share only that HTTPS link; stop both windows when the demo is done.

$ErrorActionPreference = "Stop"
$port = 8080
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "  Statement Shield — local server" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:$port  (you only — same machine)" -ForegroundColor Green
Write-Host ""
Write-Host "  Partners: open another terminal and run:" -ForegroundColor Yellow
Write-Host "    cloudflared tunnel --url http://127.0.0.1:$port" -ForegroundColor White
Write-Host ""
Write-Host "  Ctrl+C here stops the site. This does not open your firewall." -ForegroundColor DarkGray
Write-Host ""

py -3 -m http.server $port --bind 127.0.0.1
