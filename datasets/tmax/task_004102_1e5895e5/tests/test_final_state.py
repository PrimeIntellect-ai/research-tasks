# test_final_state.py

import os
import socket
import subprocess
import time
import pytest

def test_reproducer_exists():
    assert os.path.isfile("/home/user/reproducer.cpp"), "reproducer.cpp is missing"
    assert os.path.isfile("/home/user/reproducer"), "reproducer executable is missing"
    assert os.access("/home/user/reproducer", os.X_OK), "reproducer is not executable"

def test_ts_server_exists():
    assert os.path.isfile("/home/user/ts_server.cpp"), "ts_server.cpp is missing"
    assert os.path.isfile("/home/user/ts_server"), "ts_server executable is missing"
    assert os.access("/home/user/ts_server", os.X_OK), "ts_server is not executable"

def test_ts_server_protocol():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(('127.0.0.1', 9000))
    except ConnectionRefusedError:
        pytest.fail("Failed to connect to ts_server on 127.0.0.1:9000. Is it running?")

    try:
        # 1. PUT cpu_usage
        s.sendall(b"PUT cpu_usage 1678886400 95.5\n")
        resp = s.recv(1024).decode('utf-8')
        assert resp == "OK\n", f"Expected 'OK\\n' for PUT, got {repr(resp)}"

        # 2. PUT mem_usage
        s.sendall(b"PUT mem_usage 1678886400 12.1\n")
        resp = s.recv(1024).decode('utf-8')
        assert resp == "OK\n", f"Expected 'OK\\n' for PUT, got {repr(resp)}"

        # 3. GET cpu_usage (found)
        s.sendall(b"GET cpu_usage 1678886400\n")
        resp = s.recv(1024).decode('utf-8')
        assert resp == "VAL 95.5\n", f"Expected 'VAL 95.5\\n' for GET, got {repr(resp)}"

        # 4. GET cpu_usage (not found)
        s.sendall(b"GET cpu_usage 1678886401\n")
        resp = s.recv(1024).decode('utf-8')
        assert resp == "NOT_FOUND\n", f"Expected 'NOT_FOUND\\n' for GET, got {repr(resp)}"

        # 5. SYNC
        s.sendall(b"SYNC -2147485000\n")
        resp = s.recv(1024).decode('utf-8')
        assert resp == "OK -1400\n", f"Expected 'OK -1400\\n' for SYNC, got {repr(resp)}"

    finally:
        s.close()