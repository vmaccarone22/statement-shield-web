# Fund Pilot — cinematic scroll site

Apple-style **scroll motion** on **real Fund Pilot UI** — demo videos and screenshots from the actual desktop/mobile app, not placeholder 3D props.

The original 3D marketing site lives in `../website/`.

## Preview on VPS (partner link)

After changes, publish to the cloud:

```powershell
# From FundPilot repo root — requires FP_VPS_PASSWORD
py -3 scripts\publish_website_apple.py
```

Partner URL:

- **http://172.86.108.65/preview/**
- **https://crm.fundpilot.xyz/preview/**

Local dev remains **http://127.0.0.1:8081** via `Serve-Local.ps1`.

## Preview locally

```powershell
.\Serve-Local.ps1
```

Open **http://127.0.0.1:8081**

## What you see

- **Hero:** gold Saturn ambient 3D + laptop/phone device frames playing real analyze demo
- **Scroll sections:** as you scroll, copy steps through and the **real screenshot or demo video** crossfades (analyze, CRM, Pilot, dialer, leads)
- **3D is atmosphere only** — not used to represent product features

## Media source

Demo MP4s and PNGs come from `../website/assets/` (junction). Re-record or replace there, then refresh the site.

To add a new scroll step: duplicate a `<figure class="story-media">` in `index.html` and match the step count in `.story-step`.

## Structure

| File | Purpose |
|------|---------|
| `index.html` | Scroll stories with real app media per step |
| `css/apple.css` | Fund Pilot brand + scroll layout |
| `js/scroll-story.js` | Scroll-pinned copy + screenshot/video swap |
| `js/hero-3d.js` | Ambient hero rings (not product) |
| `js/device-3d.js` | Device tilt + parallax |
| `js/apple-scroll.js` | Nav, lazy video, forms |
