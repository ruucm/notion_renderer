from http.server import BaseHTTPRequestHandler
from urllib import parse
from notion_renderer.renderer import objectify_notion_blocks


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

        results = objectify_notion_blocks(dic["token_v2"],
                                          dic["pageId"], True)

        print('results', results)

        resultsStr = "[" + ','.join(results) + "]"
        self.wfile.write(resultsStr.encode())
        return
