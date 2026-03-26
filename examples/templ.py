from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from fake_weather_data import list_cities, get_weather
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 5000

class WeatherRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/weather/cities":
            cities = list_cities()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"cities": cities}).encode())
        elif parsed_path.path == "/get_weather":
            query = parse_qs(parsed_path.query)
            city = query.get("city", [None])[0]
            weather = get_weather(city)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"weather": weather}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    print(f"Starting server at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), WeatherRequestHandler)
    server.serve_forever()