"""
Local static preview with anti-cache headers so refresh always pulls latest CSS/JS.
"""
from __future__ import annotations

import argparse
import http.server
import os
import socketserver


class NoCacheRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def main() -> None:
    p = argparse.ArgumentParser(description="Serve Fund Pilot site locally (no-cache).")
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--bind", default="127.0.0.1")
    args = p.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer((args.bind, args.port), NoCacheRequestHandler) as httpd:
        print(f"http://{args.bind}:{args.port}  (Cache-Control: no-store — refresh sees latest files)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
