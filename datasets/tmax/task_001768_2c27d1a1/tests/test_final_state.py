# test_final_state.py
import os
import stat
import socket
import requests
import json
import time

def test_run_stack_script_exists_and_executable():
    script_path = "/home/user/run_stack.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {script_path}"

def test_http_info_endpoint():
    url = "http://127.0.0.1:8000/info"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to HTTP service at {url}: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    expected_tz = "Asia/Tokyo"
    expected_target = "127.0.0.1:9090"

    assert data.get("tz") == expected_tz, f"Expected tz '{expected_tz}', got '{data.get('tz')}'"
    assert data.get("legacy_target") == expected_target, f"Expected legacy_target '{expected_target}', got '{data.get('legacy_target')}'"

def test_tcp_proxy_auth_success():
    host = "127.0.0.1"
    port = 8001

    try:
        s = socket.create_connection((host, port), timeout=2)
    except Exception as e:
        assert False, f"Failed to connect to TCP proxy at {host}:{port}: {e}"

    try:
        s.sendall(b"AUTH: v2migrate\nHelloLegacy\n")
        response = s.recv(1024)
    except Exception as e:
        s.close()
        assert False, f"Error communicating with TCP proxy: {e}"

    s.close()

    response_str = response.decode('utf-8', errors='replace')
    assert "LEGACY_OS_ACK: HelloLegacy" in response_str, f"Expected 'LEGACY_OS_ACK: HelloLegacy' in response, got: '{response_str}'"

def test_tcp_proxy_auth_failure():
    host = "127.0.0.1"
    port = 8001

    try:
        s = socket.create_connection((host, port), timeout=2)
    except Exception as e:
        assert False, f"Failed to connect to TCP proxy at {host}:{port}: {e}"

    try:
        s.sendall(b"AUTH: badtoken\nHello\n")
        response = s.recv(1024)
    except Exception as e:
        # It's fine if it throws an error on reset
        response = b""

    s.close()

    assert response == b"", f"Expected connection to be dropped with no response, but got: {response}"