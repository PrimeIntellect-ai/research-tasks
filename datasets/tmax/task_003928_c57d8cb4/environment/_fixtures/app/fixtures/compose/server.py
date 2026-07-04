import http.server, socketserver
PORT = 5050
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b'hello-from-app\n')
socketserver.TCPServer(("127.0.0.1", PORT), H).serve_forever()
