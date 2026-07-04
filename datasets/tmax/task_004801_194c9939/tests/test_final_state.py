# test_final_state.py

import os
import json
import random
import string
import subprocess
import base64
import urllib.request
import urllib.error
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import time

def test_nginx_routing():
    """Test that Nginx routes /auth/ to 8081 and /data/ to 8082."""

    class AuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"AUTH_OK")

    class DataHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"DATA_OK")

    auth_server = HTTPServer(('127.0.0.1', 8081), AuthHandler)
    data_server = HTTPServer(('127.0.0.1', 8082), DataHandler)

    Thread(target=auth_server.serve_forever, daemon=True).start()
    Thread(target=data_server.serve_forever, daemon=True).start()

    # Reload Nginx to ensure it picks up changes
    subprocess.run(["nginx", "-s", "reload"], capture_output=True)
    time.sleep(1)

    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/auth/test", timeout=2)
        assert req.read() == b"AUTH_OK", "Nginx did not correctly proxy /auth/ to Auth Service"

        req = urllib.request.urlopen("http://127.0.0.1:8080/data/test", timeout=2)
        assert req.read() == b"DATA_OK", "Nginx did not correctly proxy /data/ to Data Service"
    except urllib.error.URLError as e:
        assert False, f"Nginx routing failed: {e}"
    finally:
        auth_server.shutdown()
        data_server.shutdown()

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def generate_fuzz_inputs(n=5000):
    random.seed(42)
    inputs = []

    algs = ["none", "NONE", "", "HS256", "RS256", "invalid"]

    for _ in range(n):
        # Generate header
        if random.random() < 0.1:
            header_b64 = "malformed_header_not_base64!!"
        else:
            alg = random.choice(algs)
            if random.random() < 0.1:
                header_json = "{" + f'"alg": "{alg}"' # missing closing brace
            else:
                header_json = json.dumps({"alg": alg, "typ": "JWT"})
            header_b64 = b64url_encode(header_json.encode('utf-8'))

        payload_b64 = b64url_encode(b'{"sub": "1234567890", "name": "John Doe", "iat": 1516239022}')
        signature_b64 = b64url_encode(b'signature')

        if random.random() < 0.1:
            jwt = f"{header_b64}.{payload_b64}" # missing signature
        else:
            jwt = f"{header_b64}.{payload_b64}.{signature_b64}"

        auth_header = f"Bearer {jwt}"
        if random.random() < 0.05:
            auth_header = jwt # missing Bearer

        # Generate body
        body_parts = []
        for _ in range(random.randint(1, 5)):
            choice = random.random()
            if choice < 0.3:
                # SSN
                body_parts.append(f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}")
            elif choice < 0.6:
                # CC
                body_parts.append(f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}")
            else:
                # Random words
                body_parts.append(''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 10))))

        body = " ".join(body_parts)

        inputs.append(json.dumps({"auth_header": auth_header, "response_body": body}))

    return inputs

def test_auditor_fuzz_equivalence():
    """Fuzz equivalence test for the auditor binary."""
    agent_bin = "/app/auditor"
    oracle_bin = "/opt/oracle/auditor"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    if not os.path.isfile(oracle_bin):
        # If oracle is not present (e.g. local testing), skip or fail gracefully
        # In the verifier environment, this will be present.
        return

    inputs = generate_fuzz_inputs(5000)

    for i, inp in enumerate(inputs):
        inp_bytes = (inp + "\n").encode('utf-8')

        try:
            agent_proc = subprocess.run([agent_bin], input=inp_bytes, capture_output=True, timeout=1)
            agent_out = agent_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            assert False, f"Agent binary timed out on input: {inp}"

        try:
            oracle_proc = subprocess.run([oracle_bin], input=inp_bytes, capture_output=True, timeout=1)
            oracle_out = oracle_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            assert False, f"Oracle binary timed out on input: {inp}"

        assert agent_out == oracle_out, (
            f"Mismatch on input {i}:\n"
            f"Input:  {inp}\n"
            f"Oracle: {oracle_out}\n"
            f"Agent:  {agent_out}"
        )