# test_final_state.py

import os
import subprocess
import random
import string
import hmac
import hashlib
import urllib.request
import urllib.error
import ssl
import pytest

def test_infrastructure_certs_exist():
    assert os.path.isfile("/home/user/certs/tls.crt"), "TLS certificate missing at /home/user/certs/tls.crt"
    assert os.path.isfile("/home/user/certs/tls.key"), "TLS private key missing at /home/user/certs/tls.key"

def test_infrastructure_nginx_conf_exists():
    assert os.path.isfile("/home/user/nginx.conf"), "Nginx config missing at /home/user/nginx.conf"

def test_infrastructure_nginx_proxy():
    # Bypass self-signed cert validation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request("https://127.0.0.1:8443/log", method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert "Log received" in body, f"Expected 'Log received' in response, got {body}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy on port 8443: {e}")

def test_fuzz_equivalence_log_normalizer():
    agent_script = "/home/user/log_normalizer.py"
    oracle_script = "/app/oracle_normalizer.py"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing at {oracle_script}"

    random.seed(42)
    key = b'COMPLIANCE_KEY_2024'

    lines = []
    for _ in range(1000):
        msg_len = random.randint(10, 200)
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=msg_len))

        if random.choice([True, False]):
            mac = hmac.new(key, msg.encode('utf-8'), hashlib.sha256).hexdigest()
        else:
            mac = ''.join(random.choices("0123456789abcdef", k=64))

        lines.append(f"{mac}:{msg}")

    input_data = "\n".join(lines) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        ["python3", oracle_script],
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error: {agent_proc.stderr}"

    agent_output = agent_proc.stdout

    oracle_lines = oracle_output.splitlines()
    agent_lines = agent_output.splitlines()

    assert len(agent_lines) == len(oracle_lines), f"Expected {len(oracle_lines)} lines of output, got {len(agent_lines)}"

    for i, (expected, actual) in enumerate(zip(oracle_lines, agent_lines)):
        if expected != actual:
            pytest.fail(f"Mismatch on line {i+1}.\nInput: {lines[i]}\nExpected: {expected}\nGot: {actual}")