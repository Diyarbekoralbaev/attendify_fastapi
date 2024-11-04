import http.server
import socketserver
import os

# Customize the port and path
PORT = 3000
DIRECTORY = "/home/rocked/Desktop/aralvision_frontend"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Try to serve the file requested by the client
        if self.path != '/' and not os.path.exists(DIRECTORY + self.path):
            # If the file does not exist, serve index.html
            self.path = '/index.html'
        return super().do_GET()

# Set up the server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
