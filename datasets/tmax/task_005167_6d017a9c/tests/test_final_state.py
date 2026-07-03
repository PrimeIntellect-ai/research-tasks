# test_final_state.py

import os
import re
import json
import subprocess
import time
import requests
import pytest

def test_orchestrator_exists_and_executable():
    path = "/home/user/orchestrator.sh"
    assert os.path.isfile(path), f"{path} is missing"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_pipeline_execution_and_server_response():
    # 1. Update vars.env
    vars_env_path = "/home/user/vars.env"
    with open(vars_env_path, "a") as f:
        f.write("\nREGION=us-east-1\n")

    # 2. Run orchestrator.sh
    result = subprocess.run(
        ["su", "user", "-c", "/home/user/orchestrator.sh"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"orchestrator.sh failed with exit code {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"

    # Wait a moment for the server to start
    time.sleep(1)

    # 3. Make HTTP request
    try:
        response = requests.get("http://127.0.0.1:8080/", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    # 4. Check JSON response
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    expected_data = {
        "database": "postgresql://db.example.com:5432/mydb",
        "auth": {
            "key": "secret_123",
            "region": "us-east-1"
        }
    }

    assert data == expected_data, f"JSON response did not match expected.\nExpected: {expected_data}\nGot: {data}"

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"{log_path} is missing"

    with open(log_path, "r") as f:
        content = f.read()

    # The verifier checks /home/user/pipeline.log for the regex: 
    # `\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Pipeline run complete\. Config generated\.`
    pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Pipeline run complete\. Config generated\."
    assert re.search(pattern, content), f"Could not find the expected log entry in {log_path}. Content:\n{content}"