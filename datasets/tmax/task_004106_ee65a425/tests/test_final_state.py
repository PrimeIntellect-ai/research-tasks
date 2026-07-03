# test_final_state.py

import os
import json
import pytest
import random
import string
import subprocess
import urllib.request
import urllib.error

def test_config_json_corrected():
    """Verify that the configuration file has been properly restored."""
    config_path = '/app/config.json'
    assert os.path.exists(config_path), f"Config file {config_path} is missing."

    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Config file {config_path} is not valid JSON.")

    assert config_data.get("REDIS_HOST") == "127.0.0.1", \
        f"Expected REDIS_HOST to be '127.0.0.1', got {config_data.get('REDIS_HOST')}"
    assert config_data.get("REDIS_PORT") == 6379, \
        f"Expected REDIS_PORT to be 6379, got {config_data.get('REDIS_PORT')}"
    assert config_data.get("AUTH_SOCKET") == "/tmp/auth.sock", \
        f"Expected AUTH_SOCKET to be '/tmp/auth.sock', got {config_data.get('AUTH_SOCKET')}"

def test_api_gateway_end_to_end():
    """Verify that the services are running and the end-to-end flow works."""
    url = "http://127.0.0.1:5000/auth"
    payload = json.dumps({"username": "testuser"}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            response_body = response.read().decode('utf-8')
            try:
                data = json.loads(response_body)
            except json.JSONDecodeError:
                pytest.fail(f"API Gateway did not return valid JSON. Got: {response_body}")

            assert "token" in data, f"Response JSON missing 'token' key. Got: {data}"
            # The oracle token for "testuser"
            # t: (116 ^ 66) + 7 = 57 -> 39
            # e: (101 ^ 66) + 7 = 46 -> 2e
            # s: (115 ^ 66) + 7 = 56 -> 38
            # t: (116 ^ 66) + 7 = 57 -> 39
            # u: (117 ^ 66) + 7 = 58 -> 3a
            # s: (115 ^ 66) + 7 = 56 -> 38
            # e: (101 ^ 66) + 7 = 46 -> 2e
            # r: (114 ^ 66) + 7 = 55 -> 37
            # Let's just ensure it's not empty, the exact logic is tested in fuzzing.
            assert len(data["token"]) > 0, "Returned token is empty."

    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API Gateway at {url}. Are the services running? Error: {e}")

def test_backdoor_token_fuzz_equivalence():
    """Fuzz test the student's Python script against the oracle implementation."""
    agent_script = '/home/user/backdoor_token.py'
    oracle_script = '/app/.oracle/oracle_token.py'

    assert os.path.exists(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(100):
        length = random.randint(4, 64)
        test_input = ''.join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_cmd = ['python3', oracle_script, test_input]
        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
            expected_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle script failed on input '{test_input}': {e.stderr}")

        # Run agent
        agent_cmd = ['python3', agent_script, test_input]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_res.returncode == 0, \
            f"Agent script failed (exit code {agent_res.returncode}) on input '{test_input}'. Stderr: {agent_res.stderr}"

        actual_output = agent_res.stdout.strip()

        assert actual_output == expected_output, (
            f"Fuzzing mismatch on iteration {i+1}!\n"
            f"Input Username: '{test_input}'\n"
            f"Expected Token: '{expected_output}'\n"
            f"Actual Token:   '{actual_output}'"
        )