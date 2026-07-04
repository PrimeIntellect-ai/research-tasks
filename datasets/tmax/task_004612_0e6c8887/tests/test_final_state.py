# test_final_state.py

import pytest
import requests
import time

def wait_for_service(url, timeout=5):
    """Wait for the service to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200 or response.status_code == 404:
                return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_alert_info_endpoint():
    """Test the /api/alert_info endpoint returns the correct target and depth."""
    base_url = "http://127.0.0.1:8080"
    endpoint = f"{base_url}/api/alert_info"

    assert wait_for_service(base_url), f"Service at {base_url} is not reachable."

    try:
        response = requests.get(endpoint, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {endpoint}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "target" in data, "Key 'target' missing in JSON response."
    assert "depth" in data, "Key 'depth' missing in JSON response."

    assert data["target"] == "BlackOasis", f"Expected target 'BlackOasis', got '{data['target']}'"
    assert data["depth"] == 2, f"Expected depth 2, got {data['depth']}"

def test_trace_endpoint():
    """Test the /api/trace endpoint returns the correct entities within traversal depth."""
    base_url = "http://127.0.0.1:8080"
    endpoint = f"{base_url}/api/trace?entity=BlackOasis"

    assert wait_for_service(base_url), f"Service at {base_url} is not reachable."

    try:
        response = requests.get(endpoint, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {endpoint}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), f"Expected JSON array, got {type(data).__name__}"

    expected_entities = ["BlackOasis", "Crimson_Shell", "Frontier_Corp", "Global_Holdings", "Shadow_Trust"]

    # The array must be sorted alphabetically and contain no duplicates.
    assert data == sorted(list(set(data))), "Returned array is not sorted alphabetically or contains duplicates."

    assert data == expected_entities, f"Expected {expected_entities}, got {data}"