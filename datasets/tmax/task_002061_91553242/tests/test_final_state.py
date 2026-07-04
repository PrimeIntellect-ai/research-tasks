# test_final_state.py

import os
import socket
import time
import pytest

def test_server_files_exist():
    assert os.path.exists("/home/user/server.c"), "Source code /home/user/server.c is missing."
    assert os.path.exists("/home/user/server"), "Compiled binary /home/user/server is missing."
    assert os.access("/home/user/server", os.X_OK), "Compiled binary is not executable."

def test_tcp_server_logic_and_logging():
    host = '127.0.0.1'
    port = 7777

    # Ensure log file doesn't have our specific test lines yet, or we just read it after
    try:
        with open("/home/user/pipeline.log", "r") as f:
            initial_log = f.read()
    except FileNotFoundError:
        initial_log = ""

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Could not connect to server at {host}:{port}: {e}")

    def send_and_expect(data_to_send, expected_response):
        s.sendall(data_to_send.encode('ascii'))
        if expected_response is not None:
            resp = s.recv(1024).decode('ascii')
            assert expected_response in resp, f"Expected '{expected_response}' in response, got '{resp}'"

    try:
        # B1: 100
        send_and_expect("100,10.0\n", None)
        # B2: 110 -> triggers B1
        send_and_expect("110,10.0\n", "BUCKET 100 10.00 NORMAL\n")
        # B3: 120 -> triggers B2
        send_and_expect("120,10.0\n", "BUCKET 110 10.00 NORMAL\n")
        # B4: 130 -> triggers B3
        send_and_expect("130,18.0\n", "BUCKET 120 10.00 NORMAL\n")

        # B4 value is 18.0. History is 10.0, 10.0, 10.0. Avg = 10.0.
        # Threshold = 10.0 * 1.5 + 2.5 = 17.5.
        # 18.0 > 17.5 -> ANOMALY
        # B5: 140 -> triggers B4
        send_and_expect("140,5.0\n", "BUCKET 130 18.00 ANOMALY\n")

    finally:
        s.close()

    # Wait a moment for the server to process the close and write logs
    time.sleep(0.5)

    # Check log file
    assert os.path.exists("/home/user/pipeline.log"), "Log file /home/user/pipeline.log does not exist."
    with open("/home/user/pipeline.log", "r") as f:
        final_log = f.read()

    expected_logs = [
        "[INFO] Processed bucket 100, avg: 10.00, status: NORMAL",
        "[INFO] Processed bucket 110, avg: 10.00, status: NORMAL",
        "[INFO] Processed bucket 120, avg: 10.00, status: NORMAL",
        "[INFO] Processed bucket 130, avg: 18.00, status: ANOMALY",
        "[INFO] Processed bucket 140, avg: 5.00, status: NORMAL"
    ]

    for log_line in expected_logs:
        assert log_line in final_log, f"Expected log line '{log_line}' not found in /home/user/pipeline.log"