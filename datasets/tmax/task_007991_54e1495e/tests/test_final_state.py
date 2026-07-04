# test_final_state.py
import os
import json
import pytest

def test_test_result_log_exists():
    log_file = "/home/user/deploy_bridge/test_result.log"
    assert os.path.exists(log_file), f"Expected log file {log_file} does not exist."
    assert os.path.isfile(log_file), f"Expected {log_file} to be a file."

def test_test_result_log_content():
    log_file = "/home/user/deploy_bridge/test_result.log"

    try:
        with open(log_file, "r") as f:
            content = f.read().strip()
    except Exception as e:
        pytest.fail(f"Could not read {log_file}: {e}")

    assert content, f"The file {log_file} is empty."

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"The content of {log_file} is not valid JSON. Content: {content}. Error: {e}")

    assert isinstance(data, dict), f"The JSON in {log_file} is not a dictionary."

    expected_event = "deployment_checked"
    expected_service = "billing-service"
    expected_version = 4
    expected_score = len(expected_service) * expected_version  # 15 * 4 = 60

    assert data.get("event") == expected_event, f"Expected event '{expected_event}', got '{data.get('event')}'"
    assert data.get("service") == expected_service, f"Expected service '{expected_service}', got '{data.get('service')}'"
    assert data.get("version") == expected_version, f"Expected version {expected_version}, got {data.get('version')}"
    assert data.get("score") == expected_score, f"Expected score {expected_score}, got {data.get('score')}"