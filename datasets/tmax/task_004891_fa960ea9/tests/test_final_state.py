# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = f"{BASE_URL}/extract"
AUTH_HEADER = {"Authorization": "Bearer graph-token-999"}

def test_missing_auth_rejected():
    """Verify that requests without the correct authorization header are rejected."""
    payload = {"num_nodes": 4, "edges": [[0, 1], [2, 3]]}
    try:
        response = requests.post(ENDPOINT, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server on 127.0.0.1:8000. Is the service running?")

    assert response.status_code in [401, 403], (
        f"Expected 401 or 403 for missing auth, but got {response.status_code}."
    )

def test_extract_endpoint_success():
    """Verify that the endpoint processes a disconnected graph successfully with correct auth."""
    payload = {"num_nodes": 4, "edges": [[0, 1], [2, 3]]}
    try:
        response = requests.post(ENDPOINT, json=payload, headers=AUTH_HEADER, timeout=15)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server on 127.0.0.1:8000. Is the service running?")

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
    )

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but got: {response.text}")

    assert "embedding" in data, "Response JSON missing 'embedding' key."
    assert "tv_distance" in data, "Response JSON missing 'tv_distance' key."

    embedding = data["embedding"]
    tv_distance = data["tv_distance"]

    assert isinstance(embedding, list), f"Expected 'embedding' to be a list, got {type(embedding)}."
    assert len(embedding) == 4, f"Expected 'embedding' to have 4 elements, got {len(embedding)}."
    assert all(isinstance(x, (int, float)) for x in embedding), "All elements in 'embedding' must be numbers."

    assert isinstance(tv_distance, (int, float)), f"Expected 'tv_distance' to be a float, got {type(tv_distance)}."