# test_final_state.py

import pytest
import requests
import time

def test_service_responds_correctly():
    """
    Test that the service is running on 127.0.0.1:8080, accepts the correct 
    payload, and returns the expected authenticated response.
    """
    url = "http://127.0.0.1:8080/auth"
    payload = {
        "ticket_date": "2024/05/12 10:00:00",
        "code": "gamma ray burst"
    }

    # Retry a few times in case the service is still starting up
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=5)
            break
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                pytest.fail("Failed to connect to the service at 127.0.0.1:8080. Is it running?")
        except requests.exceptions.Timeout:
            pytest.fail("Service at 127.0.0.1:8080 timed out.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Service did not return valid JSON. Response body: {response.text}")

    assert json_data.get("status") == "authenticated", f"Expected status 'authenticated', got {json_data.get('status')}. Full response: {json_data}"