# test_final_state.py
import pytest
import requests
import json
import os

def test_api_signal_endpoint():
    """Test the /api/signal endpoint via Nginx."""
    url = "http://127.0.0.1:8080/api/signal"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "dominant_frequency" in data, f"Key 'dominant_frequency' missing in response: {data}"

    # The simulator generates a 42 Hz signal
    assert data["dominant_frequency"] == 42, f"Expected dominant frequency to be 42, got {data['dominant_frequency']}"

def test_api_graph_endpoint_42():
    """Test the /api/graph/<freq> endpoint with freq=42 via Nginx."""
    url = "http://127.0.0.1:8080/api/graph/42"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "max_component_size" in data, f"Key 'max_component_size' missing in response: {data}"

    # For freq=42, the resonating nodes are 1, 2, 3, 6. They form a connected component of size 4.
    assert data["max_component_size"] == 4, f"Expected max_component_size to be 4, got {data['max_component_size']}"

def test_api_graph_endpoint_100():
    """Test the /api/graph/<freq> endpoint with freq=100 via Nginx."""
    url = "http://127.0.0.1:8080/api/graph/100"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "max_component_size" in data, f"Key 'max_component_size' missing in response: {data}"

    # For freq=100, only node 5 resonates. Max component size is 1.
    assert data["max_component_size"] == 1, f"Expected max_component_size to be 1, got {data['max_component_size']}"

def test_processor_file_exists():
    """Ensure the processor file was created."""
    assert os.path.isfile("/app/processor.py"), "Expected /app/processor.py to exist, but it does not."