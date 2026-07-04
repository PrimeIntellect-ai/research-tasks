# test_final_state.py

import os
import random
import struct
import subprocess
import urllib.request
import urllib.error
import pytest
import time

def generate_fuzz_input(valid_header=True):
    if valid_header:
        data = b"DOCW\x01"
    else:
        data = bytes(random.choices(range(256), k=5))
        if data == b"DOCW\x01":
            data = b"DOCW\x02"

    if valid_header:
        num_records = random.randint(1, 50)
        for _ in range(num_records):
            rtype = random.choice([0x01, 0x02, 0x03])
            length = random.randint(0, 1024)
            payload = bytes(random.choices(range(256), k=length))
            data += struct.pack("<BH", rtype, length) + payload
        data += b"\xFF"
    return data

def run_extractor(binary_path, input_data):
    try:
        proc = subprocess.run(
            [binary_path],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, b"", b"TIMEOUT"

def test_extractor_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_extractor"
    agent_path = "/home/user/extractor"

    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    for i in range(1000):
        valid_header = (i % 2 == 0)
        input_data = generate_fuzz_input(valid_header)

        oracle_code, oracle_stdout, oracle_stderr = run_extractor(oracle_path, input_data)
        agent_code, agent_stdout, agent_stderr = run_extractor(agent_path, input_data)

        assert agent_code == oracle_code, f"Exit code mismatch on input {i}. Expected {oracle_code}, got {agent_code}"
        assert agent_stdout == oracle_stdout, f"Stdout mismatch on input {i}. Expected {oracle_stdout}, got {agent_stdout}"

        if not valid_header:
            assert b"INVALID" in agent_stderr, f"Expected 'INVALID' in stderr for bad header, got {agent_stderr}"

def test_nginx_config_updated():
    nginx_conf_path = "/home/user/doc_system/nginx.conf"
    with open(nginx_conf_path, 'r') as f:
        content = f.read()
    assert "proxy_pass" in content, "nginx.conf missing proxy_pass directive"
    assert "127.0.0.1:5000" in content or "localhost:5000" in content, "nginx.conf proxy_pass not pointing to Flask"

def test_flask_app_updated():
    flask_app_path = "/home/user/doc_system/flask_app.py"
    with open(flask_app_path, 'r') as f:
        content = f.read()
    assert "/home/user/extractor" in content, "flask_app.py not updated to use /home/user/extractor"
    assert "/app/bin/oracle_extractor" not in content, "flask_app.py still contains reference to old oracle"

def test_services_running_and_e2e():
    # Construct a valid DocWAL file with text payload
    text_payload = b"Hello, DocWAL E2E Test!"
    docwal_data = b"DOCW\x01" + struct.pack("<BH", 0x01, len(text_payload)) + text_payload + b"\xFF"

    req = urllib.request.Request(
        "http://127.0.0.1:8080/api/upload",
        data=docwal_data,
        method="POST"
    )

    max_retries = 5
    for i in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                body = response.read()
                assert body == text_payload, f"Expected response {text_payload}, got {body}"
                return
        except urllib.error.URLError as e:
            if i == max_retries - 1:
                pytest.fail(f"E2E request failed: {e}")
            time.sleep(1)