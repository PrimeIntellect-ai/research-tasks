# test_final_state.py

import requests
import pytest

URL = "http://127.0.0.1:8080/deploy"
TOKEN = "DEPLOY_SECRET_99X"

def test_unauthorized_missing_header():
    """Test that a request without the Authorization header returns 401."""
    try:
        response = requests.post(URL, data="SET test val", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:8080")

    assert response.status_code == 401, f"Expected status code 401 for missing header, got {response.status_code}"

def test_unauthorized_wrong_header():
    """Test that a request with an incorrect Authorization header returns 401."""
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    try:
        response = requests.post(URL, headers=headers, data="SET test val", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:8080")

    assert response.status_code == 401, f"Expected status code 401 for wrong header, got {response.status_code}"

def test_authorized_valid_payload():
    """Test that a request with the correct header and a valid DSL payload returns 200 and the correct JSON."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = """SET region us-east-1
NUM workers 5
MERGE {"features": {"beta": true}, "timeout": 30}
DELETE debug"""

    try:
        response = requests.post(URL, headers=headers, data=payload, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:8080")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_data = {
        "environment": "production",
        "features": {"beta": True},
        "region": "us-east-1",
        "timeout": 30,
        "version": "1.0",
        "workers": 5
    }

    assert data == expected_data, f"Expected JSON response {expected_data}, got {data}"

    # Check if keys are sorted in the raw JSON response
    # The dictionary keys should be in alphabetical order
    import json
    raw_json = response.text
    # We can parse it with object_pairs_hook to check order
    parsed_pairs = json.loads(raw_json, object_pairs_hook=list)
    keys = [pair[0] for pair in parsed_pairs]
    sorted_keys = sorted(keys)

    assert keys == sorted_keys, f"Expected JSON keys to be sorted alphabetically. Got keys: {keys}"