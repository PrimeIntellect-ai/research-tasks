# test_final_state.py

import os
import pytest
import requests
import time

def test_service_responds_correctly():
    url = "http://127.0.0.1:8080/dispatch?lat=40.7128&lon=-74.0060"
    headers = {
        "Authorization": "Bearer ALPHA-TANGO-NINER"
    }

    # Retry a few times in case the service is slow to start or respond
    max_retries = 5
    last_exception = None

    for _ in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException as e:
            last_exception = e
        time.sleep(1)
    else:
        if last_exception:
            pytest.fail(f"Failed to connect to the service at {url}: {last_exception}")
        else:
            pytest.fail(f"Service returned non-200 status code: {response.status_code}. Response: {response.text}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "responder_id" in data, "Response JSON missing 'responder_id'"
    assert data["responder_id"] == "R-442", f"Expected responder_id 'R-442', got '{data['responder_id']}'"

    assert "distance" in data, "Response JSON missing 'distance'"
    assert isinstance(data["distance"], (int, float)), f"Expected 'distance' to be a number, got {type(data['distance'])}"

def test_unauthorized_request():
    url = "http://127.0.0.1:8080/dispatch?lat=40.7128&lon=-74.0060"
    headers = {
        "Authorization": "Bearer WRONG-TOKEN"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Should not be 200 if unauthorized, but we mainly check that it doesn't return the secret data
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("responder_id") == "R-442":
                    pytest.fail("Service returned correct responder_id even with wrong token.")
            except ValueError:
                pass
    except requests.exceptions.RequestException:
        # If it fails to connect or drops, that's fine for an unauthorized request or if it only accepts the exact token
        pass