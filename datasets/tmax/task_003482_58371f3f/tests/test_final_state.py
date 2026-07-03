# test_final_state.py

import os
import stat
import subprocess
import time
import threading
import requests
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Mock Backend Setup ---
class MockBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Backend OK")

def setup_module(module):
    # Start mock backend
    module.backend_server = HTTPServer(('127.0.0.1', 8080), MockBackendHandler)
    thread = threading.Thread(target=module.backend_server.serve_forever, daemon=True)
    thread.start()

    # Run the startup script
    startup_script = "/home/user/start_gateway.sh"
    assert os.path.exists(startup_script), f"{startup_script} does not exist"

    subprocess.run(["chmod", "+x", startup_script], check=True)
    subprocess.Popen(["bash", startup_script])

    # Wait for services to start
    time.sleep(3)

def teardown_module(module):
    if hasattr(module, 'backend_server'):
        module.backend_server.shutdown()
    subprocess.run(["pkill", "-f", "nginx"], ignore_errors=True)
    subprocess.run(["pkill", "-f", "fcgiwrap"], ignore_errors=True)

# --- Helper to find certs ---
def find_certs():
    certs_dir = "/home/user/certs"
    assert os.path.isdir(certs_dir), f"{certs_dir} directory is missing"

    # Find all .crt and .key files
    crts = [os.path.join(certs_dir, f) for f in os.listdir(certs_dir) if f.endswith('.crt') or f.endswith('.pem')]
    keys = [os.path.join(certs_dir, f) for f in os.listdir(certs_dir) if f.endswith('.key')]

    # We will try to find the CA, client cert, and client key by inspecting them using openssl
    ca_cert = None
    client_cert = None
    client_key = None

    for crt in crts:
        out = subprocess.check_output(["openssl", "x509", "-in", crt, "-text", "-noout"]).decode()
        if "CA:TRUE" in out:
            ca_cert = crt
        elif "TLS Web Client Authentication" in out or "client" in crt.lower():
            client_cert = crt

    # If not explicitly marked, fallback to names
    if not ca_cert:
        for crt in crts:
            if "ca" in crt.lower(): ca_cert = crt
    if not client_cert:
        for crt in crts:
            if "client" in crt.lower(): client_cert = crt

    for key in keys:
        if "client" in key.lower():
            client_key = key

    return ca_cert, client_cert, client_key

def test_server_key_permissions():
    certs_dir = "/home/user/certs"
    keys = [os.path.join(certs_dir, f) for f in os.listdir(certs_dir) if f.endswith('.key')]
    server_key = None
    for key in keys:
        if "server" in key.lower() or "localhost" in key.lower():
            server_key = key

    if not server_key:
        # If we can't identify by name, check all keys that aren't the client key
        _, _, client_key = find_certs()
        for key in keys:
            if key != client_key:
                server_key = key
                break

    assert server_key is not None, "Could not find server private key"

    st = os.stat(server_key)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Server key {server_key} has permissions {oct(perms)}, expected 0o400"

def test_mtls_missing_client_cert():
    # Request without client cert should fail
    try:
        resp = requests.get("https://127.0.0.1:8443/data", verify=False, timeout=2)
        assert resp.status_code == 400, "Expected 400 Bad Request for missing client cert"
    except requests.exceptions.SSLError:
        # TLS handshake failure is also acceptable
        pass

def test_valid_mtls_and_jwt():
    ca_cert, client_cert, client_key = find_certs()
    assert ca_cert and client_cert and client_key, "Could not identify CA, client cert, or client key"

    # Valid JWT (alg=HS256)
    header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    payload = "e30"
    signature = "signature"
    token = f"{header}.{payload}.{signature}"

    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get("https://127.0.0.1:8443/data", headers=headers, verify=ca_cert, cert=(client_cert, client_key))
    assert resp.status_code == 200, f"Expected 200 OK for valid JWT, got {resp.status_code}"

def test_valid_mtls_vulnerable_jwt():
    ca_cert, client_cert, client_key = find_certs()
    assert ca_cert and client_cert and client_key, "Could not identify CA, client cert, or client key"

    # Vulnerable JWT (alg=none)
    header = "eyJhbGciOiJub25lIn0"
    payload = "e30"
    token = f"{header}.{payload}."

    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get("https://127.0.0.1:8443/data", headers=headers, verify=ca_cert, cert=(client_cert, client_key))
    assert resp.status_code == 403, f"Expected 403 Forbidden for vulnerable JWT, got {resp.status_code}"

def test_audit_log_format():
    log_file = "/home/user/audit.log"
    assert os.path.exists(log_file), "Audit log file does not exist"

    with open(log_file, "r") as f:
        logs = f.read().strip().split('\n')

    assert len(logs) >= 2, "Expected at least 2 audit log entries"

    # Check formats
    hs256_header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    none_header = "eyJhbGciOiJub25lIn0"

    found_200 = False
    found_403 = False

    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] AUDIT: Token with header ([a-zA-Z0-9\-_]+) evaluated\. Status: (\d{3})$")

    for line in logs:
        match = pattern.match(line)
        if match:
            hdr = match.group(1)
            status = match.group(2)
            if hdr == hs256_header and status == "200":
                found_200 = True
            if hdr == none_header and status == "403":
                found_403 = True

    assert found_200, "Did not find expected audit log entry for valid JWT (200)"
    assert found_403, "Did not find expected audit log entry for vulnerable JWT (403)"