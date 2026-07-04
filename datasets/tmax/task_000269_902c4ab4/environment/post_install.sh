apt-get update && apt-get install -y python3 python3-pip nginx curl openssl
    pip3 install pytest flask

    mkdir -p /app/nginx /app/certs /app/backend /app/corpus/evil /app/corpus/clean

    # Nginx config for non-root user
    cat << 'EOF' > /app/nginx/nginx.conf
worker_processes 1;
pid /tmp/nginx.pid;
error_log /tmp/error.log;

events {
    worker_connections 1024;
}

http {
    client_body_temp_path /tmp/client_body;
    fastcgi_temp_path /tmp/fastcgi_temp;
    proxy_temp_path /tmp/proxy_temp;
    scgi_temp_path /tmp/scgi_temp;
    uwsgi_temp_path /tmp/uwsgi_temp;
    access_log /tmp/access.log;

    server {
        listen 8443 ssl;
        ssl_certificate /app/certs/cert.pem;
        ssl_certificate_key /app/certs/key.pem;

        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

    # Backend Flask server
    cat << 'EOF' > /app/backend/server.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"status": "ok", "data": "CC: 1234-5678-1234-5678"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    # Corpus files
    echo "<script>alert(1)</script>" > /app/corpus/evil/1.txt
    echo "' OR 1=1--" > /app/corpus/evil/2.txt
    echo "hello world" > /app/corpus/clean/1.txt
    echo "admin" > /app/corpus/clean/2.txt

    # Set permissions for /app
    chmod -R 777 /app

    # Create user and set permissions for home directory
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user