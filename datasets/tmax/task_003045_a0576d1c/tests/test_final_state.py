# test_final_state.py

import os
import json
import subprocess
import urllib.request
import urllib.error
import random
import string
import time
import pytest

def test_schema_json_patched():
    schema_path = "/app/schema.json"
    assert os.path.isfile(schema_path), f"Schema file {schema_path} does not exist."
    with open(schema_path, "r") as f:
        try:
            schema = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Schema file {schema_path} is not valid JSON.")

    properties = schema.get("properties", {})
    assert "email" in properties, "Schema is missing the 'email' property."
    assert "api_key" in properties, "Schema is missing the 'api_key' property."

def test_gateway_conf_updated():
    conf_path = "/app/gateway.conf"
    assert os.path.isfile(conf_path), f"Gateway config {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert 'REDACTOR_CMD="/home/user/redactor"' in content, (
        f"Gateway config does not correctly set REDACTOR_CMD. Content:\n{content}"
    )

def test_redactor_executable():
    redactor_path = "/home/user/redactor"
    assert os.path.isfile(redactor_path), f"Redactor script {redactor_path} does not exist."
    assert os.access(redactor_path, os.X_OK), f"Redactor script {redactor_path} is not executable."

def generate_random_value():
    length = random.randint(1, 15)
    res = ""
    for _ in range(length):
        choice = random.choice(["char", "escaped_space", "escaped_backslash"])
        if choice == "char":
            res += random.choice(string.ascii_letters + string.digits)
        elif choice == "escaped_space":
            res += "\\ "
        elif choice == "escaped_backslash":
            res += "\\\\"
    return res if res else "val"

def generate_fuzz_inputs(n=5000):
    random.seed(42)
    lines = []
    for _ in range(n):
        timestamp = f"[2023-10-10T12:{random.randint(10,59)}:{random.randint(10,59)}]"
        ip = f"192.168.1.{random.randint(1,255)}"
        num_pairs = random.randint(0, 10)
        has_secret = random.random() < 0.5

        pairs = []
        secret_inserted = False
        for i in range(num_pairs):
            if has_secret and not secret_inserted and (i == num_pairs // 2 or num_pairs == 1):
                key = "secret_token"
                secret_inserted = True
            else:
                key = "".join(random.choices(string.ascii_letters, k=random.randint(3, 8)))
                if key == "secret_token":
                    key = "other_token"

            val = generate_random_value()
            pairs.append(f"{key}={val}")

        if has_secret and not secret_inserted:
            pairs.append(f"secret_token={generate_random_value()}")

        line = f"{timestamp} {ip}"
        if pairs:
            line += " " + " ".join(pairs)
        lines.append(line)
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_redactor"
    agent_path = "/home/user/redactor"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}."
    assert os.path.isfile(agent_path), f"Agent program missing at {agent_path}."

    fuzz_input = generate_fuzz_inputs(5000)

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_path],
            input=fuzz_input,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to run:\n{e.stderr}")

    # Run agent
    try:
        agent_proc = subprocess.run(
            [agent_path],
            input=fuzz_input,
            text=True,
            capture_output=True,
            check=True
        )
        agent_output = agent_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent redactor failed to run:\n{e.stderr}")

    if oracle_output != agent_output:
        oracle_lines = oracle_output.splitlines()
        agent_lines = agent_output.splitlines()
        input_lines = fuzz_input.splitlines()

        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                pytest.fail(
                    f"Mismatch at line {i+1}:\n"
                    f"Input:  {input_lines[i]}\n"
                    f"Oracle: {o_line}\n"
                    f"Agent:  {a_line}\n"
                )

        # If lengths differ
        pytest.fail(f"Output line counts differ. Oracle: {len(oracle_lines)}, Agent: {len(agent_lines)}")

def test_end_to_end_flow():
    # Wait a bit in case services are still starting
    time.sleep(2)

    url = "http://127.0.0.1:8000/api"
    payload = json.dumps({
        "email": "test@test.com",
        "api_key": "123",
        "secret_token": "super\\ secret\\ password"
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            assert status == 200, f"Expected HTTP 200, got {status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to gateway or backend returned error: {e}")

    # Check log file
    log_path = "/home/user/gateway.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    # Needs a moment to flush
    time.sleep(1)

    with open(log_path, "r") as f:
        logs = f.read()

    assert "secret_token=***" in logs, "The log file does not contain the redacted secret_token=***."
    assert "super\\ secret\\ password" not in logs, "The literal secret_token value was found in the logs!"