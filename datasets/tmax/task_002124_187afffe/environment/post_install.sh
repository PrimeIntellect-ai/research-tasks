apt-get update && apt-get install -y python3 python3-pip gawk sqlite3 curl procps
    pip3 install pytest flask

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/service

    # Create wordlist.txt
    cat << 'EOF' > /home/user/wordlist.txt
apple
banana
solstice
password
admin123
supersecret
EOF
    for i in $(seq 1 990); do echo "randomword$i" >> /home/user/wordlist.txt; done

    # Create SQLite database
    sqlite3 /home/user/service/data.db << 'EOF'
CREATE TABLE items (id INTEGER, name TEXT, description TEXT);
INSERT INTO items VALUES (1, 'Widget', 'A standard widget');
INSERT INTO items VALUES (2, 'Gadget', 'An advanced gadget');
CREATE TABLE hidden_secrets (id INTEGER, flag TEXT);
INSERT INTO hidden_secrets VALUES (1, 'SEC_FLAG{proc_leak_sqli_master_9921}');
EOF

    # Create background runner
    cat << 'EOF' > /home/user/service/runner.sh
#!/bin/bash
HASH=$(echo -n "solstice" | sha256sum | awk '{print $1}')
while true; do
    bash -c "exec -a auth_backend sleep 0.1 --password $HASH" &
    sleep 1.5
done
EOF
    chmod +x /home/user/service/runner.sh

    # Create Flask application
    cat << 'EOF' > /home/user/service/app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
TOKEN = "secret_token_8841"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data and data.get('username') == 'admin' and data.get('password') == 'solstice':
        return jsonify({"auth_token": TOKEN})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/items', methods=['GET'])
def get_items():
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    item_id = request.args.get('id')
    if not item_id:
        return jsonify({"error": "Missing id"}), 400

    conn = sqlite3.connect('/home/user/service/data.db')
    cursor = conn.cursor()
    # Vulnerable query
    query = f"SELECT name, description FROM items WHERE id = {item_id}"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    # Setup services to run on container start
    cat << 'EOF' > /.singularity.d/env/99-start-services.sh
#!/bin/bash
if ! pgrep -f "app.py" > /dev/null; then
    nohup python3 /home/user/service/app.py >/dev/null 2>&1 &
    nohup bash /home/user/service/runner.sh >/dev/null 2>&1 &
    sleep 1
fi
EOF
    chmod +x /.singularity.d/env/99-start-services.sh

    chmod -R 777 /home/user