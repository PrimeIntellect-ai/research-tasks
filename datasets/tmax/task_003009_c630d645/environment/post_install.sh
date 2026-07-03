apt-get update && apt-get install -y python3 python3-pip openssl sqlite3 curl
    pip3 install pytest flask requests

    mkdir -p /home/user/certs /home/user/target_env

    cd /home/user/certs
    openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout ca.key -out ca.crt -subj "/CN=Test CA"
    openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"
    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

    cat << 'EOF' > /home/user/target_env/init_db.py
import sqlite3

conn = sqlite3.connect('/home/user/target_env/app.db')
c = conn.cursor()
c.execute('CREATE TABLE users (username TEXT, password TEXT, token TEXT)')
c.execute("INSERT INTO users VALUES ('admin', 'Sup3rS3cr3tP4ssw0rd_991!', 'FLAG{sqli_auth_bypass_success_8832}')")
c.execute("INSERT INTO users VALUES ('guest', 'guest', 'FLAG{guest_token_none}')")
conn.commit()
conn.close()
EOF

    python3 /home/user/target_env/init_db.py

    cat << 'EOF' > /home/user/target_env/server.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing credentials"}), 400

    username = data['username']
    password = data['password']

    conn = sqlite3.connect('/home/user/target_env/app.db')
    c = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT token FROM users WHERE username='{username}' AND password='{password}'"
    try:
        c.execute(query)
        result = c.fetchone()
        conn.close()

        if result:
            return jsonify({"status": "success", "token": result[0]}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        conn.close()
        return jsonify({"error": "Database error"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user