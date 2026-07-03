# test_final_state.py

import json
import requests
import pytest

def test_dashboard_service():
    """
    Test that the dashboard service is running on 127.0.0.1:8080,
    accepts the correct authentication token, and returns valid JSON
    with all targets marked as UP.
    """
    url = "http://127.0.0.1:8080/state"
    headers = {
        "Authorization": "Bearer sre-secret-77x"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the dashboard service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        pytest.fail(f"Dashboard response is not valid JSON. Response body: {response.text}\nError: {e}")

    # Verify that data contains targets and they are all UP
    # The exact structure depends on the monitor, but typically it's a dict or list of targets.
    # We will check if 'targets' key exists or iterate over values.

    # If it's a dict of targets:
    if isinstance(data, dict):
        # Look for a targets key or assume the dict itself is the targets mapping
        targets = data.get("targets", data)
        if isinstance(targets, dict):
            for target, status in targets.items():
                # Status might be a dict with a 'status' key or just a string
                if isinstance(status, dict):
                    assert status.get("status") == "UP", f"Target {target} is not UP: {status}"
                else:
                    assert status == "UP", f"Target {target} is not UP: {status}"
        elif isinstance(targets, list):
            for item in targets:
                assert item.get("status") == "UP", f"Target {item} is not UP"
    elif isinstance(data, list):
        for item in data:
            assert item.get("status") == "UP", f"Target {item} is not UP"
    else:
        pytest.fail(f"Unexpected JSON structure: {data}")