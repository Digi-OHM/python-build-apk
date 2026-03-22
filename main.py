import os
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import flet as ft

HOST = "127.0.0.1"
PORT = 8765


def start_server():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    handler = SimpleHTTPRequestHandler
    httpd = ThreadingHTTPServer((HOST, PORT), handler)
    httpd.serve_forever()


def main(page: ft.Page):
    page.title = "Shopping List"
    page.padding = 0
    page.spacing = 0

    # start local server only once
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    web = ft.WebView(
        url=f"http://{HOST}:{PORT}/index.html",
        expand=True,
    )

    page.add(web)


if __name__ == "__main__":
    ft.app(target=main)