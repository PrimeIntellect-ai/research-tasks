apt-get update && apt-get install -y python3 python3-pip nginx
    pip3 install pytest flask gunicorn

    mkdir -p /home/user/deployment/nginx
    mkdir -p /home/user/deployment/app
    mkdir -p /app

    # Create the oracle processor
    cat << 'EOF' > /app/oracle_processor
#!/usr/bin/env python3
import sys

def process(text):
    if not text: return ""
    res = []
    count = 1
    prev = text[0]
    for c in text[1:]:
        if c == prev:
            count += 1
        else:
            res.append(f"{count}{prev}")
            prev = c
            count = 1
    res.append(f"{count}{prev}")
    out = "".join(res)
    out = out.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('u', 'v')
    return out

for line in sys.stdin:
    print(process(line.strip('\n')))
EOF
    chmod +x /app/oracle_processor

    # Create the empty processor script
    cat << 'EOF' > /home/user/deployment/processor.py
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    pass
EOF
    chmod +x /home/user/deployment/processor.py

    # Create the Flask backend
    cat << 'EOF' > /home/user/deployment/app/app.py
from flask import Flask, request, Response
import subprocess

app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_data(as_text=True)
    res = subprocess.run(['/usr/bin/python3', '/home/user/deployment/processor.py'], input=data, text=True, capture_output=True)
    return Response(res.stdout, status=200)
EOF

    # Create the broken Nginx config
    cat << 'EOF' > /home/user/deployment/nginx/nginx.conf
worker_processes 1;
pid /tmp/nginx.pid;
events {
    worker_connections 1024;
}
http {
    client_body_temp_path /tmp/client_temp;
    proxy_temp_path       /tmp/proxy_temp_path;
    fastcgi_temp_path     /tmp/fastcgi_temp;
    uwsgi_temp_path       /tmp/uwsgi_temp;
    scgi_temp_path        /tmp/scgi_temp;
    access_log /tmp/access.log;
    error_log /tmp/error.log;

    server {
        listen 8080;
        location / {
            proxy_pass http://127.0.0.1:9999;
        }
    }
}
EOF

    # Wrapper for pytest to ensure background services are running during tests
    mv /usr/local/bin/pytest /usr/local/bin/pytest_orig
    cat << 'EOF' > /usr/local/bin/pytest
#!/bin/bash
nginx -c /home/user/deployment/nginx/nginx.conf &
gunicorn --chdir /home/user/deployment/app app:app -b 127.0.0.1:5000 --daemon
sleep 2
exec /usr/local/bin/pytest_orig "$@"
EOF
    chmod +x /usr/local/bin/pytest

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app