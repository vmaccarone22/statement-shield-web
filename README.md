# Fund Pilot (marketing site)

Static site deployed with [GitHub Pages](https://pages.github.com/).

## Live site & deployment repo

| | URL |
|---|---|
| **Live site (GitHub Pages)** | https://vmaccarone22.github.io/statement-shield-web/ |
| **GitHub repo (push here to publish)** | https://github.com/vmaccarone22/statement-shield-web |

This folder is also copied in the [fundpilot-windows](https://github.com/vmaccarone22/fundpilot-windows) monorepo as `Fund-Pilot-Website/` for local dev alongside the Windows app. **Production deploys** come from `statement-shield-web` — push there after you edit files here (or sync both).

## Enable / check GitHub Pages

1. Open https://github.com/vmaccarone22/statement-shield-web → **Settings → Pages**.
2. **Build and deployment**: Source = **Deploy from a branch**.
3. **Branch**: `main`, folder **`/ (root)`**, Save.

## Edit the site

| Where | How |
|--------|-----|
| This PC | Change files in this folder, commit, push to `statement-shield-web`. |
| GitHub | Open a file in the repo → **Edit** (pencil) → commit. |
| Cursor / VS Code | Same as local: edit, Source Control, push. |

The server only serves what is in the repo; there is no WordPress-style admin panel.

## Local preview & verify

Use `Serve-Local.bat` or `Serve-Local.ps1` (Python on `127.0.0.1:8080`).

Run `Build-Site.ps1` to verify required HTML/CSS/JS/assets exist (no compile step — static site).

## First-time push (new machine)

```powershell
cd path\to\Fund-Pilot-Website
git init
git add .
git commit -m "Fund Pilot marketing site"
git branch -M main
git remote add origin https://github.com/vmaccarone22/statement-shield-web.git
git push -u origin main
```

Then confirm Pages is enabled in repo settings (see above).
