# Website preview QA

**Local:** http://127.0.0.1:8081

## Audit captures

```powershell
cd FundPilot\website
py -3 scripts\audit-preview.py
```

Screenshots land in `review-captures/` (desktop + `mobile/`).

## Regenerate marketing screenshots

```powershell
py -3 scripts\capture-demo-ui.py
```

## Publish

- **GitHub Pages:** `powershell -File scripts\Sync-Website-To-GitHub.ps1` from repo root
- **VPS preview:** `py -3 scripts\publish_website.py`
