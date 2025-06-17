from http.server import BaseHTTPRequestHandler, HTTPServer

WEBPAGE = """
<style>
body {
  background-color: lightblue;
  font-family: "Comic Sans MS", cursive;
}
</style>
<h1>Python webpage!</h1>
"""

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(WEBPAGE))

webServer = HTTPServer(("localhost", 8080), MyServer)
print("Server running at http://localhost:8080")
webServer.serve_forever()
