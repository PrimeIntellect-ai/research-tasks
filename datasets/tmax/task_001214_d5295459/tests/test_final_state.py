# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/log_anomaly_detector"
AGENT_SCRIPT = "/home/user/anomaly_detector.py"
NUM_ITERATIONS = 100

def generate_log_file(path, seed):
    random.seed(seed)
    num_lines = random.randint(10, 500)

    timestamp = 1600000000

    methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
    http_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
    status_codes = [200, 301, 400, 403, 404, 500]

    with open(path, 'w') as f:
        for _ in range(num_lines):
            timestamp += random.randint(1, 100)
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            method = random.choice(methods)
            url_path = f"/api/v1/resource_{random.randint(1, 100)}"
            version = random.choice(http_versions)
            status = random.choice(status_codes)
            size = random.randint(0, 50000)

            # 2% chance of malformed line
            is_malformed = random.random() < 0.02

            if is_malformed:
                # randomly drop status or size
                if random.choice([True, False]):
                    line = f"[{timestamp}] {ip} {method} {url_path} {version} {status}\n"
                else:
                    line = f"[{timestamp}] {ip} {method} {url_path} {version}\n"
            else:
                line = f"[{timestamp}] {ip} {method} {url_path} {version} {status} {size}\n"

            f.write(line)

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "input.log")

        for i in range(NUM_ITERATIONS):
            generate_log_file(input_file, seed=42 + i)

            # Run oracle
            try:
                oracle_result = subprocess.run(
                    [ORACLE_PATH, input_file],
                    capture_output=True,
                    text=True,
                    check=True
                )
                oracle_output = oracle_result.stdout
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on iteration {i} with error:\n{e.stderr}")

            # Run agent
            try:
                agent_result = subprocess.run(
                    ["python3", AGENT_SCRIPT, input_file],
                    capture_output=True,
                    text=True,
                    check=True
                )
                agent_output = agent_result.stdout
            except subprocess.CalledProcessError as e:
                with open(input_file, 'r') as f:
                    input_content = f.read()
                pytest.fail(f"Agent script failed on iteration {i} with error:\n{e.stderr}\n\nInput:\n{input_content}")

            if oracle_output != agent_output:
                with open(input_file, 'r') as f:
                    input_content = f.read()
                pytest.fail(
                    f"Output mismatch on iteration {i}.\n\n"
                    f"--- Input ---\n{input_content}\n"
                    f"--- Oracle Output ---\n{oracle_output}\n"
                    f"--- Agent Output ---\n{agent_output}\n"
                )