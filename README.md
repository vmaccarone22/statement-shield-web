# Fund Pilot (marketing site)

Static site — **private repo**, not published to public GitHub Pages.

## Repo (private, invite-only)

https://github.com/vmaccarone22/statement-shield-web

Only people you add under **Settings → Collaborators** can see or clone this repo. There is no public live URL while Pages is disabled.

This folder is also in the [fundpilot-windows](https://github.com/vmaccarone22/fundpilot-windows) monorepo as `Fund-Pilot-Website/` for local dev next to the Windows app.

## Local preview

```powershell
py -3 serve_local.py
# or: .\Serve-Local.ps1
```

Opens at `http://127.0.0.1:8080` on your PC only.

Run `Build-Site.ps1` to verify required HTML/CSS/JS/assets exist.

## If you want a private live site later

- **GitHub Pro** (~$4/mo): private repo + **private GitHub Pages** (only repo collaborators can view).
- **Netlify / Vercel / Cloudflare**: password or SSO in front of the site.
- **Custom domain** with access control on your host.

Do not re-enable public GitHub Pages unless you intend for the whole internet to see the site.

## Edit the site

| Where | How |
|--------|-----|
| This PC | Edit files, commit, push to `statement-shield-web` (requires collaborator access). |
| Cursor | Same — Source Control → push. |

## First-time clone (partner)

```powershell
git clone https://github.com/vmaccarone22/statement-shield-web.git
```

They must be invited to the repo first.
