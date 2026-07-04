apt-get update && apt-get install -y python3 python3-pip ffmpeg tesseract-ocr openssl curl
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/certs

    # Generate the video with mock traffic
    cat << 'EOF' > /app/gen_vid.py
import os
tokens = ["aB9xLp2QzM4vN7cY", "Kk3jH8fP5wR1tG6u", "7dE4sW2xZ9vC1bM0", "Xm5yN8pQ3rT6kV2j", "9fL4cV1bN7mZ3xK8"]
text = "\n".join([f"Set-Cookie: auth_session={t};" for t in tokens])
with open("/app/text.txt", "w") as f:
    f.write(text)
os.system("ffmpeg -f lavfi -i color=c=black:s=640x480:d=2 -vf \"drawtext=textfile=/app/text.txt:fontcolor=white:fontsize=24:x=10:y=10\" -c:v libx264 -y /app/traffic_capture.mp4")
EOF
    python3 /app/gen_vid.py

    # Create mock HTTPS service
    cat << 'EOF' > /app/server.py
import sys, ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

port = int(sys.argv[1])
httpd = HTTPServer(('127.0.0.1', port), Handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/app/cert.pem', '/app/key.pem')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
EOF

    # Generate dummy certs for the mock services
    openssl req -x509 -newkey rsa:2048 -keyout /app/key.pem -out /app/cert.pem -days 365 -nodes -subj '/CN=localhost'

    # Start the services in the background whenever the container is executed
    echo "python3 /app/server.py 8084 >/dev/null 2>&1 &" >> $APPTAINER_ENVIRONMENT
    echo "python3 /app/server.py 8087 >/dev/null 2>&1 &" >> $APPTAINER_ENVIRONMENT

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app