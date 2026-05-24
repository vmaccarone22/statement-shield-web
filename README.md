# Fund Pilot marketing site

Static marketing site for **Fund Pilot** — MCA analyzer, native CRM, Twilio dialer.

**Source of truth:** `FundPilot/website/` in the private [fundpilot](https://github.com/vmaccarone22/fundpilot) monorepo.

**Public deploy repo (legacy name):** [statement-shield-web](https://github.com/vmaccarone22/statement-shield-web) — sync from this folder before pushing live.

## Local preview

```powershell
cd website
py -3 serve_local.py
# or: .\Serve-Local.ps1
```

Opens at http://127.0.0.1:8080

## What’s on the site (2026-05-24)

- Native in-exe CRM, deal board, merchants
- Fund Pilot Dialer (Twilio, campaigns, Ops admin)
- Four pricing tiers: Core, Core + CRM, CRM + Dialer, Enterprise
- SEO: meta keywords, Open Graph, Twitter cards, JSON-LD SoftwareApplication + Organization
- FAQ entries for CRM and dialer

## Before public launch

1. Replace `fundpilot.example` in `index.html`, `sitemap.xml`, `robots.txt`
2. Set contact email in `js/main.js` (`CONTACT_EMAIL`)
3. Run `Build-Site.ps1` to verify assets
4. Sync to `statement-shield-web` and enable GitHub Pages (or Netlify/Cloudflare)

## Sync to statement-shield-web

```powershell
# From FundPilot repo root — copy site files to a clone of statement-shield-web, then commit there
powershell -ExecutionPolicy Bypass -File scripts\Sync-Website-To-GitHub.ps1
```
