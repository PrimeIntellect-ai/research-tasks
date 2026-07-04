# test_final_state.py

import os
import requests
import pytest

def test_api_gateway_processes_large_integers_correctly():
    """
    Sends a POST request with a large 64-bit integer to the API Gateway.
    Verifies that the services process it without precision loss or crashing.
    """
    url = "http://127.0.0.1:8080/process"
    large_tx_id = 12345678901234567
    payload = {
        "tx_id": large_tx_id,
        "amount": 100.0
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the API Gateway on 127.0.0.1:8080. Are the services running?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to API Gateway timed out. The services might be deadlocked or crashed.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but got: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert "processed_id" in data, "Response JSON is missing 'processed_id' field"
    assert data["processed_id"] == large_tx_id, (
        f"Precision loss or corruption detected. Expected processed_id {large_tx_id}, "
        f"but got {data['processed_id']}."
    )

def test_worker_contains_type_assertion():
    """
    Verifies that worker.py contains an assertion to ensure tx_id is an int.
    """
    worker_path = "/app/src/worker.py"
    assert os.path.isfile(worker_path), f"File not found: {worker_path}"

    with open(worker_path, "r") as f:
        content = f.read()

    # Look for common ways to assert type is int
    has_assertion = "assert type(" in content and "is int" in content
    has_isinstance = "assert isinstance(" in content and "int" in content

    assert has_assertion or has_isinstance, (
        "worker.py is missing the required strict assertion to validate that the "
        "deserialized transaction ID is exactly of type int."
    )