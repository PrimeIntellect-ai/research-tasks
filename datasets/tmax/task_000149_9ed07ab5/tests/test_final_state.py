# test_final_state.py

import os
import subprocess
import random
import string
import base64
import json
import pytest

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + "/.-_", k=length))

def generate_random_path():
    paths = [
        "/var/lib/isolated_sandbox/test.txt",
        "/var/lib/isolated_sandbox/../test.txt",
        "../../../etc/passwd",
        "/etc/passwd",
        "/var/run/../app/restricted",
        "valid_file.txt",
        "/var/lib/isolated_sandbox/subdir/file.txt"
    ]
    if random.random() < 0.5:
        return random.choice(paths)
    return generate_random_string(random.randint(5, 50))

def generate_random_token():
    if random.random() < 0.3:
        # Malformed base64
        return generate_random_string(random.randint(10, 100))

    # Generate some JSON
    data = {
        "signature": generate_random_string(32),
        "cert_chain": [generate_random_string(20) for _ in range(random.randint(0, 3))],
        "claims": {
            "file_access": generate_random_path(),
            "exp": random.randint(1000000000, 2000000000)
        }
    }

    if random.random() < 0.2:
        # Invalid JSON
        json_str = json.dumps(data) + "{"
    else:
        json_str = json.dumps(data)

    return base64.b64encode(json_str.encode()).decode()

def test_agent_binary_exists():
    agent_path = "/home/user/policy_evaluator"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_evaluator"
    agent_path = "/home/user/policy_evaluator"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"

    random.seed(42)

    # Run 1000 iterations to avoid timeout while still providing strong assurance
    N = 1000

    for i in range(N):
        token = generate_random_token()
        path = generate_random_path()

        oracle_proc = subprocess.run(
            [oracle_path, token, path],
            capture_output=True,
            text=True
        )

        agent_proc = subprocess.run(
            [agent_path, token, path],
            capture_output=True,
            text=True
        )

        oracle_stdout = oracle_proc.stdout.strip()
        agent_stdout = agent_proc.stdout.strip()

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Exit code mismatch on iteration {i}.\n"
            f"Token: {token}\n"
            f"Path: {path}\n"
            f"Oracle exit code: {oracle_proc.returncode}, Agent exit code: {agent_proc.returncode}\n"
            f"Oracle stdout: {oracle_stdout}\n"
            f"Agent stdout: {agent_stdout}"
        )

        assert oracle_stdout == agent_stdout, (
            f"Stdout mismatch on iteration {i}.\n"
            f"Token: {token}\n"
            f"Path: {path}\n"
            f"Oracle stdout: {oracle_stdout}\n"
            f"Agent stdout: {agent_stdout}"
        )