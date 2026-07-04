# test_final_state.py

import os
import socket
import time
import requests
import pytest

def test_admin_token_file():
    token_file = "/home/user/admin_token.txt"
    assert os.path.isfile(token_file), f"File {token_file} does not exist."
    with open(token_file, "r") as f:
        content = f.read().strip()
    assert content == "s3cr3t_0ps_t0k3n_99", f"Token file content is incorrect: {content}"

def test_minilogd_service_and_logic():
    # 1. Send logs to TCP Ingest Port
    tcp_host = "127.0.0.1"
    tcp_port = 8080

    logs = [
        b"[ERROR] app=frontend msg=Connection timeout\n",
        b"[INFO] app=backend msg=Started worker\n",
        b"[ERROR] app=database msg=Disk full\n"
    ]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((tcp_host, tcp_port))
            for log in logs:
                s.sendall(log)
                time.sleep(0.1) # Give it a moment to process
    except Exception as e:
        pytest.fail(f"Failed to connect and send logs to TCP port {tcp_port}: {e}")

    # 2. Query logs via HTTP API
    http_url = "http://127.0.0.1:8081/query"
    params = {"q": "(level=ERROR)"}
    headers = {"Authorization": "Bearer s3cr3t_0ps_t0k3n_99"}

    try:
        response = requests.get(http_url, params=params, headers=headers, timeout=5.0)
    except requests.exceptions.Timeout:
        pytest.fail("HTTP GET request timed out. The infinite recursion bug in query parser may not be fixed.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to HTTP port 8081. Is the service running?")
    except Exception as e:
        pytest.fail(f"HTTP GET request failed: {e}")

    # 3. Verify response
    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    response_text = response.text
    assert "app=frontend" in response_text and "Connection timeout" in response_text, "Missing first ERROR log in response."
    assert "app=database" in response_text and "Disk full" in response_text, "Missing second ERROR log in response."
    assert "app=backend" not in response_text and "Started worker" not in response_text, "Response contains INFO logs, but should only contain ERROR logs. Logic bug in db.c may not be fixed."