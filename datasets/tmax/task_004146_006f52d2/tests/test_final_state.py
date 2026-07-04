# test_final_state.py

import os
import subprocess
import json
import random
import string
import pytest

def test_nginx_conf_fixed():
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, 'r') as f:
        content = f.read()
    assert "proxy_pass" in content and "5000" in content, "Nginx config missing proxy_pass to port 5000"

def test_flask_app_fixed():
    path = "/home/user/search_app.py"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, 'r') as f:
        content = f.read()
    assert "127.0.0.1" in content and "6379" in content, "Flask app not configured to connect to Redis on 127.0.0.1:6379"
    assert "dummy" not in content, "Flask app still contains dummy Redis configuration"

def generate_fuzz_input(seed):
    random.seed(seed)
    num_entries = random.randint(10, 100)
    lines = []
    for i in range(num_entries):
        req_id = random.randint(1, 10000)

        # Generate endpoint with repeating characters
        endpoint = "/"
        for _ in range(random.randint(2, 5)):
            char = random.choice(string.ascii_lowercase)
            repeat = random.randint(1, 6)
            endpoint += char * repeat

        status = random.choice([200, 404, 500])

        lines.append(f"[REQ_START] id={req_id}")
        payload = json.dumps({"endpoint": endpoint, "status": status})
        lines.append(payload)
        lines.append("[REQ_END]")

    return "\n".join(lines) + "\n"

def test_archiver_fuzz_equivalence():
    agent_script = "/home/user/archiver.py"
    oracle_bin = "/opt/doc_archiver_ref"

    assert os.path.isfile(agent_script), f"Missing agent script at {agent_script}"
    assert os.path.isfile(oracle_bin), f"Missing oracle binary at {oracle_bin}"

    for i in range(50):
        input_data = generate_fuzz_input(seed=i)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_bin],
                input=input_data.encode('utf-8'),
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {i}: {e.stderr.decode('utf-8', errors='ignore')}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_script],
                input=input_data.encode('utf-8'),
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {i}. Stderr: {e.stderr.decode('utf-8', errors='ignore')}")

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzz input {i}.\n"
            f"Input:\n{input_data}\n"
            f"Oracle output (hex): {oracle_out.hex()}\n"
            f"Agent output (hex): {agent_out.hex()}"
        )