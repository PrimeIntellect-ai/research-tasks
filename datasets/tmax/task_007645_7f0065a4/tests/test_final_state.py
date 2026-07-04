# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_result_json_exists_and_correct():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"The file {result_path} does not exist."

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {result_path} does not contain valid JSON.")

    assert "status" in data, f"The JSON in {result_path} does not contain the 'status' key."
    assert data["status"] == "malicious", f"Expected status 'malicious', but got '{data['status']}'."

def test_build_sh_flags():
    build_sh_path = "/home/user/waf_project/build.sh"
    assert os.path.isfile(build_sh_path), f"The file {build_sh_path} does not exist."

    with open(build_sh_path, "r") as f:
        content = f.read()

    assert "-shared" in content, "The build.sh script is missing the '-shared' flag."
    assert "-fPIC" in content, "The build.sh script is missing the '-fPIC' flag."

def test_web_service_reachable_and_correct():
    url = "http://127.0.0.1:8000/analyze"

    # Test safe payload
    safe_payload = json.dumps({"data": "Hello World"}).encode("utf-8")
    req = urllib.request.Request(url, data=safe_payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            assert res_data.get("status") == "safe", f"Expected 'safe' for safe payload, got {res_data.get('status')}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to web service or got error: {e}")

    # Test malicious payload
    malicious_payload = json.dumps({"data": "SELECT * FROM users"}).encode("utf-8")
    req = urllib.request.Request(url, data=malicious_payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            assert res_data.get("status") == "malicious", f"Expected 'malicious' for malicious payload, got {res_data.get('status')}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to web service or got error: {e}")