from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode("<h1>Python webpage!</h1>\n"))

webServer = HTTPServer(("localhost", 8080), MyServer)
print("Server running at http://localhost:8080")
webServer.serve_forever()
