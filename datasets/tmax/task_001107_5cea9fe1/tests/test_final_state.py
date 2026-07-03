# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:9090"

def test_nodes_endpoint():
    """
    Validates Endpoint A: GET /nodes
    Checks pagination, filtering by label, and correct JSON response structure.
    """
    params = {"label": "Author", "limit": 1, "page": 2}
    try:
        response = requests.get(f"{BASE_URL}/nodes", params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("page") == 2, f"Expected page 2, got {data.get('page')}"
    assert data.get("limit") == 1, f"Expected limit 1, got {data.get('limit')}"

    results = data.get("results")
    assert isinstance(results, list), "Expected 'results' to be a list"
    assert len(results) == 1, f"Expected exactly 1 result, got {len(results)}"

    assert results[0].get("id") == "n2", f"Expected result id 'n2', got {results[0].get('id')}"
    assert results[0].get("name") == "Bob", f"Expected result name 'Bob', got {results[0].get('name')}"

def test_shortest_path_endpoint():
    """
    Validates Endpoint B: GET /shortest-path
    Checks graph traversal, scorer integration, and correct JSON response structure.
    """
    params = {"start": "n1", "end": "n4"}
    try:
        response = requests.get(f"{BASE_URL}/shortest-path", params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    path = data.get("path")
    assert isinstance(path, list), "Expected 'path' to be a list"
    assert path == ["n1", "n3", "n4"], f"Expected path ['n1', 'n3', 'n4'], got {path}"

    score = data.get("score")
    assert isinstance(score, (float, int)), "Expected 'score' to be a number"
    assert abs(score - 0.6) < 0.001, f"Expected score around 0.6, got {score}"

def test_shortest_path_not_found():
    """
    Validates Endpoint B for a non-existent path.
    """
    params = {"start": "n1", "end": "n999"}
    try:
        response = requests.get(f"{BASE_URL}/shortest-path", params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert response.status_code == 404, f"Expected status code 404 for missing path, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "error" in data, "Expected 'error' key in 404 response"