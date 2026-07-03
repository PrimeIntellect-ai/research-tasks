# test_final_state.py
import os
import json
import random
import string
import subprocess
import urllib.request
import urllib.parse
import pytest

ORACLE_PATH = "/opt/oracle/backend_server_oracle"
AGENT_PATH = "/home/user/app/backend/backend_server"
CONFIG_PATH = "/home/user/app/gateway/config.json"
N_FUZZ = 1000  # Reduced from 5000 to avoid excessive test duration, but high enough for confidence

def test_config_fixed():
    assert os.path.exists(CONFIG_PATH), f"Config file missing at {CONFIG_PATH}"
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    assert config.get("backend_url") == "http://localhost:9090", "backend_url not correctly updated in config.json"
    assert config.get("rate_limit_rps") == 100, "rate_limit_rps not correctly updated in config.json"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}. Did you fix the Makefile and compile?"

    random.seed(42)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

    for _ in range(N_FUZZ):
        length = random.randint(16, 256)
        test_input = "".join(random.choice(charset) for _ in range(length))

        # Run Oracle
        oracle_cmd = [ORACLE_PATH, "--cli", test_input]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}"
        oracle_output = oracle_proc.stdout

        # Run Agent
        agent_cmd = [AGENT_PATH, "--cli", test_input]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent binary failed or crashed on input: {test_input}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Mismatch found!\n"
            f"Input: {test_input}\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output: {agent_output}"
        )

def test_gateway_end_to_end():
    # Test a single request through the API gateway to ensure it's up and proxying
    test_input = "EndToEndTestString123!"
    encoded_input = urllib.parse.quote(test_input)
    url = f"http://localhost:8080/api/v1/process?data={encoded_input}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            agent_http_output = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to reach Go gateway or gateway returned error: {e}")

    # Compare with oracle
    oracle_cmd = [ORACLE_PATH, "--cli", test_input]
    oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
    oracle_output = oracle_proc.stdout

    assert agent_http_output == oracle_output, (
        f"Gateway End-to-End Mismatch!\n"
        f"Oracle output: {oracle_output}\n"
        f"Gateway output: {agent_http_output}"
    )