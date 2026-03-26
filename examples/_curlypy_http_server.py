true = True; false = False
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
HOST: str = "127.0.0.1"
PORT: int = 42069
class ExampleEchoHandler(BaseHTTPRequestHandler) :
    def do_GET(self) :
        path = urlparse(self.path).path
        print(f"User reached {path}")
        if path == "echo" :
            self.send_response(200)
            self.wfile.write(json.dumps(self.headers))
if __name__ == "__main__" :
    print(f"HTTP Server started at {HOST} on port {PORT}")
    srv = HTTPServer((HOST, PORT), ExampleEchoHandler)
    srv.serve_forever()