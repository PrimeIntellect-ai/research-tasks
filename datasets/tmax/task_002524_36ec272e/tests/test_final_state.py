# test_final_state.py
import os
import socket
import requests
import pytest
import urllib3

# Suppress insecure request warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_https_health_endpoint():
    url = "https://127.0.0.1:8443/health"
    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    expected_body = '{"status": "UP", "target": "QEMU_VNC", "latency": "15ms"}\n'
    assert response.text == expected_body, f"Expected response body {expected_body!r}, got {response.text!r}"

def test_tcp_quota_endpoint():
    host = "127.0.0.1"
    port = 9090

    # First check: should be QUOTA_OK
    try:
        s = socket.create_connection((host, port), timeout=5)
        s.sendall(b"STATUS\n")
        response = s.recv(1024).decode('utf-8')
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to {host}:{port} or receive data: {e}")

    assert response == "QUOTA_OK\n", f"Expected 'QUOTA_OK\\n', got {response!r}"

    # Write a 2MB file to exceed quota
    junk_file = "/home/user/monitor_data/junk.dat"
    os.makedirs("/home/user/monitor_data", exist_ok=True)
    try:
        with open(junk_file, "wb") as f:
            f.write(b"0" * (2 * 1024 * 1024))
    except Exception as e:
        pytest.fail(f"Failed to write 2MB file to {junk_file}: {e}")

    # Second check: should be QUOTA_EXCEEDED
    try:
        s = socket.create_connection((host, port), timeout=5)
        s.sendall(b"STATUS\n")
        response2 = s.recv(1024).decode('utf-8')
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to {host}:{port} or receive data after writing junk file: {e}")

    assert response2 == "QUOTA_EXCEEDED\n", f"Expected 'QUOTA_EXCEEDED\\n', got {response2!r}"

def test_file_permissions():
    state_file = "/home/user/monitor_data/qemu_state.bin"
    assert os.path.exists(state_file), f"State file {state_file} does not exist"
    st = os.stat(state_file)
    assert (st.st_mode & 0o777) == 0o400, f"State file permissions should be 0400, got {oct(st.st_mode & 0o777)}"