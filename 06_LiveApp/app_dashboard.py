# -*- coding: utf-8 -*-
"""
PHANToM GRID :: CHI-BENCH CLINICAL OPERATIONS DESK LAUNCHER (PG-SHOWCASE-02)
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8766
DIRECTORY = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"[*] CHI-Bench Operations Desk running at http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}/index.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Server shutdown gracefully.")

if __name__ == "__main__":
    main()
