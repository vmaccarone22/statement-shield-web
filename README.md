# Fund Pilot marketing website

Public marketing site for Fund Pilot — scroll-driven product story with real desktop UI screenshots.

## Preview locally

```powershell
cd FundPilot\website
.\Serve-Local.ps1
```

Open **http://127.0.0.1:8081**

## Publish live (GitHub Pages)

```powershell
cd FundPilot
powershell -File scripts\Sync-Website-To-GitHub.ps1
```

## Publish VPS preview

```powershell
py -3 scripts\publish_website.py
```

Requires `FP_VPS_PASSWORD`. Serves at `https://crm.fundpilot.xyz/preview/`.

## QA captures

```powershell
cd FundPilot\website
py -3 scripts\audit-preview.py
```

Screenshots land in `review-captures/` (desktop + `mobile/`).
