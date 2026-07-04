# test_final_state.py

import os
import requests
import pytest

def test_validator_bindings():
    """Check that the Validator service binds only to localhost."""
    assert os.path.isfile('/app/validator.py'), "/app/validator.py is missing"
    with open('/app/validator.py', 'r') as f:
        content = f.read()
        assert '127.0.0.1' in content, "Validator source code does not contain 127.0.0.1 binding."
        assert '0.0.0.0' not in content, "Validator source code still contains 0.0.0.0 binding, exposing it to the network."

def test_storage_bindings():
    """Check that the Storage service binds only to localhost."""
    assert os.path.isfile('/app/storage.py'), "/app/storage.py is missing"
    with open('/app/storage.py', 'r') as f:
        content = f.read()
        assert '127.0.0.1' in content, "Storage source code does not contain 127.0.0.1 binding."
        assert '0.0.0.0' not in content, "Storage source code still contains 0.0.0.0 binding, exposing it to the network."

def test_end_to_end_flow():
    """
    Test the end-to-end flow by sending a payload to the Ingester.
    This verifies that the Ingester correctly extracts the seed, computes the token,
    and successfully forwards the request through the Validator to the Storage.
    """
    url = "http://127.0.0.1:5000/ingest"
    payload = {"test": "data"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Ingester at {url}. Are the services running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert data.get("status") == "stored", f"Expected response JSON to contain {{'status': 'stored'}}, got {data}"