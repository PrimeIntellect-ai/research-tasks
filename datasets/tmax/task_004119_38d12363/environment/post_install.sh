apt-get update && apt-get install -y python3 python3-pip openssh-client procps coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create legacy_passwords.txt
    for i in $(seq 1 499); do
        echo "legacy_pass_$i" >> /home/user/legacy_passwords.txt
    done
    echo "B4sti0n_M4st3r_2022!" >> /home/user/legacy_passwords.txt

    # Create rotate_ssh.py
    cat << 'EOF' > /home/user/rotate_ssh.py
#!/usr/bin/env python3
import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--password', required=True)
args = parser.parse_args()

if args.password != "B4sti0n_M4st3r_2022!":
    print("Invalid password!")
    exit(1)

ssh_dir = "/home/user/.ssh"
os.makedirs(ssh_dir, exist_ok=True)
os.chmod(ssh_dir, 0o700)

priv_key = os.path.join(ssh_dir, "id_ed25519")
pub_key = priv_key + ".pub"
auth_keys = os.path.join(ssh_dir, "authorized_keys")

if os.path.exists(priv_key):
    os.remove(priv_key)
if os.path.exists(pub_key):
    os.remove(pub_key)

# Generate new key
subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", priv_key, "-N", "", "-q"], check=True)

# Replace authorized_keys
with open(pub_key, 'r') as f:
    pub_data = f.read()
with open(auth_keys, 'w') as f:
    f.write(pub_data)
os.chmod(auth_keys, 0o600)

print("SSH rotation successful.")
EOF
    chmod +x /home/user/rotate_ssh.py

    # Create legacy_service.py
    cat << 'EOF' > /usr/local/bin/legacy_service.py
#!/usr/bin/env python3
import http.server
import socketserver
import json

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/config':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {"status": "legacy", "admin_hash": "2f6c8d374cb2eb4d52bc05bb5f7b889504ba4e4e94b15c7e1ab2096d2e68cf0a"}
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8042), Handler) as httpd:
    httpd.serve_forever()
EOF
    chmod +x /usr/local/bin/legacy_service.py

    # Setup service to start automatically when commands are executed in the container
    cat << 'EOF' > /.singularity.d/env/99-service.sh
#!/bin/sh
if ! pgrep -f legacy_service.py > /dev/null; then
    nohup python3 /usr/local/bin/legacy_service.py >/dev/null 2>&1 &
    sleep 1
fi
EOF
    chmod +x /.singularity.d/env/99-service.sh

    chmod -R 777 /home/user