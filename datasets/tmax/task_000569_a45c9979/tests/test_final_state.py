# test_final_state.py

import os
import socket
import time
import subprocess
import pytest

def wait_for_port(port, host='127.0.0.1', timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
        time.sleep(0.5)
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_service_running():
    script_path = "/home/user/start_service.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    if not wait_for_port(8888, timeout=1):
        # Try to start the service
        proc = subprocess.Popen([script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert wait_for_port(8888, timeout=5), "Service did not start listening on port 8888"
        yield
        proc.terminate()
    else:
        yield

def send_payload(payload: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 8888))
        sock.sendall(payload.encode('utf-8'))
        sock.shutdown(socket.SHUT_WR) # Half-close to signal EOF

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
    return response.decode('utf-8').strip()

def test_files_exist():
    assert os.path.exists("/home/user/covar.cpp"), "C++ source file /home/user/covar.cpp is missing"
    assert os.path.exists("/home/user/covar"), "Compiled binary /home/user/covar is missing"
    assert os.access("/home/user/covar", os.X_OK), "/home/user/covar is not executable"

def test_valid_schema():
    payload = "featA,featB,featC\n1.0,2.0,3.0\n4.0,5.0,6.0\n7.0,8.0,9.0\n"
    expected = "9.0000,9.0000,9.0000\n9.0000,9.0000,9.0000\n9.0000,9.0000,9.0000"

    response = send_payload(payload)

    # Normalize line endings
    response_lines = [line.strip() for line in response.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected.splitlines() if line.strip()]

    assert response_lines == expected_lines, f"Expected covariance matrix:\n{expected}\nGot:\n{response}"

def test_invalid_schema_wrong_header():
    payload = "f1,f2,f3\n1.0,2.0,3.0\n"
    expected = "ERR_SCHEMA"

    response = send_payload(payload)
    assert response == expected, f"Expected {expected} for wrong header, got: {response}"

def test_invalid_schema_missing_columns():
    payload = "featA,featB,featC\n1.0,2.0\n"
    expected = "ERR_SCHEMA"

    response = send_payload(payload)
    assert response == expected, f"Expected {expected} for missing columns, got: {response}"