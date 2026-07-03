apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest flask

    mkdir -p /home/user/incident

    cat << 'EOF' > /home/user/incident/app.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/profile')
def profile():
    user_id = request.args.get('id')
    conn = sqlite3.connect('users.db')
    query = f"SELECT username, email FROM users WHERE id = {user_id}"
    cursor = conn.cursor()
    cursor.execute(query)
    return str(cursor.fetchone())

@app.route('/welcome')
def welcome():
    name = request.args.get('name', 'Guest')
    html = f"<html><body><h1>Welcome, {name}</h1></body></html>"
    return render_template_string(html)
EOF

    # Generate certificate chain
    # Create root CA
    openssl req -x509 -nodes -newkey rsa:2048 -keyout /tmp/root.key -out /tmp/root.crt -days 365 -subj "/CN=EvilCorp Root CA"
    # Create server cert
    openssl req -nodes -newkey rsa:2048 -keyout /tmp/server.key -out /tmp/server.csr -subj "/CN=evil.local"
    openssl x509 -req -in /tmp/server.csr -CA /tmp/root.crt -CAkey /tmp/root.key -CAcreateserial -out /tmp/server.crt -days 365

    # Combine into chain
    cat /tmp/server.crt /tmp/root.crt > /home/user/incident/cert_chain.pem

    # Cleanup tmp files
    rm -f /tmp/root.key /tmp/root.crt /tmp/server.key /tmp/server.csr /tmp/server.crt /tmp/root.srl

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/incident
    chmod -R 777 /home/user