# test_final_state.py

import os
import json
import subprocess
import urllib.request
import urllib.error

def test_diagnostics_json_exists_and_valid():
    json_path = "/home/user/diagnostics.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert "diagnostic_token" in data, "Key 'diagnostic_token' missing in diagnostics.json."
    assert "bad_commit" in data, "Key 'bad_commit' missing in diagnostics.json."
    assert "service_status" in data, "Key 'service_status' missing in diagnostics.json."

def test_diagnostic_token():
    json_path = "/home/user/diagnostics.json"
    with open(json_path, 'r') as f:
        data = json.load(f)

    expected_token = "f9b23c4a-8d1e-4567-b90a-123456abcdef"
    assert data["diagnostic_token"] == expected_token, f"diagnostic_token is incorrect. Got {data['diagnostic_token']}."

def test_bad_commit():
    json_path = "/home/user/diagnostics.json"
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Dynamically find the bad commit hash
    result = subprocess.run(
        ["git", "-C", "/home/user/poly_parser", "log", "--format=%H", "--grep=Optimize regex for faster parsing"],
        capture_output=True, text=True
    )
    expected_hash = result.stdout.strip()

    assert expected_hash, "Could not find the bad commit in git history (test setup issue)."
    assert data["bad_commit"] == expected_hash, f"bad_commit is incorrect. Expected {expected_hash}, got {data['bad_commit']}."

def test_service_status_json():
    json_path = "/home/user/diagnostics.json"
    with open(json_path, 'r') as f:
        data = json.load(f)

    assert data["service_status"] == "running", f"service_status should be 'running', got {data['service_status']}."

def test_diagnostic_server_running():
    try:
        response = urllib.request.urlopen("http://localhost:8080", timeout=2)
        assert response.status == 200, f"Diagnostic server returned status {response.status}."
        body = response.read().decode('utf-8')
        assert "Diagnostic server running" in body, "Diagnostic server is not returning the expected response."
    except urllib.error.URLError as e:
        assert False, f"Could not connect to the diagnostic server on port 8080: {e}"

def test_evaluate_script_fixed():
    result = subprocess.run(
        ["python", "/home/user/poly_parser/evaluate.py", "--test", "/home/user/poly_parser/edge_case.txt"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"evaluate.py failed with error:\n{result.stderr}"
    assert "Parsed: 0.00015" in result.stdout, f"evaluate.py did not print the expected output. Got:\n{result.stdout}"