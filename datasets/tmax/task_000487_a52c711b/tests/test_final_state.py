# test_final_state.py

import os
import subprocess
import random
import string
import urllib.request
import time
import pytest

ORACLE_PATH = "/app/bin/obfuscated_logger"
AGENT_SCRIPT = "/home/user/clean_logger.py"
VERIFIED_LOGS_PATH = "/home/user/verified_logs.txt"

def generate_random_string(min_len=10, max_len=500):
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(chars) for _ in range(length))

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(1000):
        test_input = generate_random_string()

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH, test_input],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input!r}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT, test_input],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input: {test_input!r}\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout

        assert agent_out == oracle_out, (
            f"Mismatch on iteration {i}.\n"
            f"Input: {test_input!r}\n"
            f"Expected (Oracle): {oracle_out!r}\n"
            f"Got (Agent): {agent_out!r}"
        )

def test_integration_flow():
    # Clear the verified logs file if it exists
    if os.path.exists(VERIFIED_LOGS_PATH):
        os.remove(VERIFIED_LOGS_PATH)

    random.seed(123)
    test_messages = [generate_random_string(20, 50) for _ in range(5)]

    # Send messages via HTTP POST
    for msg in test_messages:
        req = urllib.request.Request(
            "http://localhost:8080/log",
            data=msg.encode('utf-8'),
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status in (200, 201, 202, 204), f"Unexpected HTTP status: {response.status}"
        except Exception as e:
            pytest.fail(f"Failed to send POST request to Nginx: {e}")

    # Wait for the backend worker to process the messages
    time.sleep(2)

    assert os.path.exists(VERIFIED_LOGS_PATH), f"Verified logs file not created at {VERIFIED_LOGS_PATH}"

    with open(VERIFIED_LOGS_PATH, "r") as f:
        content = f.read().splitlines()

    assert len(content) == len(test_messages), (
        f"Expected {len(test_messages)} lines in {VERIFIED_LOGS_PATH}, got {len(content)}"
    )

    for expected, actual in zip(test_messages, content):
        assert expected == actual, f"Expected log line {expected!r}, got {actual!r}"