from http.server import BaseHTTPRequestHandler
from datetime import datetime
# from notion_renderer import main
from notion_renderer import version
from notion_renderer.mdx import hello


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        greeting = hello('Sunny')

        self.wfile.write(
            (str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n' + greeting).encode())
        return
