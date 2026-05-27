"""Capture browser-rendered EXE-style demo screens for the Apple marketing site."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "marketing"
DEMO = (ROOT / "demo-ui" / "index.html").resolve()

SCREENS = [
    ("features-overview", "features-overview.png", 1440, 900),
    ("command-center", "command-center.png", 1440, 900),
    ("broker-floor", "broker-floor.png", 1440, 900),
    ("crm-deal-board", "crm-deal-board.png", 1440, 900),
    ("crm-deal-detail", "crm-deal-detail.png", 1440, 900),
    ("analyze-files", "analyze-files.png", 1440, 900),
    ("merchant-checks", "merchant-checks.png", 1440, 900),
    ("crm-dashboard", "crm-dashboard.png", 1440, 900),
    ("crm-activity", "crm-activity.png", 1440, 900),
    ("dialer-campaign", "dialer-campaign.png", 1440, 900),
    ("pilot-desk", "pilot-desk.png", 1440, 900),
    ("pilot-bot", "pilot-bot.png", 420, 620),
    ("lead-hunter", "lead-hunter.png", 1440, 900),
    ("admin-import", "admin-import.png", 1440, 900),
    ("ops-distribution", "ops-distribution.png", 1440, 900),
]


def main() -> None:
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for screen, filename, width, height in SCREENS:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            page.goto(f"{DEMO.as_uri()}?screen={screen}", wait_until="networkidle")
            page.locator("#appWindow").screenshot(path=str(OUT / filename))
            page.close()
            print(f"OK {filename}")
        browser.close()


if __name__ == "__main__":
    main()
