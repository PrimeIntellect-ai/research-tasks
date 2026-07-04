# test_final_state.py

import os
import json
import subprocess

def test_payload_bin_exists_and_executable():
    path = "/home/user/payload.bin"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_payload_bin_output():
    path = "/home/user/payload.bin"
    assert os.path.isfile(path), f"File {path} is missing."

    try:
        result = subprocess.run([path], capture_output=True, text=True, timeout=2)
        output = result.stdout.strip()
        data = json.loads(output)
    except Exception as e:
        assert False, f"Failed to execute {path} or parse its output as JSON: {e}"

    assert data.get("status") == "exploited", "Payload output missing or incorrect 'status' field."
    assert data.get("env") == "staging", "Payload output 'env' should be 'staging' (compiled with MOCK_MODE)."

def test_final_report_json():
    path = "/home/user/final_report.json"
    assert os.path.isfile(path), f"File {path} is missing. The test harness did not generate it."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    assert "payload_result" in data, "final_report.json is missing 'payload_result' key."
    assert "blocked_agents" in data, "final_report.json is missing 'blocked_agents' key."

    assert data["payload_result"].get("env") == "staging", "final_report.json payload_result.env is not 'staging'."
    assert data["payload_result"].get("status") == "exploited", "final_report.json payload_result.status is not 'exploited'."

    expected_agents = ["Nmap Scripting Engine", "curl/7.68.0", "sqlmap/1.5.8.2#dev"]
    assert data["blocked_agents"] == expected_agents, f"final_report.json blocked_agents does not match expected list. Got {data['blocked_agents']}"