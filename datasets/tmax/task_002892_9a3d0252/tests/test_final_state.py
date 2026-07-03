# test_final_state.py
import socket
import requests
import json
import time

def wait_for_port(port, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return True
        time.sleep(0.5)
    return False

def test_http_endpoint_authorized():
    """Test the HTTP endpoint with the correct authorization token."""
    assert wait_for_port(8080), "HTTP server is not listening on port 8080"

    url = "http://127.0.0.1:8080/solve/dtmf"
    headers = {"Authorization": "Bearer polyglot-auth-token"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to HTTP server: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, f"Expected JSON response, got: {response.text}"

    assert "result" in data, "Response JSON missing 'result' key"
    assert str(data["result"]) == "42", f"Expected result 42, got {data['result']}"

def test_http_endpoint_unauthorized():
    """Test the HTTP endpoint without the authorization token."""
    assert wait_for_port(8080), "HTTP server is not listening on port 8080"

    url = "http://127.0.0.1:8080/solve/dtmf"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to HTTP server: {e}"

    assert response.status_code == 401, f"Expected status code 401 for unauthorized request, got {response.status_code}"

def test_grpc_port_listening():
    """Test that the gRPC server is listening on port 50051."""
    assert wait_for_port(50051), "gRPC server is not listening on port 50051"