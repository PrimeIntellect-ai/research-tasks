# test_final_state.py
import requests
import pytest
import json

def test_audit_service_response():
    url = "http://127.0.0.1:9090/audit_report"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the audit service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    # Check required keys
    required_keys = ["target_port", "debug_token", "cwe", "exploit_payload"]
    for key in required_keys:
        assert key in data, f"Missing required key '{key}' in JSON response."

    # Validate target_port
    assert data["target_port"] == 4432, f"Expected target_port 4432, got {data['target_port']}"

    # Validate debug_token
    expected_token = "AUTH_B4ckd00r_99"
    assert data["debug_token"] == expected_token, f"Expected debug_token '{expected_token}', got '{data['debug_token']}'"

    # Validate cwe
    assert data["cwe"] == "CWE-94", f"Expected cwe 'CWE-94', got '{data['cwe']}'"

    # Validate exploit_payload
    payload = data["exploit_payload"]
    assert isinstance(payload, str), "exploit_payload must be a string."
    assert len(payload) > 0, "exploit_payload must not be empty."

    # Basic heuristic to check if it looks like a python payload for eval
    # We don't execute it for safety, but check for common python builtins/modules used in RCE
    has_python_constructs = any(keyword in payload for keyword in ["__import__", "os", "sys", "subprocess", "eval", "exec", "open"])
    assert has_python_constructs, f"The exploit_payload '{payload}' does not appear to contain typical Python injection constructs."