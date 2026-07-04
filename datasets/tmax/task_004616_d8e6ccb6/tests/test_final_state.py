# test_final_state.py

import os
import socket
import pytest
import time

def send_req(payload: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('127.0.0.1', 9000))
        s.sendall(payload.encode())
        resp = s.recv(1024).decode()
    finally:
        s.close()
    return resp

def test_libbayes_so_exists():
    assert os.path.isfile('/app/bayes_infer/libbayes.so'), "libbayes.so was not created in /app/bayes_infer"

def test_tcp_server_responses():
    # Test first request
    try:
        resp1 = send_req("1.0,2.0,3.0")
    except Exception as e:
        pytest.fail(f"Failed to connect or receive response from TCP server on port 9000: {e}")

    assert resp1 == "POSITIVE\n", f"Expected 'POSITIVE\\n' for '1.0,2.0,3.0', got {repr(resp1)}"

    # Test second request
    try:
        resp2 = send_req("-5.0,-1.0")
    except Exception as e:
        pytest.fail(f"Failed to connect or receive response from TCP server on port 9000: {e}")

    assert resp2 == "NEGATIVE\n", f"Expected 'NEGATIVE\\n' for '-5.0,-1.0', got {repr(resp2)}"

def test_experiment_log_contents():
    # Sleep briefly to ensure the server has time to flush to the log file
    time.sleep(0.5)
    log_path = '/home/user/experiment_log.txt'
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, 'r') as f:
        content = f.read()

    # The exact posterior means are:
    # 1.0+2.0+3.0 = 6.0 / (3+1) = 1.5000
    # -5.0-1.0 = -6.0 / (2+1) = -2.0000

    expected_line1 = "[Data size: 3] Posterior Mean: 1.5000, Result: POSITIVE"
    expected_line2 = "[Data size: 2] Posterior Mean: -2.0000, Result: NEGATIVE"

    assert expected_line1 in content, f"Expected log line '{expected_line1}' not found in {log_path}"
    assert expected_line2 in content, f"Expected log line '{expected_line2}' not found in {log_path}"