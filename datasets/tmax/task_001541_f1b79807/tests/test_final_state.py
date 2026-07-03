# test_final_state.py
import os
import socket
import csv
import math

def test_rms_features_csv():
    path = '/home/user/rms_features.csv'
    assert os.path.exists(path), f"Features file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 10, "Not enough rows in rms_features.csv. Expected at least 10."

    # Check first row format (could be header or data, but spec says "starting with window_index 0")
    # Let's check if the first line starts with '0,' or 'window_index'
    has_header = content[0].startswith('window_index')
    start_idx = 1 if has_header else 0

    for i in range(10):
        row = content[start_idx + i].split(',')
        assert len(row) == 2, f"Invalid format in rms_features.csv at row {start_idx + i}"
        assert int(row[0]) == i, f"Expected window_index {i}, got {row[0]}"
        rms = float(row[1])

        # Expected RMS is roughly amp / sqrt(2), amp = 1000 + i * 500
        amp = 1000 + i * 500
        expected_rms = amp / math.sqrt(2)
        assert math.isclose(rms, expected_rms, rel_tol=0.05), f"RMS value mismatch at window {i}: expected ~{expected_rms}, got {rms}"

def test_tcp_server_auth_failure():
    # Test incorrect auth
    try:
        s = socket.create_connection(('127.0.0.1', 9000), timeout=2)
        s.sendall(b"AUTH: wrong_token\n")
        response = s.recv(1024)
        # Should close connection or return nothing
        assert not response, "Server should close connection on incorrect auth without responding"
        s.close()
    except ConnectionRefusedError:
        assert False, "Server is not listening on 127.0.0.1:9000"
    except socket.timeout:
        pass # Timeout is also acceptable if it just drops the connection

def test_tcp_server_success():
    try:
        s = socket.create_connection(('127.0.0.1', 9000), timeout=2)
        s.sendall(b"AUTH: ds_agent_2024\n")
        s.sendall(b"GET_CORRELATION\n")
        response = s.recv(1024).decode('utf-8')
        s.close()
    except ConnectionRefusedError:
        assert False, "Server is not listening on 127.0.0.1:9000"
    except socket.timeout:
        assert False, "Server timed out waiting for response"

    assert response == "RESULT: 1.0000\n", f"Expected 'RESULT: 1.0000\\n', got {repr(response)}"