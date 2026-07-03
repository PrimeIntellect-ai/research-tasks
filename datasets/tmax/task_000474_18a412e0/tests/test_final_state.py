# test_final_state.py

import socket
import threading
import time
import os
import pytest

HOST = '127.0.0.1'
PORT = 9090

def send_request(request_str: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((HOST, PORT))
        s.sendall(request_str.encode('utf-8'))

        # Read until newline or timeout
        response = b""
        while b"\n" not in response:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk

        return response.decode('utf-8')

def test_get_corrupted():
    try:
        response = send_request("GET_CORRUPTED\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with the server for GET_CORRUPTED: {e}")

    assert response.strip() == "archive_corrupted.tar.gz", f"Expected 'archive_corrupted.tar.gz', got '{response.strip()}'"

def test_get_token():
    try:
        response = send_request("GET_TOKEN\n")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with the server for GET_TOKEN: {e}")

    assert response.strip() == "s3cr3tKEY", f"Expected 's3cr3tKEY', got '{response.strip()}'"

def test_record_access_concurrency():
    # Clear or create the access log
    log_path = "/home/user/access.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    num_threads = 20
    responses = []
    exceptions = []

    def worker(thread_id):
        try:
            resp = send_request(f"RECORD_ACCESS test_entry_{thread_id}\n")
            responses.append((thread_id, resp))
        except Exception as e:
            exceptions.append(e)

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    assert not exceptions, f"Exceptions occurred during concurrent requests: {exceptions}"

    for _, resp in responses:
        assert resp.strip() == "OK", f"Expected 'OK' response for RECORD_ACCESS, got '{resp.strip()}'"

    assert os.path.isfile(log_path), f"{log_path} does not exist after RECORD_ACCESS commands"

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    # Filter out any empty lines
    lines = [line for line in lines if line.strip()]

    assert len(lines) == num_threads, f"Expected {num_threads} entries in {log_path}, found {len(lines)}"

    expected_entries = set(f"test_entry_{i}" for i in range(num_threads))
    actual_entries = set(lines)

    missing = expected_entries - actual_entries
    assert not missing, f"Missing entries in {log_path} due to race conditions: {missing}"