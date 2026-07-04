# test_final_state.py

import os
import socket
import urllib.request
import json

def test_result_log_content():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_status = "Service_Operational_9921"
    assert content == expected_status, f"Expected '{expected_status}' in {log_path}, got '{content}'."

def test_backend_listening():
    # Check if port 9090 is open
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "No process is listening on 127.0.0.1:9090 (backend service)."

def test_proxy_listening():
    # Check if port 8080 is open
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "No process is listening on 127.0.0.1:8080 (reverse proxy)."

def test_proxy_functionality():
    # Test if the proxy correctly forwards to the backend
    url = "http://127.0.0.1:8080/api/health"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 from proxy, got {response.status}."
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        assert False, f"Failed to fetch or parse response from proxy at {url}: {e}"

    expected_status = "Service_Operational_9921"
    assert "status" in data, "Response JSON does not contain 'status' key."
    assert data["status"] == expected_status, f"Expected status '{expected_status}' from proxy, got '{data['status']}'."