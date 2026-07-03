# test_final_state.py
import os
import json
import time
import subprocess
import pytest

def test_new_token_saved():
    token_path = "/home/user/new_token.txt"
    assert os.path.isfile(token_path), f"The file {token_path} is missing."

    with open(token_path, "r") as f:
        token = f.read().strip()

    expected_token = "TOK_abc123_Secure"
    assert expected_token in token, f"The file {token_path} does not contain the expected rotated token. Found: {token}"

def test_service_config_csp():
    config_path = "/app/service_config.json"
    assert os.path.isfile(config_path), f"The file {config_path} is missing."

    with open(config_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {config_path} does not contain valid JSON.")

    assert "csp" in data, "The 'csp' key is missing from the JSON root in /app/service_config.json."

    expected_csp = "default-src 'self'; script-src 'none'; object-src 'none';"
    assert data["csp"] == expected_csp, f"The 'csp' value is incorrect. Expected: {expected_csp}, Got: {data['csp']}"

def test_fast_audit_performance():
    script_path = "/home/user/fast_audit.py"
    assert os.path.isfile(script_path), f"The auditing script {script_path} is missing."

    start = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    end = time.time()

    duration = end - start

    assert result.returncode == 0, f"The script {script_path} failed to execute. Error: {result.stderr}"
    assert "5000" in result.stdout, f"The script did not output '5000' indicating successful responses. Output: {result.stdout}"

    threshold = 2.0
    assert duration <= threshold, f"Performance test failed: Execution time was {duration:.2f} seconds, which exceeds the threshold of {threshold} seconds."