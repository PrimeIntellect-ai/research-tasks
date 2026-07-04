# test_final_state.py

import os
import re
import json
import base64
import random
import string
import subprocess
import time
import pytest
import hmac
import hashlib

def create_valid_token(payload, secret="secret_key_123"):
    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode('utf-8').rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').rstrip('=')
    msg = f"{header}.{payload_b64}"
    sig = hmac.new(secret.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode('utf-8').rstrip('=')
    return f"{msg}.{sig_b64}"

def create_none_token(payload):
    header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode('utf-8').rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').rstrip('=')
    return f"{header}.{payload_b64}."

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + "-_.", k=length))

def generate_fuzz_inputs(n=10000):
    random.seed(42)
    inputs = []
    for _ in range(n):
        choice = random.random()
        if choice < 0.1:
            inputs.append(create_valid_token({"user": "admin", "rand": random.randint(1, 10000)}))
        elif choice < 0.2:
            inputs.append(create_none_token({"user": "admin", "rand": random.randint(1, 10000)}))
        elif choice < 0.3:
            tok = create_valid_token({"user": "admin", "rand": random.randint(1, 10000)})
            inputs.append(tok.rsplit('.', 1)[0]) # Missing signature
        elif choice < 0.5:
            inputs.append(random_string(random.randint(10, 500)))
        else:
            # Malformed base64 or random parts
            parts = [random_string(random.randint(10, 50)) for _ in range(random.randint(1, 4))]
            inputs.append(".".join(parts))
    return inputs

@pytest.mark.timeout(60)
def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/token_verifier"
    agent_script = "/home/user/app/auth.py"

    assert os.path.exists(oracle_path), "Oracle binary not found."
    assert os.path.exists(agent_script), "Agent script not found."

    inputs = generate_fuzz_inputs(1000) # Using 1000 to avoid excessive test duration, but representative

    for token in inputs:
        oracle_proc = subprocess.run([oracle_path, token], capture_output=True, text=True)
        agent_proc = subprocess.run(["python3", agent_script, token], capture_output=True, text=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on token: {token}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/app/nginx.conf"
    assert os.path.exists(nginx_conf_path), "nginx.conf not found."

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    assert re.search(r"listen\s+8080\s*;", content), "Nginx is not configured to listen on port 8080."
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:5000/?\s*;", content), "Nginx is not proxying to http://127.0.0.1:5000."

def test_flask_config_fixed():
    config_path = "/home/user/app/config.py"
    assert os.path.exists(config_path), "config.py not found."

    with open(config_path, "r") as f:
        content = f.read()

    assert re.search(r"REDIS_PORT\s*=\s*6379", content), "Flask config REDIS_PORT is not 6379."
    assert re.search(r"REDIS_HOST\s*=\s*['\"]127\.0\.0\.1['\"]", content) or re.search(r"REDIS_HOST\s*=\s*['\"]localhost['\"]", content), "Flask config REDIS_HOST is not 127.0.0.1."

def test_worker_redaction_logic():
    worker_path = "/home/user/app/worker.py"
    assert os.path.exists(worker_path), "worker.py not found."

    with open(worker_path, "r") as f:
        content = f.read()

    # Check if a regex substitution for SSN is present
    assert re.search(r"\*\*\*-\*\*", content), "Worker does not seem to contain SSN redaction replacement string '***-**-'."
    assert "re.sub" in content, "Worker does not use re.sub for redaction."