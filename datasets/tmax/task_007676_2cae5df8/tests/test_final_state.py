# test_final_state.py

import os
import socket
import pytest

def test_libparser_so_exists():
    path = "/home/user/workspace/lib/libparser.so"
    assert os.path.isfile(path), f"Shared library {path} was not built or is missing."

def test_integration_results_log():
    log_path = "/home/user/workspace/integration_results.log"
    assert os.path.isfile(log_path), f"Integration log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, "Log file does not have the expected number of lines."
    assert "VERSION_REJECTED" in lines[0], "First line does not contain 'VERSION_REJECTED'."

    expected_success = "SUCCESS: {PROCESSED: " + ("A" * 500) + "}"
    assert expected_success in lines[1], "Second line does not contain the expected SUCCESS message with 500 'A's."

def test_nginx_running_port_8080():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Nothing is listening on port 8080 (expected Nginx)."

def test_backend_running_port_9000():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 9000))
        assert result == 0, "Nothing is listening on port 9000 (expected Python backend)."