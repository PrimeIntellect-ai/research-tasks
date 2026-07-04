# test_final_state.py

import os
import subprocess
import random
import base64
import socket
import pytest

def test_redis_conf_fixed():
    redis_conf_path = "/app/redis.conf"
    assert os.path.exists(redis_conf_path), f"File {redis_conf_path} does not exist."
    with open(redis_conf_path, "r") as f:
        content = f.read()
    assert "port 6379" in content, "Redis config was not updated to port 6379."
    assert "port 6380" not in content, "Redis config still contains port 6380."

def test_agent_script_attributes():
    path = "/home/user/log_analyzer.py"
    assert os.path.exists(path), f"Agent script {path} does not exist."
    assert os.access(path, os.X_OK), f"Agent script {path} is not executable."
    with open(path, "r") as f:
        first_line = f.readline().strip()
    assert first_line == "#!/usr/bin/env python3", f"Agent script missing correct shebang. Got: {first_line}"

def test_services_running():
    # Check if Redis is running on port 6379
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', 6379))
        assert result == 0, "Redis is not running on port 6379. Did you start the service?"

    # Check if Flask is running on port 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', 5000))
        assert result == 0, "Flask metadata service is not running on port 5000. Did you start the service?"

def test_fuzz_equivalence():
    random.seed(42)
    methods = ["GET", "POST", "PUT"]
    encodings = ["utf-8", "utf-16le", "latin-1"]

    inputs = []
    for _ in range(1000):
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        method = random.choice(methods)
        path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(3, 10)))
        bytes_ = random.randint(10, 100000)

        raw_str = f"{ip} {method} {path} {bytes_}"
        encoding = random.choice(encodings)
        encoded_bytes = raw_str.encode(encoding)
        b64_str = base64.b64encode(encoded_bytes).decode('ascii')
        inputs.append(b64_str)

    input_data = "\n".join(inputs) + "\n"

    oracle_proc = subprocess.run(
        ["/app/oracle_analyzer"],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"

    agent_proc = subprocess.run(
        ["/home/user/log_analyzer.py"],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"

    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    assert len(oracle_lines) == len(agent_lines), f"Output line count mismatch. Expected {len(oracle_lines)}, got {len(agent_lines)}."

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, (
            f"Mismatch on input {i+1}:\n"
            f"Input (base64): {inputs[i]}\n"
            f"Expected: {o_line}\n"
            f"Got:      {a_line}"
        )