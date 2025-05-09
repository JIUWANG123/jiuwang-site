import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import json

UPLOAD_DIR = "images/uploads"

class SimpleUploader(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            if "file" in form:
                file_field = form["file"]
                if file_field.filename:
                    filename = os.path.basename(file_field.filename)
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_field.file.read())
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Success')
                    return
        self.send_error(400, "Bad Request")

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        if self.path == '/list':
            files = []
            for f in os.listdir(UPLOAD_DIR):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    files.append(f)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode('utf-8'))
            return

        try:
            file_path = '.' + self.path
            with open(file_path, 'rb') as file:
                self.send_response(200)
                if self.path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif self.path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif self.path.endswith(('.jpg', '.jpeg')):
                    self.send_header('Content-type', 'image/jpeg')
                elif self.path.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print("Server running at http://localhost:8000/")
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleUploader)
    httpd.serve_forever()
