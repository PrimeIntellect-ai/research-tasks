# test_final_state.py
import os
import time
import requests
import pytest

def test_executable_exists():
    """Check if the C backend was successfully compiled."""
    assert os.path.exists('/home/user/app/backend/layout_engine'), "The layout_engine executable was not found. Did you compile it?"

def test_api_reachable():
    """Check if the API is running and reachable."""
    payload = {
        "vertices": 3,
        "edges": [[0, 1], [1, 2], [2, 0]]
    }
    try:
        response = requests.post("http://127.0.0.1:8000/api/layout", json=payload, timeout=2)
        assert response.status_code == 200, f"API returned status code {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("API is not reachable on 127.0.0.1:8000. Is the server running in the background?")

def test_api_correctness():
    """Verify the structural correctness of the API response."""
    payload = {
        "vertices": 3,
        "edges": [[0, 1], [1, 2], [2, 0]]
    }
    response = requests.post("http://127.0.0.1:8000/api/layout", json=payload).json()
    assert "coordinates" in response, "Response JSON missing 'coordinates' key"
    assert len(response["coordinates"]) == 3, "Response JSON 'coordinates' length should be 3"

    coords = response["coordinates"]
    for coord in coords:
        assert "x" in coord and "y" in coord, "Coordinates should contain 'x' and 'y' keys"
        assert isinstance(coord["x"], (int, float)), "'x' must be a number"
        assert isinstance(coord["y"], (int, float)), "'y' must be a number"

def test_api_latency_metric():
    """
    Evaluate the performance metric: 100 cached requests must complete in <= 0.5s.
    This validates that Redis caching was correctly implemented.
    """
    payload = {
        "vertices": 3,
        "edges": [[0, 1], [1, 2], [2, 0]]
    }

    # Warm up to ensure the result is cached
    requests.post("http://127.0.0.1:8000/api/layout", json=payload)

    start = time.time()
    for _ in range(100):
        requests.post("http://127.0.0.1:8000/api/layout", json=payload)
    total_time = time.time() - start

    threshold = 0.5
    assert total_time <= threshold, (
        f"Metric failed: total_time for 100 requests was {total_time:.4f}s, "
        f"threshold is <= {threshold}s. Redis caching might not be working properly."
    )