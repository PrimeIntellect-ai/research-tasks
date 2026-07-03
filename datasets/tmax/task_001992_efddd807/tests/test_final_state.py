# test_final_state.py

import os
import time
import socket
import subprocess
import requests
import pytest

@pytest.fixture(scope="session", autouse=True)
def start_services():
    """Ensure the services are started via /app/start.sh."""
    # Check if service is already running
    try:
        requests.get("http://127.0.0.1:8080", timeout=1)
        running = True
    except requests.RequestException:
        running = False

    if not running:
        proc = subprocess.Popen(["bash", "/app/start.sh"], cwd="/app")

        # Wait for the service to be available
        for _ in range(30):
            try:
                # We just need the TCP port to be open, or any HTTP response
                with socket.create_connection(("127.0.0.1", 8080), timeout=1):
                    break
            except OSError:
                time.sleep(0.5)
        else:
            pytest.fail("Service did not start on port 8080 within 15 seconds")

        yield
        proc.terminate()
    else:
        yield

def test_c_code_fixed():
    path = "/app/legacy/telemetry.c"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "i <= len" not in content, "The bug (i <= len) should be fixed in telemetry.c"

def test_auth_missing():
    response = requests.post(
        "http://127.0.0.1:8080/api/v1/process",
        json={"batch_id": "test_auth", "readings": [1, 2, 3]}
    )
    assert response.status_code == 401, f"Expected 401 Unauthorized without auth header, got {response.status_code}"

def test_auth_invalid():
    response = requests.post(
        "http://127.0.0.1:8080/api/v1/process",
        headers={"Authorization": "Bearer invalid_token"},
        json={"batch_id": "test_auth_invalid", "readings": [1, 2, 3]}
    )
    assert response.status_code == 401, f"Expected 401 Unauthorized with bad token, got {response.status_code}"

def get_redis_key(key: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(('127.0.0.1', 6379))
    cmd = f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n"
    s.sendall(cmd.encode('utf-8'))
    resp = s.recv(4096).decode('utf-8')
    s.close()

    # RESP Bulk String format: $<length>\r\n<data>\r\n
    # Null bulk string: $-1\r\n
    if resp.startswith("$-1"):
        return None

    parts = resp.split("\r\n")
    if len(parts) >= 2:
        return parts[1]
    return resp

def test_process_endpoint_small_payload():
    batch_id = "test_small"
    readings = [10, 20, 30, 40]
    expected_sum = sum(readings)

    response = requests.post(
        "http://127.0.0.1:8080/api/v1/process",
        headers={"Authorization": "Bearer dev_token_99z"},
        json={"batch_id": batch_id, "readings": readings}
    )

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code} with body {response.text}"

    data = response.json()
    assert "result" in data, f"Response JSON missing 'result' key: {data}"
    assert data["result"] == expected_sum, f"Expected result {expected_sum}, got {data['result']}"

    # Check Redis
    redis_val = get_redis_key(f"batch:{batch_id}")
    assert redis_val == str(expected_sum), f"Expected Redis value {expected_sum}, got {redis_val}"

def test_process_endpoint_large_payload():
    batch_id = "test_large"
    readings = [1] * 5000
    expected_sum = 5000

    try:
        response = requests.post(
            "http://127.0.0.1:8080/api/v1/process",
            headers={"Authorization": "Bearer dev_token_99z"},
            json={"batch_id": batch_id, "readings": readings},
            timeout=5
        )
    except requests.RequestException as e:
        pytest.fail(f"Request failed, possibly due to a crash (OOB read): {e}")

    assert response.status_code == 200, f"Expected 200 OK for large payload, got {response.status_code} with body {response.text}"

    data = response.json()
    assert "result" in data, f"Response JSON missing 'result' key: {data}"
    assert data["result"] == expected_sum, f"Expected result {expected_sum}, got {data['result']}"

    # Check Redis
    redis_val = get_redis_key(f"batch:{batch_id}")
    assert redis_val == str(expected_sum), f"Expected Redis value {expected_sum}, got {redis_val}"