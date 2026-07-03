# test_final_state.py

import os
import glob
import socket
import requests
import pytest

DOCS_DIR = "/home/user/organized_docs"
EXPECTED_COUNT = 25
SECRET_CODENAME = "VANGUARD"

def test_organized_docs_count():
    """Verify that the organized_docs directory contains exactly 25 .txt files."""
    assert os.path.isdir(DOCS_DIR), f"Directory {DOCS_DIR} does not exist."
    txt_files = glob.glob(os.path.join(DOCS_DIR, "*.txt"))
    assert len(txt_files) == EXPECTED_COUNT, f"Expected {EXPECTED_COUNT} .txt files in {DOCS_DIR}, but found {len(txt_files)}."

def test_http_server():
    """Verify the HTTP server is serving the files correctly."""
    url = "http://127.0.0.1:8080/file1.txt"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."
    assert len(response.text) > 0, "Expected file1.txt to have content."

def test_tcp_server_valid_auth():
    """Verify the TCP server accepts valid auth and returns the correct count."""
    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=2) as s:
            # Test AUTH
            s.sendall(f"AUTH {SECRET_CODENAME}\n".encode('utf-8'))
            auth_response = s.recv(1024).decode('utf-8')
            assert auth_response == "OK\n", f"Expected 'OK\\n' for valid auth, got {repr(auth_response)}"

            # Test COUNT
            s.sendall(b"COUNT\n")
            count_response = s.recv(1024).decode('utf-8')
            expected_count_response = f"FILES: {EXPECTED_COUNT}\n"
            assert count_response == expected_count_response, f"Expected '{expected_count_response}', got {repr(count_response)}"
    except ConnectionRefusedError:
        pytest.fail("Connection to TCP server at 127.0.0.1:9090 was refused.")
    except socket.timeout:
        pytest.fail("TCP server at 127.0.0.1:9090 timed out.")

def test_tcp_server_invalid_auth():
    """Verify the TCP server rejects invalid auth and closes the connection."""
    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=2) as s:
            s.sendall(b"AUTH INVALID\n")
            auth_response = s.recv(1024).decode('utf-8')
            assert auth_response == "ERROR\n", f"Expected 'ERROR\\n' for invalid auth, got {repr(auth_response)}"

            # Check if connection is closed
            s.settimeout(1)
            try:
                extra_data = s.recv(1024)
                assert len(extra_data) == 0, "Expected connection to be closed, but received more data."
            except socket.timeout:
                pytest.fail("Expected connection to be closed, but it timed out waiting for EOF.")
    except ConnectionRefusedError:
        pytest.fail("Connection to TCP server at 127.0.0.1:9090 was refused.")
    except socket.timeout:
        pytest.fail("TCP server at 127.0.0.1:9090 timed out.")