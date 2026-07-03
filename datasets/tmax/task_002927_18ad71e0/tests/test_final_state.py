# test_final_state.py

import os
import random
import string
import subprocess
import urllib.request
import json
import time
import pytest

def test_config_files_updated():
    # Check /app/api/.env
    env_path = "/app/api/.env"
    assert os.path.isfile(env_path), f"{env_path} does not exist."
    with open(env_path, "r") as f:
        env_content = f.read()
        assert "REDIS_PORT=6379" in env_content, "REDIS_PORT not updated to 6379 in /app/api/.env"
        assert "REDIS_CHANNEL=math_jobs" in env_content, "REDIS_CHANNEL not updated to math_jobs in /app/api/.env"

    # Check /app/worker/config.ini
    config_path = "/app/worker/config.ini"
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        config_content = f.read()
        assert "queue_channel=math_jobs" in config_content, "queue_channel not updated to math_jobs in /app/worker/config.ini"

def test_fuzz_equivalence():
    agent_bin = "/app/worker/math_worker"
    oracle_bin = "/app/oracle/reference_worker.py"

    assert os.path.isfile(agent_bin), f"Compiled worker {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Compiled worker {agent_bin} is not executable."
    assert os.path.isfile(oracle_bin), f"Oracle script {oracle_bin} does not exist."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    # Run a subset to avoid excessive test duration, but enough to verify correctness
    N = 1000 
    for i in range(N):
        length = random.randint(1, 1024)
        test_input = ''.join(random.choices(charset, k=length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                ["python3", oracle_bin, test_input],
                capture_output=True, text=True, check=True, timeout=2
            )
            expected_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {test_input}: {e.stderr}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_bin, test_input],
                capture_output=True, text=True, check=True, timeout=2
            )
            actual_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary crashed or failed on input {test_input}: {e.stderr}")

        assert actual_output == expected_output, (
            f"Mismatch on input: {test_input[:50]}...\n"
            f"Expected: {expected_output}\n"
            f"Got: {actual_output}"
        )

def test_end_to_end_flow():
    # Test the API endpoint
    url = "http://127.0.0.1:3000/compute"
    test_input = "testE2Eflow123"

    # Get expected from oracle
    oracle_bin = "/app/oracle/reference_worker.py"
    try:
        oracle_res = subprocess.run(
            ["python3", oracle_bin, test_input],
            capture_output=True, text=True, check=True, timeout=2
        )
        expected_output = oracle_res.stdout.strip()
    except Exception as e:
        pytest.fail(f"Could not run oracle for E2E test: {e}")

    data = json.dumps({"input": test_input}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    max_retries = 5
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                res_body = response.read().decode('utf-8')
                res_json = json.loads(res_body)

                # Depending on the API implementation, it might return the result directly or in a field
                # We'll check if the expected output is anywhere in the response JSON
                assert expected_output in res_body, (
                    f"Expected result {expected_output} not found in API response: {res_body}"
                )
                return
        except urllib.error.URLError as e:
            time.sleep(1)
            if attempt == max_retries - 1:
                pytest.fail(f"Failed to connect to API at {url} or API returned error: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during API request: {e}")