# test_final_state.py
import os
import requests

def test_service_ready_log():
    """Test that the service_ready.log file exists and contains SERVICE_UP."""
    log_path = "/home/user/service_ready.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "SERVICE_UP" in content, f"Log file does not contain 'SERVICE_UP', found: {content}"

def test_shortest_path_a_to_e():
    """Test that the service correctly computes the shortest path from A to E."""
    url = "http://127.0.0.1:8080/shortest_path"
    headers = {"Authorization": "Token research-2024"}
    payload = {"start_node": "A", "end_node": "E"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert "path" in data, "Response JSON missing 'path' key"
    assert "total_weight" in data, "Response JSON missing 'total_weight' key"

    assert data["path"] == ["A", "B", "C", "D", "E"], f"Incorrect path, got: {data['path']}"
    assert data["total_weight"] == 25, f"Incorrect total weight, got: {data['total_weight']}"

def test_unauthorized_access():
    """Test that the service rejects requests without the correct Authorization header."""
    url = "http://127.0.0.1:8080/shortest_path"
    payload = {"start_node": "A", "end_node": "B"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service: {e}"

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_no_path_exists():
    """Test that the service correctly returns 404 when no path exists."""
    url = "http://127.0.0.1:8080/shortest_path"
    headers = {"Authorization": "Token research-2024"}
    payload = {"start_node": "E", "end_node": "A"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the service: {e}"

    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}. Response: {response.text}"