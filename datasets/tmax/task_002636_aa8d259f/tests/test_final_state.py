# test_final_state.py
import pytest
import requests
import time

def wait_for_service(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

def test_impact_endpoint_delta_92():
    url = "http://127.0.0.1:8080/api/impact?corrupted_id=delta-92"

    # Wait for the service to be up
    service_up = wait_for_service("http://127.0.0.1:8080/")
    # If the root isn't accessible, we just proceed to the actual endpoint and let it fail if it's down.

    try:
        response = requests.get(url, timeout=5)
    except requests.ConnectionError:
        pytest.fail("Failed to connect to the service at 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "impacted" in data, "JSON response missing 'impacted' key."

    expected_impacted = {"epsilon-93", "zeta-94"}
    actual_impacted = set(data["impacted"])

    assert actual_impacted == expected_impacted, f"Expected impacted snapshots {expected_impacted}, but got {actual_impacted}"

def test_impact_endpoint_gamma_30():
    url = "http://127.0.0.1:8080/api/impact?corrupted_id=gamma-30"

    try:
        response = requests.get(url, timeout=5)
    except requests.ConnectionError:
        pytest.fail("Failed to connect to the service at 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "impacted" in data, "JSON response missing 'impacted' key."

    expected_impacted = {"delta-92", "epsilon-93", "zeta-94"}
    actual_impacted = set(data["impacted"])

    assert actual_impacted == expected_impacted, f"Expected impacted snapshots {expected_impacted}, but got {actual_impacted}"