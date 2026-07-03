# test_final_state.py

import os
import subprocess
import json
import hashlib
import random
import string
import base64
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import jwt
from cryptography.hazmat.primitives import serialization

def get_file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def generate_fuzz_inputs():
    private_key_path = "/app/certs/private.pem"
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    config_path = "/app/data/critical_config.json"
    correct_hash = get_file_hash(config_path)

    inputs = []
    random.seed(42)

    # Generate 500 inputs total for test efficiency
    for _ in range(100):
        # 1. Random strings
        length = random.randint(10, 500)
        inputs.append(''.join(random.choices(string.ascii_letters + string.digits, k=length)))

        # 2. Well-formed invalid signatures
        payload = {"file_hash": correct_hash, "rand": random.randint(1, 10000)}
        token = jwt.encode(payload, "wrong_secret", algorithm="HS256")
        inputs.append(token)

        # 3. alg=none
        header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode('utf-8').rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode('utf-8').rstrip('=')
        inputs.append(f"{header}.{payload_b64}.")

        # 4. Valid sig, invalid file_hash
        bad_payload = {"file_hash": "badhash123", "rand": random.randint(1, 10000)}
        token = jwt.encode(bad_payload, private_key, algorithm="RS256")
        inputs.append(token)

        # 5. Fully valid
        good_payload = {"file_hash": correct_hash, "rand": random.randint(1, 10000)}
        token = jwt.encode(good_payload, private_key, algorithm="RS256")
        inputs.append(token)

    return inputs

def test_fuzz_equivalence():
    agent_script = "/home/user/verify_token.py"
    oracle_bin = "/app/oracle/token_validator_bin"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    inputs = generate_fuzz_inputs()

    for i, token in enumerate(inputs):
        # Run oracle
        oracle_proc = subprocess.run([oracle_bin], input=token.encode(), capture_output=True)
        oracle_out = oracle_proc.stdout.decode().strip()

        # Run agent
        agent_proc = subprocess.run(["python3", agent_script], input=token.encode(), capture_output=True)
        agent_out = agent_proc.stdout.decode().strip()

        assert agent_out == oracle_out, f"Mismatch on input {i}:\nInput: {token}\nOracle: {oracle_out}\nAgent: {agent_out}"

class DummyBackend(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BACKEND_SECRET")

def test_integration():
    # Start dummy backend on 9000
    server = HTTPServer(('127.0.0.1', 9000), DummyBackend)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    time.sleep(1)

    private_key_path = "/app/certs/private.pem"
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    config_path = "/app/data/critical_config.json"
    correct_hash = get_file_hash(config_path)

    valid_payload = {"file_hash": correct_hash}
    valid_token = jwt.encode(valid_payload, private_key, algorithm="RS256")

    # 1. No auth header
    req = urllib.request.Request("http://127.0.0.1:8080/")
    try:
        urllib.request.urlopen(req)
        assert False, "Expected 401 for missing auth"
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401, got {e.code}"

    # 2. Invalid auth header (alg=none)
    header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode('utf-8').rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(valid_payload).encode()).decode('utf-8').rstrip('=')
    bad_token = f"{header}.{payload_b64}."

    req = urllib.request.Request("http://127.0.0.1:8080/")
    req.add_header("Authorization", f"Bearer {bad_token}")
    try:
        urllib.request.urlopen(req)
        assert False, "Expected 401 for alg=none"
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401, got {e.code}"

    # 3. Valid token
    req = urllib.request.Request("http://127.0.0.1:8080/")
    req.add_header("Authorization", f"Bearer {valid_token}")
    try:
        resp = urllib.request.urlopen(req)
        assert resp.code == 200, f"Expected 200, got {resp.code}"
        body = resp.read().decode()
        assert "BACKEND_SECRET" in body, "Did not receive backend response"
    except urllib.error.HTTPError as e:
        assert False, f"Expected 200 for valid token, got {e.code}"

    server.shutdown()
    server.server_close()