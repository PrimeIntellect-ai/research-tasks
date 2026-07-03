apt-get update && apt-get install -y python3 python3-pip ffmpeg fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app
    mkdir -p /opt

    # Create the vulnerable service
    cat << 'EOF' > /opt/vulnerable_service.py
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get('Authorization')
        if auth != 'Bearer SuperSecretKey123!':
            self.send_response(401)
            self.end_headers()
            return

        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/read':
            query = urllib.parse.parse_qs(parsed_path.query)
            if 'path' in query:
                filepath = query['path'][0]
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(content.encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(str(e).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8080), MyHandler)
    server.serve_forever()
EOF

    # Generate the video with the hidden text
    ffmpeg -f lavfi -i color=c=black:s=640x480:d=10 \
        -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='/usr/bin/python3 /opt/vulnerable_service.py --port 8080 --auth-token SuperSecretKey123!':fontcolor=white:fontsize=14:x=10:y=10:enable='between(t,4,6)'" \
        -c:v libx264 -t 10 -y /app/debug_session.mp4

    # Ensure the service runs on shell startup for testing purposes if not using instances
    echo "python3 /opt/vulnerable_service.py >/dev/null 2>&1 &" >> /etc/bash.bashrc

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user