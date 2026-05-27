# Website preview QA (marketing site only)

**Live:** http://172.86.108.65/preview/  
**Local:** http://127.0.0.1:8081

## How we audit

```powershell
cd FundPilot\website-apple
py -3 scripts\audit-preview.py
```

Screenshots land in `review-captures/` — open those after every content change.

Regenerate sanitized app shots (no app code touched):

```powershell
py -3 ..\scripts\sanitize_marketing_screenshots.py
py -3 ..\scripts\publish_website_apple.py   # needs FP_VPS_PASSWORD
```

## Marketing story (aligned with your other session)

| Section | Sell this | Screenshot |
|---------|-----------|------------|
| Hero | Whole MCA desk in one app | `features-overview.png` |
| Platform | One login · command center · Pilot on desk | features → command-center → pilot-desk |
| Analyze | Statement PDFs → score (video until analyze shot exists) | demo video |
| CRM | Deal board → dashboard → activity log | crm-deal-board → crm-dashboard → crm-activity |
| Pilot | Voice desk → Pilot Drop modal → Lead Hunter page | pilot-desk → pilot-bot → lead-hunter |
| Dialer | Call on card → logged activity → trace-to-dial | deal board → activity → pilot-desk |
| Plans | Pricing tiers | — |

**Rules from your sessions:** real Fund Pilot UI only (no random 3D props), Fund Pilot gold/dark brand, Apple-style scroll + one headline per step, PII blurred on marketing PNGs.

## Fixes applied (May 26)

- Removed aggressive sidebar crop that cut off UI
- Fixed wrong asset: dashboard was labeled as command center
- Full-window screenshots with `object-fit: contain` (not cropped by frame)
- Sharper scroll copy (no overlapping step text)
- Dimmed 3D background behind real screenshots
- Blur: sidebar user, merchant rows, emails, “Good day” greeting, footer paths

## Still needed from you (optional)

- **Analyze tab** screenshot or short screen recording for the Analyze scroll section
- **Dialer campaign** screen if different from deal-board Call buttons
