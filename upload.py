import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

UPLOAD_DIR = "images/uploads"
UPLOAD_PASSWORD = "852"

class SimpleUploader(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            if "file" in form and "secret" in form:
                file_field = form["file"]
                password = form.getvalue("secret")

                if password != UPLOAD_PASSWORD:
                    self.send_response(403)
                    self.end_headers()
                    self.wfile.write(b"Forbidden: incorrect password")
                    return

                if file_field.filename:
                    filename = os.path.basename(file_field.filename)
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_field.file.read())
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Success')
                    return

            self.send_error(400, 'Bad Request')

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            with open("." + self.path, "rb") as file:
                self.send_response(200)
                if self.path.endswith(".js"):
                    self.send_header("Content-type", "application/javascript")
                elif self.path.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                elif self.path.endswith(".png") or self.path.endswith(".jpg") or self.path.endswith(".jpeg"):
                    self.send_header("Content-type", "image/png")
                else:
                    self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print("Server running at http://localhost:8000/")
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleUploader)
    httpd.serve_forever()