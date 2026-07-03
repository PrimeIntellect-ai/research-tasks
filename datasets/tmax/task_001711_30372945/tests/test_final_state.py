# test_final_state.py
import os
import requests
import pytest

def test_c_file_exists_and_uses_openmp():
    """Test that the C program exists and contains OpenMP directives."""
    c_file_path = "/home/user/motif_scorer.c"
    assert os.path.isfile(c_file_path), f"C program not found at {c_file_path}"

    with open(c_file_path, "r") as f:
        content = f.read()

    # Check for basic OpenMP usage
    assert "omp" in content.lower(), "C program does not appear to use OpenMP (missing 'omp' pragmas or headers)."

def test_network_service_response():
    """Test that the network service returns the correct JSON response."""
    url = "http://127.0.0.1:8080/score"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the network service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "max_score" in data, "JSON response missing 'max_score' key"
    assert "index" in data, "JSON response missing 'index' key"

    assert data["max_score"] == 8, f"Expected max_score to be 8, got {data['max_score']}"
    assert data["index"] == 42000, f"Expected index to be 42000, got {data['index']}"