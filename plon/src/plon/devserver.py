#Use to create local host
import http.server
import socketserver
from pathlib import Path

PORT = 8000

HERE = Path(__file__).parent
DIRECTORY = HERE / 'view'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

Handler.extensions_map.update({
      ".js": "application/javascript",
});

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()
