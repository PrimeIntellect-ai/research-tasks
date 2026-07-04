# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def check_shortest_path(src, dst, expected_length, expected_paths):
    url = f"{BASE_URL}/audit/shortest_path"
    params = {"src": src, "dst": dst}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or retrieve data for {src}->{dst}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", "").lower(), "Expected Content-Type: application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert "length" in data, "JSON response missing 'length' key"
    assert "path" in data, "JSON response missing 'path' key"

    assert data["length"] == expected_length, f"Expected length {expected_length}, got {data['length']}"

    if expected_length == -1:
        assert data["path"] == [], f"Expected empty path for unreachable nodes, got {data['path']}"
    else:
        assert data["path"] in expected_paths, f"Expected one of the paths {expected_paths}, got {data['path']}"

def test_shortest_path_a_to_f():
    # A->B->F is length 2
    check_shortest_path("A", "F", 2, [["A", "B", "F"]])

def test_shortest_path_a_to_d():
    # A->E->D is length 2
    check_shortest_path("A", "D", 2, [["A", "E", "D"]])

def test_shortest_path_f_to_a():
    # Unreachable
    check_shortest_path("F", "A", -1, [[]])

def test_shortest_path_b_to_d():
    # B->C->D is length 2
    check_shortest_path("B", "D", 2, [["B", "C", "D"]])