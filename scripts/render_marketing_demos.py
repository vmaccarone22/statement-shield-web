# -*- coding: utf-8 -*-
"""
Fund Pilot — marketing demo MP4s (synthetic UI matching the Windows app).

Outputs:
  assets/demo-desktop-analyze.mp4 — Select files (4 months) → Analyzing… → big-picture summary (large type)
  assets/mobile-screenshot-calendar.png — planner mock still (1920×1088)
  assets/mobile-screenshot-notification.png — notification mock still (1920×1088)
  assets/iphone-followup-notification-demo.png — portrait lock-screen composite (750×1624, matches site <img> dimensions)

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

BG_TOP = (10, 10, 14)
BG_BOT = (14, 14, 18)
CARD_BG = (20, 20, 26)
CARD_BG2 = (14, 14, 18)
ACCENT = (212, 175, 115)
ACCENT2 = (232, 213, 168)
TEXT = (243, 241, 237)
TEXT_DIM = (150, 147, 158)
GRAY = (150, 147, 158)
GREEN = (142, 182, 155)
GREEN_BTN = (90, 125, 98)
RED = (201, 123, 123)
DIM_BTN = (45, 45, 53)
WHITE = (255, 255, 255)
BTN_ON_ACCENT = (20, 17, 12)

WIN_FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
WIN_FONT_SEMI = "C:/Windows/Fonts/segoeuib.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _text_w(font: ImageFont.ImageFont, text: str) -> float:
    if hasattr(font, "getlength"):
        return float(font.getlength(text))
    return float(font.getsize(text)[0])


def bg_array() -> np.ndarray:
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    r = BG_TOP[0] * (1 - y) + BG_BOT[0] * y
    g = BG_TOP[1] * (1 - y) + BG_BOT[1] * y
    b = BG_TOP[2] * (1 - y) + BG_BOT[2] * y
    arr = np.stack([r, g, b], axis=-1).astype(np.float32)
    yy, xx = np.ogrid[:H, :W]
    cx, cy = W / 2, H / 2
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    d = (d / d.max()).astype(np.float32)
    glow = np.stack([d * 18, d * 14, d * 5], axis=-1)
    arr = np.clip(arr + glow, 0, 255).astype(np.uint8)
    return arr


def rr(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, ...],
    outline: tuple[int, ...] | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_cursor(
    draw: ImageDraw.ImageDraw, x: int, y: int, click: float = 0, scale: float = 1.0
) -> None:
    s = scale * (1.0 + 0.12 * click)
    x, y = int(x), int(y)
    pts_s = [(x + 3, y + 3), (x + 3 + 6 * s, y + 3 + 18 * s), (x + 3 + 14 * s, y + 3 + 14 * s)]
    draw.polygon(pts_s, fill=(0, 0, 0, 100))
    pts = [(x, y), (x + 6 * s, y + 18 * s), (x + 14 * s, y + 14 * s)]
    draw.polygon(pts, outline=(50, 50, 58), fill=(248, 248, 252, 235))
    if click > 0.2:
        r = int((8 + 22 * click) * scale)
        a = int(140 * (1 - click))
        draw.ellipse((x - r, y - r, x + r, y + r), outline=(*ACCENT, a), width=max(2, int(3 * scale)))


def draw_desktop_story(frame_i: int, n_frames: int) -> np.ndarray:
    """Select files (four months) → Analyzing… → one large, bold summary screen."""
    t = frame_i / max(1, n_frames - 1)
    pick_end = 0.30
    ana_end = 0.46

    arr = bg_array()
    img = Image.fromarray(arr).convert("RGBA")

    tbar = _font(WIN_FONT_SEMI, 24)
    nav = _font(WIN_FONT_SEMI, 28)
    btn = _font(WIN_FONT_SEMI, 34)
    dlg_title = _font(WIN_FONT_SEMI, 44)
    row_main = _font(WIN_FONT_SEMI, 38)
    ana_big = _font(WIN_FONT_SEMI, 64)
    ana_mid = _font(WIN_FONT_SEMI, 34)
    ana_small = _font(WIN_FONT_SEMI, 30)
    hero_name = _font(WIN_FONT_SEMI, 56)
    hero_lbl = _font(WIN_FONT_SEMI, 36)
    hero_money = _font(WIN_FONT_SEMI, 52)
    hero_score = _font(WIN_FONT_SEMI, 76)
    col_title = _font(WIN_FONT_SEMI, 38)
    col_line = _font(WIN_FONT_SEMI, 32)
    foot = _font(WIN_FONT_SEMI, 34)

    wx0, wy0 = 64, 48
    wx1, wy1 = W - 64, H - 40
    d = ImageDraw.Draw(img)
    rr(d, (wx0, wy0, wx1, wy1), 16, (*CARD_BG2, 255))
    rr(d, (wx0, wy0, wx1, wy0 + 60), 12, (18, 18, 22, 255))
    d.text((wx0 + 52, wy0 + 16), "Fund Pilot — MCA Analyzer", fill=GRAY, font=tbar)
    for i, col in enumerate(((201, 123, 123), ACCENT, GREEN)):
        cx = wx0 + 24 + i * 22
        cy = wy0 + 29
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=col)

    ix = wx0 + 32
    iy0 = wy0 + 82
    iw = wx1 - wx0 - 56

    mx0, mx1 = W // 2 - 500, W // 2 + 500
    my0, my1 = H // 2 - 340, H // 2 + 340
    oby = my1 - 112

    if t < pick_end:
        u = t / pick_end
        pill_h = 50
        px = ix
        iy = iy0
        pills = ["Features", "Recommended", "Follow-ups", "Workspace", "Analyze"]
        for p in pills:
            active = p == "Analyze"
            pw = int(_text_w(nav, p) + 44)
            bg = ACCENT if active else DIM_BTN
            rr(d, (int(px), iy, int(px + pw), iy + pill_h), 10, (*bg, 255))
            fg = BTN_ON_ACCENT if active else TEXT
            d.text((px + 20, iy + 10), p, fill=fg[:3], font=nav)
            px += pw + 14
        iy_nav = iy + pill_h + 32

        rr(d, (ix, iy_nav, ix + iw, iy_nav + 120), 16, (*CARD_BG, 255), (*ACCENT, 90), 2)
        d.text((ix + 36, iy_nav + 22), "Add bank statements for this merchant", fill=ACCENT2, font=hero_lbl)
        sfx = ix + 44
        sfy = iy_nav + 68
        sfw, sfh = 400, 68
        pulse = 0.82 + 0.18 * math.sin(frame_i * 0.33)
        gold = (int(ACCENT[0] * pulse + 28), int(ACCENT[1] * pulse + 22), int(ACCENT[2] * pulse + 16))
        rr(d, (sfx, sfy, sfx + sfw, sfy + sfh), 14, (*gold, 255))
        d.text((sfx + 58, sfy + 16), "Select files…", fill=BTN_ON_ACCENT, font=btn)

        dialog_on = u > 0.14
        if dialog_on:
            overlay = Image.new("RGBA", (W, H), (8, 8, 10, 185))
            img = Image.alpha_composite(img, overlay)
            d = ImageDraw.Draw(img)
            rr(d, (mx0, my0, mx1, my1), 22, (*CARD_BG, 254), (*ACCENT, 130), 3)
            d.text((mx0 + 48, my0 + 44), "Pick four statement months", fill=ACCENT2, font=dlg_title)

            months = [
                "December 2025  ·  bank_statement.pdf",
                "January 2026  ·  bank_statement.pdf",
                "February 2026  ·  bank_statement.pdf",
                "March 2026  ·  bank_statement.pdf",
            ]
            ry0 = my0 + 128
            for i, line in enumerate(months):
                reveal = max(0, min(1, (u - 0.17) * 1.4 - i * 0.19))
                ry = ry0 + i * 96
                if reveal < 0.06:
                    continue
                al = int(255 * min(1.0, reveal * 1.12))
                rr(d, (mx0 + 44, ry, mx1 - 44, ry + 86), 16, (32, 32, 40, al))
                cx_m = mx0 + 64
                if reveal > 0.52:
                    d.text((cx_m, ry + 22), "✓", fill=(*GREEN, al), font=row_main)
                    cx_m += int(_text_w(row_main, "✓")) + 18
                d.text((cx_m, ry + 24), line, fill=(*TEXT, al), font=row_main)

            rr(d, (mx1 - 380, oby, mx1 - 48, oby + 72), 16, (*GREEN_BTN, 250))
            d.text((mx1 - 348, oby + 20), "Use these 4 PDFs", fill=WHITE, font=btn)

        d = ImageDraw.Draw(img)
        if not dialog_on:
            tx, ty = sfx + sfw - 28, sfy + sfh // 2
            p = max(0, min(1, u / 0.11))
            cx_cur = int(W * 0.84 + (tx - W * 0.84) * p)
            cy_cur = int(H * 0.80 + (ty - H * 0.80) * p)
            clk = max(0, 1.0 - abs((u - 0.135) * 28)) if 0.10 < u < 0.17 else 0.0
        else:
            tx, ty = mx1 - 210, oby + 36
            p = max(0, min(1, (u - 0.68) / 0.20))
            cx_cur = int(sfx + 140 + (tx - (sfx + 140)) * p)
            cy_cur = int(sfy + 32 + (ty - (sfy + 32)) * p)
            clk = max(0, 1.0 - abs((u - 0.92) * 35)) if 0.88 < u < 0.97 else 0.0
        draw_cursor(d, cx_cur, cy_cur, click=clk, scale=1.9)

    elif t < ana_end:
        u = (t - pick_end) / (ana_end - pick_end)
        d = ImageDraw.Draw(img)
        cx0, cy0 = wx0 + 28, wy0 + 100
        cx1, cy1 = wx1 - 28, wy1 - 36
        rr(d, (cx0, cy0, cx1, cy1), 20, (*CARD_BG, 255))
        ttl = "Analyzing…"
        d.text((int((W - _text_w(ana_big, ttl)) / 2), cy0 + 110), ttl, fill=ACCENT2, font=ana_big)
        sub = "Reading 4 months of statements  ·  building the full picture"
        d.text((int((W - _text_w(ana_mid, sub)) / 2), cy0 + 210), sub, fill=TEXT_DIM, font=ana_mid)
        bar_x0, bar_y = W // 2 - 460, cy0 + 330
        bar_x1 = W // 2 + 460
        rr(d, (bar_x0, bar_y, bar_x1, bar_y + 36), 12, (42, 42, 50, 255))
        prog = 0.52 + 0.48 * math.sin(u * math.pi * 2.4 + frame_i * 0.07)
        rr(d, (bar_x0, bar_y, int(bar_x0 + (bar_x1 - bar_x0) * prog), bar_y + 36), 12, (*ACCENT, 235))
        hint = "Deposits  ·  weekly positions  ·  score  ·  estimated funding range"
        d.text((int((W - _text_w(ana_small, hint)) / 2), bar_y + 60), hint, fill=GRAY, font=ana_small)

    else:
        u = (t - ana_end) / max(0.001, (1.0 - ana_end))
        d = ImageDraw.Draw(img)
        bx0, by0 = wx0 + 24, wy0 + 96
        bx1, by1 = wx1 - 24, wy1 - 32
        rr(d, (bx0, by0, bx1, by1), 24, (*CARD_BG, 255), (*ACCENT, 100), 2)
        intro = float(min(1.0, u * 2.0))
        al = int(255 * intro)

        nam = "SUMMIT TRUCKING LLC"
        d.text((int((W - _text_w(hero_name, nam)) / 2), by0 + 44), nam, fill=(*TEXT, al), font=hero_name)

        fl = "Estimated funding range"
        d.text((int((W - _text_w(hero_lbl, fl)) / 2), by0 + 138), fl, fill=(*TEXT_DIM, al), font=hero_lbl)
        money = "$85,000  —  $140,000"
        d.text((int((W - _text_w(hero_money, money)) / 2), by0 + 188), money, fill=(*ACCENT, al), font=hero_money)

        sc_l = "Approval score"
        d.text((int((W - _text_w(hero_lbl, sc_l)) / 2), by0 + 288), sc_l, fill=(*TEXT_DIM, al), font=hero_lbl)
        sc_v = "7.5 / 10"
        d.text((int((W - _text_w(hero_score, sc_v)) / 2), by0 + 332), sc_v, fill=(*GREEN, al), font=hero_score)

        rec = "Suggested lenders  ·  Harbor WC  ·  Northline SB  ·  Summit Advance"
        d.text((int((W - _text_w(col_line, rec)) / 2), by0 + 408), rec, fill=(*GREEN, al), font=col_line)

        warn = "Stacking: four weekly positions — confirm payoffs before shopping"
        warn_fw = int(_text_w(col_line, warn))
        pad_x = 44
        wx_l = (W - warn_fw) // 2 - pad_x
        wx_r = (W + warn_fw) // 2 + pad_x
        wy_box = by0 + 452
        rr(
            d,
            (wx_l, wy_box, wx_r, wy_box + 58),
            14,
            (56, 38, 40, 255),
            (*RED, 170),
            2,
        )
        d.text(((W - warn_fw) // 2, wy_box + 14), warn, fill=(*RED, al), font=col_line)

        split = W // 2
        col_top = by0 + 538
        d.text((bx0 + 60, col_top), "Cash flow — four months (net)", fill=(*ACCENT, al), font=col_title)
        flows = [
            "March 2026          +$38,905",
            "February 2026       +$31,240",
            "January 2026        +$35,180",
            "December 2025       +$33,050",
        ]
        ly = col_top + 52
        for ln in flows:
            d.text((bx0 + 68, ly), ln, fill=(*GREEN, al), font=col_line)
            ly += 46

        d.text((split + 36, col_top), "Weekly pay positions (funded)", fill=(*ACCENT, al), font=col_title)
        pos_lines = [
            "Forward     $2,850/wk   $42.5k   Sep 14, 2025",
            "Greenbox    $2,100/wk   $38.2k   Oct 2, 2025",
            "Harbor      $1,675/wk   $29.9k   Nov 19, 2025",
            "Northline   $1,240/wk   $24k     Dec 8, 2025",
        ]
        ly = col_top + 52
        for ln in pos_lines:
            d.text((split + 44, ly), ln, fill=(*TEXT, al), font=col_line)
            ly += 46

        footer = "DataMerch: no default  ·  no judgment  ·  phone on file"
        d.text((int((W - _text_w(foot, footer)) / 2), by1 - 100), footer, fill=(*TEXT_DIM, al), font=foot)

    return np.array(img.convert("RGB"))


def draw_mobile_calendar(phase: float) -> np.ndarray:
    arr = bg_array()
    img = Image.fromarray(arr).convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    f12 = _font(WIN_FONT_SEMI, 20)
    f14 = _font(WIN_FONT_SEMI, 24)
    f10 = _font(WIN_FONT_REG, 18)
    f10b = _font(WIN_FONT_SEMI, 19)
    cell = 56
    mx0, my0 = W // 2 - 240, H // 2 - 380
    mx1, my1 = W // 2 + 240, H // 2 + 380
    rr(d, (mx0, my0, mx1, my1), 44, (10, 10, 12, 255))
    rr(d, (mx0 + 12, my0 + 12, mx1 - 12, my1 - 12), 36, (*CARD_BG, 255))
    ix, iy = mx0 + 34, my0 + 52
    d.text((ix, iy), "Follow-ups — Fund Pilot", fill=ACCENT, font=f12)
    iy += 42
    d.text((ix, iy), "February 2026", fill=TEXT, font=f14)
    iy += 40
    for ci, c in enumerate(["M", "T", "W", "T", "F", "S", "S"]):
        d.text((ix + ci * cell, iy), c, fill=TEXT_DIM, font=f10)
    iy += 30
    days_layout = [
        [None, None, None, None, None, None, 1],
        [2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22],
        [23, 24, 25, 26, 27, 28, None],
    ]
    pulse = 0.92 + 0.08 * math.sin(phase * 2 * math.pi)
    for row in days_layout:
        cx = ix
        for day in row:
            if day is None:
                cx += cell
                continue
            if day == 12:
                rr(d, (cx - 2, iy - 2, cx + cell - 8, iy + 30), 9, (*ACCENT, int(55 * pulse)))
                d.text((cx + 14, iy + 2), str(day), fill=BTN_ON_ACCENT, font=f10b)
            else:
                d.text((cx + 14, iy + 2), str(day), fill=TEXT, font=f10)
            cx += cell
        iy += 36
    iy = my0 + 360
    rr(d, (mx0 + 28, iy, mx1 - 28, iy + 96), 14, (28, 24, 18, 255), (*ACCENT, 100), 1)
    d.text((mx0 + 46, iy + 16), "Thursday, February 12", fill=TEXT_DIM, font=f10)
    d.text((mx0 + 46, iy + 48), "10:30 AM · Callback — Summit Trucking LLC", fill=TEXT, font=f12)
    cap = "Planner — same callbacks as desktop"
    fc = _font(WIN_FONT_SEMI, 18)
    ImageDraw.Draw(img).text((int((W - _text_w(fc, cap)) / 2), my1 + 24), cap, fill=GRAY, font=fc)
    return np.array(img.convert("RGB"))


def draw_mobile_notification(phase: float) -> np.ndarray:
    arr = bg_array()
    img = Image.fromarray(arr).convert("RGBA")
    blob = Image.new("RGBA", (W, H), (28, 24, 38, 255))
    img = Image.alpha_composite(img, blob.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(img, "RGBA")
    scale = 1.0 + 0.035 * math.sin(phase * 2 * math.pi)
    nw, nh = int(640 * scale), int(142 * scale)
    nx = (W - nw) // 2
    ny = H // 2 - 70 + int(6 * math.sin(phase * 2 * math.pi))
    rr(d, (nx, ny, nx + nw, ny + nh), 22, (44, 44, 50, 245))
    rr(d, (nx + 4, ny + 4, nx + nw - 4, ny + nh - 4), 19, (22, 22, 28, 252))
    f9 = _font(WIN_FONT_REG, 16)
    f13 = _font(WIN_FONT_SEMI, 22)
    f11 = _font(WIN_FONT_SEMI, 20)
    d.text((nx + 28, ny + 22), "CALENDAR", fill=TEXT_DIM, font=f9)
    d.text((nx + 28, ny + 44), "Callback — Summit Trucking LLC", fill=TEXT, font=f13)
    d.text((nx + 28, ny + 82), "Today · 10:30 AM · Fund Pilot", fill=ACCENT, font=f11)
    fb = _font(WIN_FONT_SEMI, 18)
    tx = "Expanded notification — before unlock"
    d.text((int((W - _text_w(fb, tx)) / 2), ny + nh + 36), tx, fill=GRAY, font=fb)
    return np.array(img.convert("RGB"))


def write_mp4(path: Path, frame_iter, fps: int, crf: str = "26") -> None:
    writer = imageio.get_writer(
        str(path),
        fps=fps,
        codec="libx264",
        pixelformat="yuv420p",
        ffmpeg_params=["-crf", crf, "-preset", "medium", "-movflags", "+faststart"],
    )
    try:
        for fr in frame_iter:
            writer.append_data(fr)
    finally:
        writer.close()


def save_mobile_screenshots() -> None:
    """Full-frame 1920×1088 PNGs for the marketing site (calendar + notification mocks)."""
    cal = draw_mobile_calendar(0.28)
    Image.fromarray(cal).save(ASSETS / "mobile-screenshot-calendar.png", optimize=True)
    notif = draw_mobile_notification(0.28)
    Image.fromarray(notif).save(ASSETS / "mobile-screenshot-notification.png", optimize=True)


def save_iphone_lock_demo() -> None:
    """750×1624 marketing hero: synthetic iPhone lock screen + Fund Pilot calendar notification."""
    pw, ph = 750, 1624
    img = Image.new("RGB", (pw, ph))
    px = img.load()
    for y in range(ph):
        t = y / max(1, ph - 1)
        r = int(12 + t * 38)
        g = int(14 + t * 36)
        b = int(48 + t * 52)
        for x in range(pw):
            px[x, y] = (r, g, b)

    d = ImageDraw.Draw(img, "RGBA")
    status_y = 56

    f_status = _font(WIN_FONT_SEMI, 17)
    f_time = _font(WIN_FONT_SEMI, 82)
    f_date = _font(WIN_FONT_REG, 22)
    f_cal_lbl = _font(WIN_FONT_REG, 14)
    f_cal_title = _font(WIN_FONT_SEMI, 20)
    f_cal_sub = _font(WIN_FONT_SEMI, 18)

    d.text((44, status_y), "9:41", fill=TEXT, font=f_status)
    sw = _text_w(f_status, "LTE  100%")
    d.text((pw - sw - 44, status_y), "LTE  100%", fill=TEXT, font=f_status)

    time_s = "10:30"
    tw = _text_w(f_time, time_s)
    d.text((int((pw - tw) / 2), status_y + 140), time_s, fill=TEXT, font=f_time)

    date_s = "Wednesday, February 12"
    dw = _text_w(f_date, date_s)
    d.text((int((pw - dw) / 2), status_y + 240), date_s, fill=TEXT_DIM, font=f_date)

    nx0 = 36
    nx_r = pw - 36
    ny0 = status_y + 340
    nh = 124
    rr(d, (nx0, ny0, nx_r, ny0 + nh), 26, (36, 36, 44, 248))
    d.text((nx0 + 22, ny0 + 18), "CALENDAR", fill=TEXT_DIM, font=f_cal_lbl)
    d.text((nx0 + 22, ny0 + 40), "Callback — Summit Trucking LLC", fill=TEXT, font=f_cal_title)
    d.text((nx0 + 22, ny0 + 80), "Today · 10:30 AM · Fund Pilot", fill=ACCENT, font=f_cal_sub)

    hint = _font(WIN_FONT_REG, 16)
    cap = "Synthetic lock screen — Fund Pilot · Core + CRM"
    cw = _text_w(hint, cap)
    d.text((int((pw - cw) / 2), ph - 72), cap, fill=TEXT_DIM, font=hint)

    img.convert("RGB").save(ASSETS / "iphone-followup-notification-demo.png", optimize=True)


def draw_iphone_app_crm() -> Image.Image:
    """750×1624 in-app CRM pipeline screen for 3D phone mockups."""
    pw, ph = 750, 1624
    img = Image.new("RGB", (pw, ph), BG_TOP)
    d = ImageDraw.Draw(img)
    f10 = _font(WIN_FONT_REG, 16)
    f12 = _font(WIN_FONT_SEMI, 18)
    f14 = _font(WIN_FONT_SEMI, 22)
    f18 = _font(WIN_FONT_SEMI, 28)
    f22 = _font(WIN_FONT_SEMI, 34)

    # status
    d.text((44, 56), "9:41", fill=TEXT, font=f12)
    sw = _text_w(f12, "5G  100%")
    d.text((pw - sw - 44, 56), "5G  100%", fill=TEXT, font=f12)

    d.text((44, 118), "Fund Pilot", fill=ACCENT, font=f14)
    d.text((44, 152), "Pipeline", fill=TEXT, font=f22)

    # search bar
    rr(d, (44, 210, pw - 44, 268), 16, CARD_BG)
    d.text((68, 228), "Search merchants…", fill=TEXT_DIM, font=f12)

    # filter pills
    pills = ["All deals", "Contacted", "My activity"]
    px = 44
    for i, p in enumerate(pills):
        active = i == 0
        pw_p = int(_text_w(f10, p) + 36)
        rr(d, (px, 288, px + pw_p, 328), 999, ACCENT if active else DIM_BTN)
        d.text((px + 18, 300), p, fill=BTN_ON_ACCENT if active else TEXT, font=f10)
        px += pw_p + 12

    deals = [
        ("Summit Trucking LLC", "$142K/mo", "Score 7.5", "Analyze ready"),
        ("Metro HVAC Services", "$98K/mo", "Score 8.2", "In CRM"),
        ("Coastal Auto Repair", "$76K/mo", "Score 6.9", "Follow-up today"),
        ("Brightline Logistics", "$210K/mo", "Score 9.1", "Dialing"),
        ("Prime Dental Group", "$54K/mo", "Score 7.0", "Packaged"),
    ]
    y = 360
    for name, dep, score, tag in deals:
        rr(d, (36, y, pw - 36, y + 118), 20, CARD_BG, (*ACCENT, 60 if tag == "Analyze ready" else 30), 2)
        d.text((56, y + 18), name, fill=TEXT, font=f14)
        d.text((56, y + 52), dep, fill=TEXT_DIM, font=f12)
        d.text((56, y + 82), score, fill=GREEN, font=f12)
        tw = _text_w(f10, tag)
        rr(d, (pw - 56 - tw, y + 20, pw - 56, y + 50), 8, (212, 175, 115, 40) if "Analyze" in tag else DIM_BTN)
        d.text((pw - 48 - tw, y + 28), tag, fill=ACCENT if "Analyze" in tag else TEXT_DIM, font=f10)
        y += 132

    # bottom tab bar
    rr(d, (0, ph - 120, pw, ph), 0, (16, 16, 20))
    tabs = ["Home", "CRM", "Call", "More"]
    tx = pw // 8
    for i, tab in enumerate(tabs):
        col = ACCENT if tab == "CRM" else TEXT_DIM
        tw = _text_w(f10, tab)
        d.text((tx + i * (pw // 4) - tw // 2, ph - 68), tab, fill=col, font=f10)

    return img


def draw_iphone_app_deal() -> Image.Image:
    """750×1624 deal detail + score for secondary phone in 3D cluster."""
    pw, ph = 750, 1624
    img = Image.new("RGB", (pw, ph), BG_TOP)
    d = ImageDraw.Draw(img)
    f10 = _font(WIN_FONT_REG, 16)
    f12 = _font(WIN_FONT_SEMI, 18)
    f14 = _font(WIN_FONT_SEMI, 22)
    f18 = _font(WIN_FONT_SEMI, 28)
    f36 = _font(WIN_FONT_SEMI, 52)

    d.text((44, 56), "9:41", fill=TEXT, font=f12)
    d.text((44, 118), "← CRM", fill=ACCENT, font=f12)
    d.text((44, 162), "Summit Trucking LLC", fill=TEXT, font=f18)

    rr(d, (36, 220, pw - 36, 420), 24, CARD_BG, (*ACCENT, 90), 2)
    d.text((56, 248), "Funding range", fill=TEXT_DIM, font=f12)
    d.text((56, 282), "$85K — $140K", fill=ACCENT, font=f36)
    d.text((56, 360), "Approval score  7.5 / 10", fill=GREEN, font=f14)

    rr(d, (36, 448, pw - 36, 620), 20, CARD_BG)
    d.text((56, 472), "Next step", fill=ACCENT, font=f12)
    d.text((56, 508), "Callback today · 10:30 AM", fill=TEXT, font=f14)
    d.text((56, 548), "Rep: Frank Romano", fill=TEXT_DIM, font=f12)

    rr(d, (36, 648, pw - 36, 760), 20, (28, 24, 18))
    d.text((56, 676), "Push reminder sent to lock screen", fill=ACCENT, font=f12)
    d.text((56, 712), "Tap to open dialer campaign", fill=TEXT_DIM, font=f10)

    rr(d, (36, 788, pw - 36, 860), 16, GREEN_BTN)
    d.text((int((pw - _text_w(f14, "Call merchant")) / 2), 812), "Call merchant", fill=WHITE, font=f14)

    return img


def draw_desktop_crm() -> np.ndarray:
    """Static CRM board frame for 3D laptop screen."""
    arr = bg_array()
    img = Image.fromarray(arr).convert("RGBA")
    d = ImageDraw.Draw(img)
    nav = _font(WIN_FONT_SEMI, 28)
    row = _font(WIN_FONT_SEMI, 32)
    sm = _font(WIN_FONT_REG, 26)
    title = _font(WIN_FONT_SEMI, 38)

    wx0, wy0, wx1, wy1 = 64, 48, W - 64, H - 40
    rr(d, (wx0, wy0, wx1, wy1), 16, (*CARD_BG2, 255))
    rr(d, (wx0, wy0, wx1, wy0 + 60), 12, (18, 18, 22, 255))
    d.text((wx0 + 52, wy0 + 16), "Fund Pilot — CRM", fill=GRAY, font=sm)

    ix, iy = wx0 + 32, wy0 + 82
    pills = ["Home", "CRM", "Call", "Analyze"]
    px = ix
    for p in pills:
        active = p == "CRM"
        pw_p = int(_text_w(nav, p) + 44)
        rr(d, (px, iy, px + pw_p, iy + 50), 10, ACCENT if active else DIM_BTN)
        d.text((px + 20, iy + 10), p, fill=BTN_ON_ACCENT if active else TEXT, font=nav)
        px += pw_p + 14

    d.text((ix, iy + 78), "Deal board — 15,332 merchants", fill=TEXT, font=title)

    cols = ["Merchant", "Monthly dep.", "Score", "Status"]
    cx = ix
    for c in cols:
        d.text((cx, iy + 140), c, fill=ACCENT, font=sm)
        cx += 420

    rows = [
        ("Summit Trucking LLC", "$142,000", "7.5", "Ready"),
        ("Metro HVAC Services", "$98,400", "8.2", "Contacted"),
        ("Coastal Auto Repair", "$76,200", "6.9", "Follow-up"),
        ("Brightline Logistics", "$210,800", "9.1", "Dialing"),
    ]
    ry = iy + 190
    for i, (name, dep, score, st) in enumerate(rows):
        bg = (24, 24, 30) if i % 2 == 0 else CARD_BG
        rr(d, (ix, ry, wx1 - 32, ry + 72), 12, bg)
        d.text((ix + 20, ry + 20), name, fill=TEXT, font=row)
        d.text((ix + 440, ry + 20), dep, fill=TEXT_DIM, font=sm)
        d.text((ix + 860, ry + 20), score, fill=GREEN, font=row)
        d.text((ix + 1040, ry + 20), st, fill=ACCENT if st == "Ready" else TEXT_DIM, font=sm)
        ry += 82

    return np.array(img.convert("RGB"))


def save_device_screenshots() -> None:
    draw_iphone_app_crm().save(ASSETS / "iphone-app-crm.png", optimize=True)
    draw_iphone_app_deal().save(ASSETS / "iphone-app-deal.png", optimize=True)
    Image.fromarray(draw_desktop_crm()).save(ASSETS / "desktop-crm-screenshot.png", optimize=True)


def main() -> None:
    """Generate all marketing assets (v2 videos + mobile PNGs)."""
    from render_marketing_demos_v2 import render_all as render_v2

    render_v2()
    ASSETS.mkdir(parents=True, exist_ok=True)
    print("Mobile screenshots…")
    save_mobile_screenshots()
    save_iphone_lock_demo()
    print("Device PNGs (CRM phone mocks)…")
    save_device_screenshots()
    print("All marketing assets complete.")


if __name__ == "__main__":
    main()
