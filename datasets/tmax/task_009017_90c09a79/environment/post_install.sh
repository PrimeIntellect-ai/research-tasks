apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import sqlite3
import os

# Create DB
db_path = '/home/user/config.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('CREATE TABLE salts (id INTEGER, salt REAL, created_at INTEGER)')
# Insert decoy (old)
c.execute('INSERT INTO salts VALUES (8472, 0.99, 1715350000)')
# Insert correct (latest)
c.execute('INSERT INTO salts VALUES (8472, 1e-08, 1715351700)')
# Insert other payloads
c.execute('INSERT INTO salts VALUES (1122, 0.5, 1715352000)')
conn.commit()
conn.close()

# Create Logs
with open('/home/user/network_intercept.log', 'w') as f:
    f.write("[2024-05-10 14:30:00 UTC] Connection established from 192.168.1.5\n")
    f.write("[2024-05-10 14:35:00 UTC] Suspicious payload stream intercepted on port 4444.\n")
    f.write("[2024-05-10 14:40:00 UTC] Connection closed.\n")

with open('/home/user/service.log', 'w') as f:
    f.write("1715351400 - INFO - Service started\n")
    f.write("1715351700 - WARN - Received staging payload. Assigned internal payload_id: 8472\n")
    f.write("1715352000 - WARN - Received staging payload. Assigned internal payload_id: 1122\n")

# Create Python script
script_content = """import sqlite3
import math
import sys

def get_latest_salt(payload_id):
    conn = sqlite3.connect('/home/user/config.db')
    c = conn.cursor()
    # BUG: Fetches the oldest instead of the latest
    c.execute('SELECT salt FROM salts WHERE id = ? ORDER BY created_at ASC LIMIT 1', (payload_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def derive_key(salt):
    # BUG: Numerical instability for small values of salt
    # f(salt) = (sqrt(salt^2 + 1) - 1) / salt^2
    y = (math.sqrt(salt**2 + 1) - 1) / (salt**2)
    return int(y * 1000000)

def decrypt(payload_id, key):
    if payload_id == 8472 and key == 500000:
        return "FLAG{num3r1c4l_4n4lys1s_ftw}"
    elif key == 0:
        return "Error: Key derivation failed (key is 0)."
    else:
        return "Decryption failed. Invalid key or payload."

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 decrypt_payload.py <payload_id>")
        sys.exit(1)

    pid = int(sys.argv[1])
    salt = get_latest_salt(pid)
    if salt is None:
        print("Payload ID not found.")
        sys.exit(1)

    key = derive_key(salt)
    result = decrypt(pid, key)
    print(result)
"""

with open('/home/user/decrypt_payload.py', 'w') as f:
    f.write(script_content)

os.chmod('/home/user/decrypt_payload.py', 0o755)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user