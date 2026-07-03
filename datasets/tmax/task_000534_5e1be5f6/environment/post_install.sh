apt-get update && apt-get install -y python3 python3-pip curl g++
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/vault
echo -n "FLAG-8293-SECURE-KEY-SSRF-LEAK" > /home/user/vault/secret.key
chmod 600 /home/user/vault/secret.key

cat << 'EOF' > /home/user/auth_service.cpp
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

// Mock implementation of the vulnerable SSRF/LFI service
std::string handle_request(const std::string& redirect_uri) {
    if (redirect_uri.find("file://") == 0) {
        std::string filepath = redirect_uri.substr(7);
        std::ifstream file(filepath);
        if (file) {
            std::stringstream buffer;
            buffer << file.rdbuf();
            return buffer.str();
        }
    }
    return "HTTP/1.1 200 OK\r\n\r\nRedirecting to " + redirect_uri;
}
EOF

cat << 'EOF' > /home/user/server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import urllib.request

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if 'redirect' in qs:
            target = qs['redirect'][0]
            if target.startswith('file://'):
                try:
                    with open(target[7:], 'r') as f:
                        content = f.read()
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                except Exception as e:
                    self.send_response(404)
                    self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Redirecting")
        else:
            self.send_response(200)
            self.end_headers()

HTTPServer(('127.0.0.1', 8080), VulnerableHandler).serve_forever()
EOF

chmod -R 777 /home/user