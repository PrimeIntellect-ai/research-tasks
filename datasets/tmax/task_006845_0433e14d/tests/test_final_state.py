# test_final_state.py

import os
import json
import pytest

def test_analyzer_script_exists():
    assert os.path.exists("/home/user/analyzer.py"), "The analyzer.py script is missing."
    assert os.path.isfile("/home/user/analyzer.py"), "/home/user/analyzer.py is not a file."

def test_optimal_route_json():
    json_path = "/home/user/optimal_route.json"
    assert os.path.exists(json_path), f"{json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    expected_url = "http://127.0.0.1:8080/zone3"
    assert "target_url" in data, f"'target_url' key missing in {json_path}."
    assert data["target_url"] == expected_url, f"Expected target_url to be {expected_url}, but got {data['target_url']}."

def test_finops_env():
    env_path = "/home/user/.finops_env"
    assert os.path.exists(env_path), f"{env_path} is missing."

    with open(env_path, 'r') as f:
        content = f.read().strip()

    expected_line = 'export DEFAULT_CLOUD_ZONE="http://127.0.0.1:8080/zone3"'
    # Also accept without quotes or single quotes
    expected_line_single = "export DEFAULT_CLOUD_ZONE='http://127.0.0.1:8080/zone3'"
    expected_line_no_quotes = "export DEFAULT_CLOUD_ZONE=http://127.0.0.1:8080/zone3"

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert len(lines) >= 1, f"{env_path} is empty."

    found = any(
        line == expected_line or line == expected_line_single or line == expected_line_no_quotes
        for line in lines
    )
    assert found, f"Could not find the correct export statement in {env_path}. Expected: {expected_line}"

def test_connectivity_log():
    log_path = "/home/user/connectivity_test.log"
    assert os.path.exists(log_path), f"{log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "200", f"Expected {log_path} to contain exactly '200', but got '{content}'."