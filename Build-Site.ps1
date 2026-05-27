# Fund Pilot — verify static site, optional cache-bust for production ZIPs/CDN.
# Local preview: .\Serve-Local.ps1  (serves with no-cache headers so refresh is enough)
#
# Production / handoff: .\Build-Site.ps1 -Stamp  appends ?v=<unixtime> to css/styles.css + js/main.js

param(
    [switch]$Stamp
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$required = @(
    "index.html",
    "privacy.html",
    "terms.html",
    "css/styles.css",
    "js/main.js",
    "js/hero-3d.js",
    "js/scene-showcase.js",
    "js/device-3d.js",
    "assets/favicon.svg",
    "assets/social-card.svg",
    "assets/iphone-followup-notification-demo.png",
    "serve_local.py"
)

foreach ($f in $required) {
    $p = Join-Path $root $f
    if (-not (Test-Path -LiteralPath $p)) {
        Write-Error "Missing required file: $f"
    }
}

if ($Stamp) {
    $v = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $htmlFiles = @("index.html", "privacy.html", "terms.html")
    foreach ($hf in $htmlFiles) {
        $p = Join-Path $root $hf
        $text = Get-Content -LiteralPath $p -Raw -Encoding UTF8
        $text = $text -replace 'href="css/styles\.css(\?[^"]*)?"', "href=`"css/styles.css?v=$v`""
        $text = $text -replace 'src="js/main\.js(\?[^"]*)?"', "src=`"js/main.js?v=$v`""
        $text = $text -replace 'src="js/hero-3d\.js(\?[^"]*)?"', "src=`"js/hero-3d.js?v=$v`""
        Set-Content -LiteralPath $p -Value $text -Encoding UTF8 -NoNewline
    }
    Write-Host "Stamped asset query strings (?v=$v) in: $($htmlFiles -join ', ')" -ForegroundColor Cyan
}

$n = $required.Count
Write-Host "OK: Fund Pilot static site verified ($n paths)." -ForegroundColor Green
Write-Host "Preview (no-cache): .\Serve-Local.ps1" -ForegroundColor Green
if (-not $Stamp) {
    Write-Host "Optional stamp for deploy ZIP: .\Build-Site.ps1 -Stamp" -ForegroundColor DarkGray
}
