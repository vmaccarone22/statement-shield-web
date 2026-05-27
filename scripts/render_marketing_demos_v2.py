# -*- coding: utf-8 -*-
"""
Fund Pilot — 2026 marketing demo renders (current Command center, Pilot bot, dialer, leads).

Run: py -3 website/scripts/render_marketing_demos_v2.py
Requires: pip install numpy pillow imageio imageio-ffmpeg
"""
from __future__ import annotations

import math
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W, H = 1920, 1088
FPS = 24

# Current Fund Pilot dark theme (desktop + CRM)
BG = (14, 14, 18)
SURFACE = (20, 20, 26)
SURFACE2 = (28, 28, 36)
CARD = (20, 20, 26)
INPUT = (28, 28, 34)
BORDER = (45, 45, 53)
ACCENT = (212, 175, 115)
ACCENT_SOFT = (232, 213, 168)
TEXT = (243, 241, 237)
DIM = (150, 147, 158)
GREEN = (142, 182, 155)
GREEN_BTN = (90, 125, 98)
RED = (201, 123, 123)
ORANGE = (212, 160, 90)
WHITE = (255, 255, 255)
BTN_ON = (20, 17, 12)
BOT_FACE = (255, 245, 230)

WIN_REG = "C:/Windows/Fonts/segoeui.ttf"
WIN_SEMI = "C:/Windows/Fonts/segoeuib.ttf"


def _font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _tw(font, text: str) -> float:
    if hasattr(font, "getlength"):
        return float(font.getlength(text))
    return float(font.getsize(text)[0])


def _ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * _ease(t)


def bg() -> np.ndarray:
    y = np.linspace(0, 1, H, dtype=np.float32)
    r = 10 * (1 - y) + 14 * y
    g = 10 * (1 - y) + 14 * y
    b = 12 * (1 - y) + 18 * y
    base = np.stack([r, g, b], axis=-1)
    base = np.tile(base[:, None, :], (1, W, 1)).astype(np.float32)
    yy, xx = np.ogrid[:H, :W]
    glow = np.exp(-((xx - W / 2) ** 2 + (yy - H * 0.35) ** 2) / (W * 0.55) ** 2).astype(np.float32)
    base += np.stack([glow * 22, glow * 16, glow * 6], axis=-1)
    return np.clip(base, 0, 255).astype(np.uint8)


def rr(d, xy, r, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def cursor(d, x, y, click=0.0, scale=1.0):
    s = scale * (1 + 0.1 * click)
    pts = [(x, y), (x + 6 * s, y + 18 * s), (x + 14 * s, y + 14 * s)]
    d.polygon(pts, fill=(248, 248, 252), outline=(50, 50, 58))
    if click > 0.15:
        r = int((10 + 20 * click) * scale)
        d.ellipse((x - r, y - r, x + r, y + r), outline=(*ACCENT, int(120 * click)), width=3)


def shell(d, title="Fund Pilot"):
    wx0, wy0, wx1, wy1 = 48, 32, W - 48, H - 28
    rr(d, (wx0, wy0, wx1, wy1), 14, CARD)
    rr(d, (wx0, wy0, wx1, wy0 + 52), 10, SURFACE2)
    for i, c in enumerate((RED, ACCENT, GREEN)):
        d.ellipse((wx0 + 18 + i * 20, wy0 + 18, wx0 + 32 + i * 20, wy0 + 32), fill=c)
    d.text((wx0 + 72, wy0 + 14), title, fill=DIM, font=_font(WIN_SEMI, 20))
    return wx0, wy0, wx1, wy1


def top_nav(d, wx0, wy0, wx1, active="Home"):
    iy = wy0 + 68
    ix = wx0 + 24
    d.text((ix, iy), "F", fill=BTN_ON, font=_font(WIN_SEMI, 22))
    rr(d, (ix, iy, ix + 28, iy + 28), 8, ACCENT)
    d.text((ix + 6, iy + 2), "F", fill=BTN_ON, font=_font(WIN_SEMI, 18))
    ix += 40
    for label in ("Home", "Features"):
        on = label == active
        d.text((ix, iy + 4), label, fill=ACCENT if on else DIM, font=_font(WIN_SEMI, 22 if on else 20))
        ix += 100
    rx = wx1 - 24
    for label, style in (
        ("Analyze", "green"),
        ("Workspace", "ghost"),
        ("Call", "sec"),
        ("CRM", "pri"),
        ("App builder", "ghost"),
    ):
        fw = int(_tw(_font(WIN_SEMI, 18), label) + 28)
        rx -= fw + 8
        bg_c = GREEN_BTN if style == "green" else ACCENT if style == "pri" else SURFACE2
        fg = BTN_ON if style in ("green", "pri") else TEXT
        rr(d, (rx, iy - 2, rx + fw, iy + 30), 999, bg_c)
        d.text((rx + 14, iy + 4), label, fill=fg, font=_font(WIN_SEMI, 18))
    return wy0 + 110


def draw_bot(d, cx, cy, size=56, pulse=0.0):
    r = size // 2
    glow = int(40 + 30 * pulse)
    d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=(212, 175, 115, glow))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BOT_FACE, outline=ACCENT, width=2)
    d.rectangle((cx - 2, cy - r - 10, cx + 2, cy - r - 2), fill=ACCENT)
    d.ellipse((cx - 4, cy - r - 14, cx + 4, cy - r - 6), fill=ACCENT)
    eye_y = cy - 6
    d.ellipse((cx - 14, eye_y, cx - 6, eye_y + 10), fill=BTN_ON)
    d.ellipse((cx + 6, eye_y, cx + 14, eye_y + 10), fill=BTN_ON)
    d.arc((cx - 12, cy + 2, cx + 12, cy + 16), 10, 170, fill=BTN_ON, width=3)


def assistant_panel(d, x0, y0, w, h, msgs, suggest=None, typed="", pulse=0.0):
    rr(d, (x0, y0, x0 + w, y0 + h), 18, CARD, BORDER, 2)
    rr(d, (x0, y0, x0 + w, y0 + 58), 14, INPUT)
    draw_bot(d, x0 + 36, y0 + 30, 40, pulse)
    d.text((x0 + 68, y0 + 14), "Fund Pilot Bot", fill=ACCENT, font=_font(WIN_SEMI, 20))
    d.text((x0 + 68, y0 + 34), "Lead Hunter · CRM · tracers", fill=DIM, font=_font(WIN_REG, 14))
    my = y0 + 72
    for role, text in msgs:
        mw = w - 48
        lines = text.split("\n")
        lh = 22
        box_h = len(lines) * lh + 20
        if role == "user":
            bx0 = x0 + w - mw - 16
            rr(d, (bx0, my, x0 + w - 16, my + box_h), 12, ACCENT)
            fg = BTN_ON
        else:
            bx0 = x0 + 16
            rr(d, (bx0, my, bx0 + mw, my + box_h), 12, INPUT, BORDER, 1)
            fg = TEXT
        for i, ln in enumerate(lines):
            d.text((bx0 + 12, my + 10 + i * lh), ln, fill=fg, font=_font(WIN_REG, 16))
        my += box_h + 12
    if suggest:
        sx = x0 + 16
        for s in suggest:
            sw = int(_tw(_font(WIN_SEMI, 14), s) + 24)
            rr(d, (sx, my, sx + sw, my + 32), 16, CARD, ACCENT, 1)
            d.text((sx + 12, my + 8), s, fill=ACCENT, font=_font(WIN_SEMI, 14))
            sx += sw + 8
        my += 44
    inp_y = y0 + h - 52
    rr(d, (x0 + 12, inp_y, x0 + w - 90, inp_y + 40), 10, INPUT, BORDER, 1)
    ph = typed or "Gatekeeper blocked? Paste phone + business…"
    d.text((x0 + 24, inp_y + 10), ph, fill=TEXT if typed else DIM, font=_font(WIN_REG, 15))
    rr(d, (x0 + w - 78, inp_y, x0 + w - 12, inp_y + 40), 10, ACCENT)
    d.text((x0 + w - 62, inp_y + 10), "Send", fill=BTN_ON, font=_font(WIN_SEMI, 16))


# ─── Story 1: Analyze + positions + DataMerch ───────────────────────────────

def story_analyze(frame_i: int, n: int) -> np.ndarray:
    t = frame_i / max(1, n - 1)
    img = Image.fromarray(bg()).convert("RGBA")
    d = ImageDraw.Draw(img)
    wx0, wy0, wx1, wy1 = shell(d, "Fund Pilot — MCA Analyzer")
    content_top = top_nav(d, wx0, wy0, wx1, "Home")

    if t < 0.22:
        u = t / 0.22
        d.text((wx0 + 40, content_top + 8), "Command center", fill=TEXT, font=_font(WIN_SEMI, 44))
        d.text(
            (wx0 + 40, content_top + 62),
            "Search merchants, analyze locally, and jump to CRM, dialer, or Pilot.",
            fill=DIM,
            font=_font(WIN_REG, 22),
        )
        rr(d, (wx0 + 40, content_top + 110, wx1 - 40, content_top + 168), 12, SURFACE2, BORDER, 1)
        d.text((wx0 + 60, content_top + 132), "Summit Trucking LLC", fill=TEXT, font=_font(WIN_REG, 22))
        rr(d, (wx1 - 320, content_top + 118, wx1 - 60, content_top + 160), 10, ACCENT)
        d.text((wx1 - 290, content_top + 128), "Analyze", fill=BTN_ON, font=_font(WIN_SEMI, 20))
        if u > 0.35:
            rr(d, (W // 2 - 420, H // 2 - 200, W // 2 + 420, H // 2 + 200), 20, SURFACE, ACCENT, 2)
            d.text((W // 2 - 380, H // 2 - 160), "Pick four statement months", fill=ACCENT_SOFT, font=_font(WIN_SEMI, 36))
            for i, m in enumerate(["Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026"]):
                show = u > 0.4 + i * 0.08
                if show:
                    d.text((W // 2 - 360, H // 2 - 80 + i * 52), f"✓  {m}  ·  bank_statement.pdf", fill=GREEN, font=_font(WIN_REG, 24))
            if u > 0.85:
                cursor(d, W // 2 + 300, H // 2 + 140, click=max(0, 1 - abs(u - 0.92) * 20), scale=1.6)

    elif t < 0.38:
        u = (t - 0.22) / 0.16
        cx0, cy0, cx1, cy1 = wx0 + 20, content_top, wx1 - 20, wy1 - 20
        rr(d, (cx0, cy0, cx1, cy1), 16, SURFACE)
        d.text((W // 2 - 120, cy0 + 80), "Analyzing…", fill=ACCENT_SOFT, font=_font(WIN_SEMI, 56))
        d.text((W // 2 - 280, cy0 + 160), "Scanning deposits · weekly positions · DataMerch · score", fill=DIM, font=_font(WIN_REG, 24))
        bx0, bx1 = W // 2 - 400, W // 2 + 400
        by = cy0 + 240
        rr(d, (bx0, by, bx1, by + 28), 8, BORDER)
        prog = _lerp(0.15, 0.95, u)
        rr(d, (bx0, by, int(bx0 + (bx1 - bx0) * prog), by + 28), 8, ACCENT)

    else:
        u = (t - 0.38) / 0.62
        al = int(255 * min(1, u * 1.5))
        bx0, by0, bx1, by1 = wx0 + 16, content_top - 10, wx1 - 16, wy1 - 16
        rr(d, (bx0, by0, bx1, by1), 18, SURFACE, (*ACCENT, 80), 2)
        d.text((bx0 + 40, by0 + 24), "SUMMIT TRUCKING LLC", fill=(*TEXT, al), font=_font(WIN_SEMI, 40))
        d.text((bx0 + 40, by0 + 80), "Estimated funding range", fill=(*DIM, al), font=_font(WIN_REG, 22))
        d.text((bx0 + 40, by0 + 112), "$85,000  —  $140,000", fill=(*ACCENT, al), font=_font(WIN_SEMI, 44))
        d.text((bx0 + 40, by0 + 178), "Approval score  7.5 / 10", fill=(*GREEN, al), font=_font(WIN_SEMI, 32))

        dm_clear = u < 0.55
        if dm_clear:
            rr(d, (bx0 + 36, by0 + 230, bx1 - 36, by0 + 278), 12, (24, 32, 28), (*GREEN, 100), 2)
            d.text((bx0 + 52, by0 + 246), "DataMerch: CLEAR — no default · no judgment on file", fill=(*GREEN, al), font=_font(WIN_SEMI, 22))
        else:
            rr(d, (bx0 + 36, by0 + 230, bx1 - 36, by0 + 278), 12, (48, 28, 28), (*RED, 120), 2)
            d.text((bx0 + 52, by0 + 246), "DataMerch: DEFAULT DETECTED — confirm payoff before shopping", fill=(*RED, al), font=_font(WIN_SEMI, 22))

        split = W // 2
        ty = by0 + 300
        d.text((bx0 + 40, ty), "Weekly pay positions (funded)", fill=(*ACCENT, al), font=_font(WIN_SEMI, 24))
        for i, ln in enumerate(
            [
                "Forward     $2,850/wk   rem $42.5k",
                "Greenbox    $2,100/wk   rem $38.2k",
                "Harbor      $1,675/wk   rem $29.9k",
                "Northline   $1,240/wk   rem $24.0k",
            ]
        ):
            show = u > 0.2 + i * 0.08
            if show:
                d.text((bx0 + 48, ty + 36 + i * 34), ln, fill=(*TEXT, al), font=_font(WIN_REG, 20))
        d.text((split + 20, ty), "Cash flow — 4 months net", fill=(*ACCENT, al), font=_font(WIN_SEMI, 24))
        for i, ln in enumerate(["Mar 2026  +$38,905", "Feb 2026  +$31,240", "Jan 2026  +$35,180", "Dec 2025  +$33,050"]):
            show = u > 0.25 + i * 0.07
            if show:
                d.text((split + 28, ty + 36 + i * 34), ln, fill=(*GREEN, al), font=_font(WIN_REG, 20))

        if u > 0.75:
            pulse = 0.5 + 0.5 * math.sin(frame_i * 0.2)
            draw_bot(d, wx1 - 90, wy1 - 90, 52, pulse)

    return np.array(img.convert("RGB"))


# ─── Story 2: Fund Pilot Bot / voice workflow ───────────────────────────────

def story_assistant(frame_i: int, n: int) -> np.ndarray:
    t = frame_i / max(1, n - 1)
    img = Image.fromarray(bg()).convert("RGBA")
    d = ImageDraw.Draw(img)
    wx0, wy0, wx1, wy1 = shell(d, "Fund Pilot — CRM")
    content_top = top_nav(d, wx0, wy0, wx1, "Home")

    d.text((wx0 + 40, content_top + 4), "Summit Trucking LLC", fill=TEXT, font=_font(WIN_SEMI, 36))
    d.text((wx0 + 40, content_top + 50), "Owner: James Rivera  ·  Gate: (718) 555-0142", fill=DIM, font=_font(WIN_REG, 20))
    rr(d, (wx0 + 40, content_top + 90, wx1 - 420, content_top + 340), 14, SURFACE2, BORDER, 1)
    d.text((wx0 + 60, content_top + 110), "Activity · Email · SMS · Files", fill=ACCENT, font=_font(WIN_SEMI, 18))
    d.text((wx0 + 60, content_top + 150), "Last touch: gatekeeper — need owner cell", fill=DIM, font=_font(WIN_REG, 18))

    px, py, pw, ph = wx1 - 390, wy0 + 100, 360, 520
    pulse = 0.5 + 0.5 * math.sin(frame_i * 0.15)

    user_q = "Hey Pilot — find Summit Trucking's cell phone number"
    typed = user_q[: int(len(user_q) * min(1, max(0, (t - 0.18) / 0.14)))]

    msgs = []
    if t > 0.05:
        msgs.append(("bot", "Hey — I'm your Fund Pilot copilot.\nGatekeeper blocked? I'll trace the owner cell."))
    if t > 0.32:
        msgs.append(("user", user_q if t > 0.32 else typed))
    if t > 0.48:
        msgs.append(
            (
                "bot",
                "Found owner cell for Summit Trucking LLC:\n\n"
                "📱  (917) 555-8821  ·  James Rivera\n"
                "Source: Lead Hunter trace · high confidence",
            )
        )
    suggest = None
    if t > 0.62:
        suggest = ["Call merchant", "Open in CRM", "Send SMS"]
    if t > 0.78:
        rr(d, (wx0 + 40, wy1 - 100, wx0 + 340, wy1 - 48), 12, GREEN_BTN)
        d.text((wx0 + 70, wy1 - 82), "Opening dialer with (917) 555-8821…", fill=WHITE, font=_font(WIN_SEMI, 18))

    assistant_panel(d, px, py, pw, ph, msgs, suggest=suggest, typed=typed if t < 0.32 else "", pulse=pulse)
    draw_bot(d, wx1 - 70, wy1 - 70, 48, pulse)

    if 0.72 < t < 0.88:
        cursor(d, px + pw - 100, py + ph - 30, click=max(0, 1 - abs(t - 0.8) * 15), scale=1.5)

    return np.array(img.convert("RGB"))


# ─── Story 3: Dialer + campaign ───────────────────────────────────────────

def story_dialer(frame_i: int, n: int) -> np.ndarray:
    t = frame_i / max(1, n - 1)
    img = Image.fromarray(bg()).convert("RGBA")
    d = ImageDraw.Draw(img)
    wx0, wy0, wx1, wy1 = shell(d, "Fund Pilot — Call")
    top_nav(d, wx0, wy0, wx1)

    nav_w = 220
    rr(d, (wx0 + 16, wy0 + 100, wx0 + 16 + nav_w, wy1 - 16), 12, CARD, BORDER, 1)
    d.text((wx0 + 36, wy0 + 120), "Fund Pilot", fill=ACCENT, font=_font(WIN_SEMI, 20))
    d.text((wx0 + 36, wy0 + 146), "Dialer", fill=DIM, font=_font(WIN_REG, 14))
    rr(d, (wx0 + 28, wy0 + 190, wx0 + nav_w, wy0 + 230), 8, ACCENT)
    d.text((wx0 + 44, wy0 + 200), "Dial pad", fill=BTN_ON, font=_font(WIN_SEMI, 18))

    cx = wx0 + nav_w + 48
    d.text((cx, wy0 + 120), "Click-to-call & SMS", fill=TEXT, font=_font(WIN_SEMI, 36))
    d.text((cx, wy0 + 168), "Fund Pilot Dialer · local caller ID · campaigns", fill=DIM, font=_font(WIN_REG, 18))

    rr(d, (cx, wy0 + 200, wx1 - 40, wy0 + 248), 10, CARD, BORDER, 1)
    status = "Dialer ready · Caller ID (212) 555-0199"
    if t > 0.55:
        secs = int((t - 0.55) / 0.45 * 47)
        status = f"Connected · {secs // 60:01d}:{secs % 60:02d}  ·  Metro HVAC Services"
    d.text((cx + 16, wy0 + 214), status, fill=GREEN if t > 0.55 else TEXT, font=_font(WIN_REG, 20))

    d.text((cx, wy0 + 268), "Campaign", fill=DIM, font=_font(WIN_REG, 16))
    camp = "MCA Outbound — Frank Romano (24 new)"
    rr(d, (cx, wy0 + 292, wx1 - 40, wy0 + 336), 10, INPUT, BORDER, 1)
    d.text((cx + 14, wy0 + 304), camp, fill=TEXT, font=_font(WIN_REG, 20))

    phone = "(646) 555-3309"
    if t < 0.2:
        phone = ""
    elif t < 0.35:
        phone = "(646) 555-"
    lead = "Metro HVAC Services · Maria Santos" if t > 0.28 else ""
    d.text((cx, wy0 + 352), lead, fill=GREEN, font=_font(WIN_SEMI, 18))

    rr(d, (cx, wy0 + 382, wx1 - 40, wy0 + 450), 12, INPUT, BORDER, 1)
    d.text((cx + 20, wy0 + 400), phone, fill=TEXT, font=_font(WIN_SEMI, 40))

    bx = cx
    for label, col, on in (
        ("Next lead", SURFACE2, t > 0.12 and t < 0.28),
        ("Call", GREEN_BTN, t > 0.38 and t < 0.55),
        ("SMS", SURFACE2, False),
    ):
        fw = 140
        rr(d, (bx, wy0 + 470, bx + fw, wy0 + 520), 12, ACCENT if on else col)
        d.text((bx + 28, wy0 + 484), label, fill=BTN_ON if on else TEXT, font=_font(WIN_SEMI, 20))
        bx += fw + 12

    if t > 0.68:
        d.text((cx, wy0 + 540), "Disposition", fill=DIM, font=_font(WIN_REG, 16))
        dx = cx
        for disp in ("Contacted", "Voicemail", "No answer", "Callback"):
            sel = disp == "Contacted" and t > 0.82
            dw = int(_tw(_font(WIN_SEMI, 16), disp) + 28)
            rr(d, (dx, wy0 + 564, dx + dw, wy0 + 598), 10, ACCENT if sel else SURFACE2, ACCENT if sel else BORDER, 1)
            d.text((dx + 14, wy0 + 574), disp, fill=BTN_ON if sel else TEXT, font=_font(WIN_SEMI, 16))
            dx += dw + 10

    if 0.22 < t < 0.32:
        cursor(d, cx + 80, wy0 + 500, click=max(0, 1 - abs(t - 0.27) * 20), scale=1.5)
    if 0.42 < t < 0.52:
        cursor(d, cx + 70, wy0 + 494, click=max(0, 1 - abs(t - 0.47) * 20), scale=1.5)

    return np.array(img.convert("RGB"))


# ─── Story 4: In-app lead purchase ────────────────────────────────────────

def story_leads(frame_i: int, n: int) -> np.ndarray:
    t = frame_i / max(1, n - 1)
    img = Image.fromarray(bg()).convert("RGBA")
    d = ImageDraw.Draw(img)
    wx0, wy0, wx1, wy1 = shell(d, "Fund Pilot — Lead marketplace")
    top_nav(d, wx0, wy0, wx1)

    cx = wx0 + 32
    d.text((cx, wy0 + 118), "Fresh MCA leads · AI scored", fill=TEXT, font=_font(WIN_SEMI, 38))
    d.text((cx, wy0 + 168), "Buy inside Fund Pilot — one click to your dialer queue", fill=DIM, font=_font(WIN_REG, 20))

    cards = [
        ("Metro HVAC Services", "$142K avg dep", "Score 94", "$12"),
        ("Brightline Logistics", "$210K avg dep", "Score 91", "$14"),
        ("Prime Dental Group", "$54K avg dep", "Score 88", "$9"),
    ]
    y = wy0 + 220
    for i, (name, dep, score, price) in enumerate(cards):
        reveal = t > 0.08 + i * 0.06
        if not reveal:
            continue
        sel = i == 0 and t > 0.45
        rr(d, (cx, y, wx1 - 32, y + 110), 16, SURFACE if not sel else (32, 28, 22), ACCENT if sel else BORDER, 2 if sel else 1)
        d.text((cx + 24, y + 18), name, fill=TEXT, font=_font(WIN_SEMI, 26))
        d.text((cx + 24, y + 54), dep, fill=DIM, font=_font(WIN_REG, 18))
        d.text((cx + 24, y + 80), score, fill=GREEN, font=_font(WIN_SEMI, 18))
        rr(d, (wx1 - 200, y + 28, wx1 - 52, y + 82), 12, ACCENT if sel else GREEN_BTN)
        lbl = "Added ✓" if sel and t > 0.72 else f"Add — {price}"
        d.text((wx1 - 178, y + 44), lbl, fill=BTN_ON, font=_font(WIN_SEMI, 18))
        y += 128

    if t > 0.75:
        rr(d, (cx, wy1 - 90, wx1 - 32, wy1 - 36), 14, (28, 36, 30), (*GREEN, 80), 2)
        d.text((cx + 20, wy1 - 72), "Lead queued → MCA Outbound — Frank Romano · Ready to dial", fill=GREEN, font=_font(WIN_SEMI, 22))

    if 0.5 < t < 0.65:
        cursor(d, wx1 - 120, wy0 + 280, click=max(0, 1 - abs(t - 0.58) * 18), scale=1.5)

    return np.array(img.convert("RGB"))


# ─── Story 5: 52-desk fleet / headsets / Pilot everywhere ─────────────────

def story_fleet(frame_i: int, n: int) -> np.ndarray:
    t = frame_i / max(1, n - 1)
    img = Image.fromarray(bg()).convert("RGBA")
    d = ImageDraw.Draw(img)

    d.text((W // 2 - 280, 48), "Fund Pilot live across your floor", fill=TEXT, font=_font(WIN_SEMI, 42))
    sub = "52 brokers · headsets on · Pilot on every desk"
    d.text((W // 2 - int(_tw(_font(WIN_REG, 22), sub) / 2), 104), sub, fill=ACCENT, font=_font(WIN_REG, 24))

    cols, rows = 13, 4
    gw = 130
    gh = 88
    gx0 = (W - cols * (gw + 8)) // 2
    gy0 = 160
    live = int(_lerp(8, 52, min(1, t * 1.4)))

    for i in range(min(52, cols * rows)):
        if i >= live:
            break
        c, r = i % cols, i // cols
        x = gx0 + c * (gw + 8)
        y = gy0 + r * (gh + 10)
        flicker = 0.4 + 0.6 * math.sin(frame_i * 0.08 + i * 0.7)
        rr(d, (x, y, x + gw, y + gh), 8, SURFACE2, BORDER, 1)
        rr(d, (x + 6, y + 6, x + gw - 6, y + 22), 4, INPUT)
        d.text((x + 10, y + 8), f"Desk {i + 1:02d}", fill=DIM, font=_font(WIN_REG, 11))
        on_call = (i + frame_i // 6) % 7 == 0 and t > 0.3
        if on_call:
            d.text((x + gw - 54, y + 8), "ON CALL", fill=GREEN, font=_font(WIN_SEMI, 10))
        draw_bot(d, x + gw - 24, y + gh - 20, 22, flicker * 0.5)
        if on_call:
            d.text((x + 10, y + 34), "🎧 Pilot", fill=ACCENT, font=_font(WIN_REG, 12))
            d.text((x + 10, y + 52), "Dialing…", fill=GREEN, font=_font(WIN_REG, 11))
        else:
            d.text((x + 10, y + 38), "CRM · Analyze", fill=DIM, font=_font(WIN_REG, 11))

    counter = f"{live} / 52 desks active"
    d.text((W // 2 - int(_tw(_font(WIN_SEMI, 28), counter) / 2), H - 80), counter, fill=GREEN, font=_font(WIN_SEMI, 28))

    if t > 0.55:
        rr(d, (W // 2 - 340, H - 160, W // 2 + 340, H - 110), 14, (32, 28, 20), ACCENT, 2)
        d.text(
            (W // 2 - 300, H - 148),
            '"Hey Pilot — find the merchant cell"  →  traced in 4 seconds',
            fill=ACCENT_SOFT,
            font=_font(WIN_REG, 20),
        )

    return np.array(img.convert("RGB"))


# ─── Showreel composer ────────────────────────────────────────────────────

def title_card(text: str, sub: str = "") -> np.ndarray:
    img = Image.fromarray(bg()).convert("RGBA")
    d = ImageDraw.Draw(img)
    draw_bot(d, W // 2, H // 2 - 80, 72, 0.5)
    d.text((W // 2 - _tw(_font(WIN_SEMI, 48), text) / 2, H // 2 + 20), text, fill=TEXT, font=_font(WIN_SEMI, 48))
    if sub:
        d.text((W // 2 - _tw(_font(WIN_REG, 24), sub) / 2, H // 2 + 84), sub, fill=ACCENT, font=_font(WIN_REG, 24))
    return np.array(img.convert("RGB"))


def crossfade(a: np.ndarray, b: np.ndarray, alpha: float) -> np.ndarray:
    return ((a.astype(np.float32) * (1 - alpha) + b.astype(np.float32) * alpha)).astype(np.uint8)


def build_showreel(segments: list[tuple[str, list[np.ndarray]]]) -> list[np.ndarray]:
    out: list[np.ndarray] = []
    title_f = 20
    xfade = 10
    for title, frames in segments:
        card = title_card(title)
        for _ in range(title_f):
            out.append(card)
        if out:
            for i in range(xfade):
                alpha = (i + 1) / xfade
                out[-xfade + i] = crossfade(out[-xfade + i], frames[0], alpha)
        out.extend(frames)
    end = title_card("Fund Pilot", "Plug in. Close.")
    for i in range(xfade):
        if out:
            out.append(crossfade(out[-1], end, (i + 1) / xfade))
    for _ in range(title_f):
        out.append(end)
    return out


def composite_cinema(ui_frame: np.ndarray, frame_i: int, n: int) -> np.ndarray:
    """Wrap UI frame in hyperrealistic desk + monitor composite with slow push-in."""
    t = frame_i / max(1, n - 1)
    y = np.linspace(0, 1, H, dtype=np.float32)
    wall = y
    desk = np.maximum(0.0, (y - 0.72) / 0.28)
    r = 8 + wall * 10 + desk * 6
    g = 8 + wall * 9 + desk * 5
    b = 10 + wall * 12 + desk * 4
    px = np.stack([r, g, b], axis=-1)
    px = np.tile(px[:, None, :], (1, W, 1))

    yy, xx = np.ogrid[:H, :W]
    lamp = np.exp(-((xx - W * 0.22) ** 2 + (yy - H * 0.55) ** 2) / (W * 0.35) ** 2).astype(np.float32)
    px[:, :, 0] += lamp * 28
    px[:, :, 1] += lamp * 18
    px[:, :, 2] += lamp * 6

    img = Image.fromarray(np.clip(px, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)

    push = 1.0 + 0.028 * _ease(min(1.0, t * 1.1))
    sw, sh = int(1560 * push), int(878 * push)
    mx = (W - sw) // 2
    my = int(56 + (1 - push) * 18)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((mx - 40, my + sh + 36, mx + sw + 40, my + sh + 100), fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)

    rr(d, (mx - 28, my - 28, mx + sw + 28, my + sh + 52), 20, (48, 48, 54), (90, 90, 98), 2)
    rr(d, (mx - 16, my - 16, mx + sw + 16, my + sh + 36), 14, (22, 22, 26))
    rr(d, (mx - 6, my - 6, mx + sw + 6, my + sh + 6), 8, (6, 6, 8))

    ui = Image.fromarray(ui_frame).resize((sw, sh), Image.Resampling.LANCZOS)
    img.paste(ui, (mx, my))

    glare = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.polygon([(0, 0), (int(sw * 0.55), 0), (0, int(sh * 0.62))], fill=(255, 255, 255, 32))
    img.paste(Image.alpha_composite(Image.new("RGBA", (sw, sh), (0, 0, 0, 0)), glare), (mx, my), glare)

    chin_w = int(sw * 0.22)
    cx = W // 2
    rr(d, (cx - chin_w // 2, my + sh + 8, cx + chin_w // 2, my + sh + 24), 6, (36, 36, 42))
    rr(d, (cx - chin_w, my + sh + 22, cx + chin_w, my + sh + 32), 4, (28, 28, 32))
    d.line([(0, my + sh + 48), (W, my + sh + 48)], fill=(32, 32, 38), width=2)

    bloom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    bd.ellipse((mx - 20, my + sh - 10, mx + sw + 20, my + sh + 70), fill=(212, 175, 115, 35))
    img = Image.alpha_composite(img.convert("RGBA"), bloom).convert("RGB")

    arr = np.array(img, dtype=np.float32)
    vig = np.exp(-((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / (W * 0.72) ** 2)
    arr *= 0.78 + 0.22 * vig[:, :, None]
    if frame_i % 3 == 0:
        grain = np.random.randint(-6, 7, (H, W, 3), dtype=np.int16)
        arr = np.clip(arr + grain, 0, 255)
    return arr.astype(np.uint8)


def cinematic_story(fn, frame_i: int, n: int) -> np.ndarray:
    return composite_cinema(fn(frame_i, n), frame_i, n)


def write_mp4(path: Path, frames, fps: int, crf: str = "20"):
    writer = imageio.get_writer(
        str(path),
        fps=fps,
        codec="libx264",
        pixelformat="yuv420p",
        ffmpeg_params=["-crf", crf, "-preset", "slow", "-movflags", "+faststart"],
    )
    try:
        for fr in frames:
            writer.append_data(fr)
    finally:
        writer.close()


def render_all():
    ASSETS.mkdir(parents=True, exist_ok=True)
    specs = [
        ("demo-desktop-analyze.mp4", story_analyze, int(22 * FPS)),
        ("demo-assistant-pilot.mp4", story_assistant, int(18 * FPS)),
        ("demo-dialer-campaign.mp4", story_dialer, int(14 * FPS)),
        ("demo-leads-purchase.mp4", story_leads, int(12 * FPS)),
        ("demo-fleet-live.mp4", story_fleet, int(10 * FPS)),
    ]
    segment_frames: list[tuple[str, list[np.ndarray]]] = []
    for name, fn, n in specs:
        path = ASSETS / name
        print(f"Rendering {name} ({n} frames)…")
        frames = [cinematic_story(fn, i, n) for i in range(n)]
        write_mp4(path, frames, FPS, "18")
        segment_frames.append((name.replace("demo-", "").replace(".mp4", "").replace("-", " ").title(), frames))

    print("Showreel…")
    show = build_showreel(segment_frames)
    write_mp4(ASSETS / "demo-showreel.mp4", show, FPS, "19")

    # Posters (cinematic stills)
    Image.fromarray(cinematic_story(story_analyze, int(22 * FPS * 0.82), int(22 * FPS))).save(
        ASSETS / "desktop-analyze-summary.png", optimize=True
    )
    Image.fromarray(cinematic_story(story_assistant, int(18 * FPS * 0.65), int(18 * FPS))).save(
        ASSETS / "poster-assistant-pilot.png", optimize=True
    )
    Image.fromarray(cinematic_story(story_dialer, int(14 * FPS * 0.6), int(14 * FPS))).save(
        ASSETS / "poster-dialer.png", optimize=True
    )
    Image.fromarray(cinematic_story(story_leads, int(12 * FPS * 0.7), int(12 * FPS))).save(
        ASSETS / "poster-leads.png", optimize=True
    )
    Image.fromarray(cinematic_story(story_fleet, int(10 * FPS * 0.75), int(10 * FPS))).save(
        ASSETS / "poster-fleet.png", optimize=True
    )
    print("Done.")


if __name__ == "__main__":
    render_all()
