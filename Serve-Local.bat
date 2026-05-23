@echo off
setlocal
cd /d "%~dp0"
title Fund Pilot - local server
echo.
echo   Local preview:  http://127.0.0.1:8080
echo   For partners, use cloudflared in another window (see Serve-Local.ps1 comments).
echo.
py -3 "%~dp0serve_local.py" --port 8080 --bind 127.0.0.1
pause
