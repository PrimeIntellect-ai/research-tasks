# test_final_state.py
import requests
import pytest

def test_shortest_path():
    try:
        resp = requests.get("http://127.0.0.1:8080/shortest_path?from=u1&to=u4", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at 127.0.0.1:8080: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "path" in data, f"Response missing 'path' key. Got: {data}"
    path = data["path"]

    assert isinstance(path, list), f"Expected 'path' to be a list, got {type(path)}"
    assert len(path) == 3, f"Expected shortest path of length 3, got {len(path)}: {path}"
    assert path[0] == "u1", f"Path must start with 'u1', got {path[0]}"
    assert path[-1] == "u4", f"Path must end with 'u4', got {path[-1]}"
    assert path[1] in ["u2", "u3"], f"Invalid intermediate node in path: {path[1]}. Must be 'u2' or 'u3'."

def test_centrality():
    try:
        resp = requests.get("http://127.0.0.1:8080/centrality?node=u1", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at 127.0.0.1:8080: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "out_degree" in data, f"Response missing 'out_degree' key. Got: {data}"
    assert data["out_degree"] == 2, f"Expected out_degree 2 for node 'u1', got {data['out_degree']}"