# test_final_state.py
import os
import subprocess
import random
import base64
import urllib.parse
import urllib.request
import time
import pytest

ORACLE_PATH = "/opt/oracle/decoder_oracle"
AGENT_PROGRAM = "/home/user/decoder"
ITERATIONS = 100

def generate_random_input():
    target_id = chr(random.randint(65, 90)) # A-Z
    num_commands = random.randint(1, 15)

    raw_bytes = bytearray()
    for _ in range(num_commands):
        cmd_type = random.choice(['I', 'D', 'R'])
        if cmd_type == 'I':
            raw_bytes.extend(b'I' + bytes([random.randint(32, 126)]))
        elif cmd_type == 'D':
            raw_bytes.extend(b'D\x00')
        elif cmd_type == 'R':
            raw_bytes.extend(b'R' + bytes([random.randint(32, 126)]))

    b64_encoded = base64.b64encode(raw_bytes)
    url_encoded = urllib.parse.quote(b64_encoded)

    return f"patch://{target_id}/{url_encoded}"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PROGRAM), f"Agent program missing at {AGENT_PROGRAM}"

    random.seed(42)

    for i in range(ITERATIONS):
        test_input = generate_random_input()

        oracle_proc = subprocess.run(
            [ORACLE_PATH, test_input], 
            capture_output=True, text=True
        )

        agent_proc = subprocess.run(
            [AGENT_PROGRAM, test_input], 
            capture_output=True, text=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on input {test_input}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        assert agent_proc.stdout == oracle_proc.stdout, \
            f"Stdout mismatch on input {test_input}.\nOracle output: {oracle_proc.stdout}\nAgent output: {agent_proc.stdout}"

def test_end_to_end_service():
    # Ensure services are running (start.sh should have been run by the agent, but we can't guarantee it's still running in the test environment, so we just test the endpoints if they are up)
    # We will trigger the curl command

    test_input_remainder = "Z/SVoASWw="
    url = f"http://localhost:8080/process/{test_input_remainder}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx or Flask pipeline: {e}")

    # Check if redis has it
    try:
        redis_proc = subprocess.run(
            ["redis-cli", "get", "latest_patch"],
            capture_output=True, text=True, check=True
        )
        redis_val = redis_proc.stdout.strip()
    except Exception as e:
        pytest.fail(f"Failed to get value from redis: {e}")

    # We don't assert the exact string because the oracle might be a dummy or real, 
    # but we assert that the HTTP response matches what's in Redis.
    assert body == redis_val, f"HTTP response '{body}' does not match Redis value '{redis_val}'"
    assert "TARGET=" in body and "RESULT=" in body, f"Unexpected response format: {body}"