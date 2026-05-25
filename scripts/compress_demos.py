# -*- coding: utf-8 -*-
"""Create web-lite MP4s (~1–4 MB) for fast gallery switching."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    import imageio_ffmpeg
except ImportError:
    print("pip install imageio-ffmpeg", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

NAMES = [
    "demo-showreel.mp4",
    "demo-desktop-analyze.mp4",
    "demo-assistant-pilot.mp4",
    "demo-dialer-campaign.mp4",
    "demo-leads-purchase.mp4",
    "demo-fleet-live.mp4",
]


def compress(src: Path, dst: Path) -> None:
    cmd = [
        FFMPEG,
        "-y",
        "-i",
        str(src),
        "-vf",
        "scale=1280:-2",
        "-c:v",
        "libx264",
        "-crf",
        "28",
        "-preset",
        "fast",
        "-movflags",
        "+faststart",
        "-an",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    for name in NAMES:
        src = ASSETS / name
        if not src.exists():
            print(f"skip (missing): {name}")
            continue
        dst = ASSETS / name.replace(".mp4", "-lite.mp4")
        mb = src.stat().st_size / (1024 * 1024)
        print(f"Compress {name} ({mb:.1f} MB) -> {dst.name}...")
        compress(src, dst)
        lite_mb = dst.stat().st_size / (1024 * 1024)
        print(f"  done: {lite_mb:.1f} MB")


if __name__ == "__main__":
    main()
