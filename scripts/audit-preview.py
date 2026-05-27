"""Capture each scroll-step of website-apple for visual QA."""
from __future__ import annotations

import os

BASE = os.environ.get("FP_PREVIEW_URL", "http://127.0.0.1:8081/")
OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "review-captures")
OUT_MOBILE = os.path.join(OUT, "mobile")

SECTIONS = [
    ("hero", "#top", None),
    ("platform", "#desk", 3),
    ("analyze", "#analyze", 3),
    ("crm", "#crm", 3),
    ("pilot", "#pilot", 3),
    ("dialer", "#dialer", 3),
    ("leads", "#leads", 3),
    ("plans", "#plans", None),
]


def set_scroll_step(page, section_sel: str, step: int) -> None:
    page.evaluate(
        """([sel, step]) => {
          const root = document.querySelector(sel);
          if (!root) return;
          root.querySelectorAll('.story-step').forEach((el, i) => {
            const on = i === step;
            el.classList.toggle('is-active', on);
            el.style.opacity = on ? '1' : '0';
            el.style.visibility = on ? 'visible' : 'hidden';
          });
          root.querySelectorAll('.story-media').forEach((el, i) => {
            const on = i === step;
            el.classList.toggle('is-active', on);
            el.style.opacity = on ? '1' : '0';
          });
        }""",
        [section_sel, step],
    )


def capture_sections(page, out_dir: str) -> None:
    page.locator("#top").scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(out_dir, "hero.png"))

    for name, sel, steps in SECTIONS:
        if sel == "#top":
            continue
        page.locator(sel).scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        if steps:
            for i in range(steps):
                set_scroll_step(page, sel, i)
                page.wait_for_timeout(450)
                page.locator(f"{sel} .scroll-story-pin").screenshot(
                    path=os.path.join(out_dir, f"{name}-step{i + 1}.png")
                )
        else:
            page.screenshot(path=os.path.join(out_dir, f"{name}.png"))


def main() -> None:
    from playwright.sync_api import sync_playwright

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(OUT_MOBILE, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(BASE, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(600)
        capture_sections(page, OUT)

        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(BASE, wait_until="networkidle", timeout=90000)
        mobile.wait_for_timeout(600)
        capture_sections(mobile, OUT_MOBILE)

        browser.close()

    print(f"Saved desktop audit captures to {OUT}")
    print(f"Saved mobile audit captures to {OUT_MOBILE}")


if __name__ == "__main__":
    main()
