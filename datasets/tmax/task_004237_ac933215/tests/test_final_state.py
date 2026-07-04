# test_final_state.py

import socket
import os
import time
import pytest

def djb2_hash(s):
    hash_val = 5381
    for char in s:
        # Simulate 64-bit unsigned long overflow behavior
        hash_val = ((hash_val << 5) + hash_val + ord(char)) & 0xFFFFFFFFFFFFFFFF
    return f"GRAPH_NODE_{hash_val:lx}"

def send_request_and_get_response(host, port, request_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        s.sendall(request_str.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    return response

def test_service_responses():
    host = '127.0.0.1'
    port = 8081

    test_cases = [
        ("SELECT * FROM users JOIN orders ON users.id = orders.u_id\n", "users", "orders"),
        ("SELECT * FROM tableA JOIN tableB ON cond\n", "tableA", "tableB"),
        ("SELECT * FROM customers JOIN invoices ON c.id=i.cid\n", "customers", "invoices")
    ]

    for req, t1, t2 in test_cases:
        expected_out1 = djb2_hash(t1)
        expected_out2 = djb2_hash(t2)
        expected_response = f"PIPELINE: {expected_out1} -> {expected_out2}\n"

        try:
            actual_response = send_request_and_get_response(host, port, req)
        except Exception as e:
            pytest.fail(f"Failed to communicate with service on {host}:{port} for request '{req.strip()}': {e}")

        assert actual_response == expected_response, \
            f"Expected response '{expected_response.strip()}', but got '{actual_response.strip()}'"

def test_log_file_exists_and_contains_requests():
    log_path = "/home/user/wrapper.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"Path {log_path} is not a file."

    with open(log_path, 'r') as f:
        log_contents = f.read()

    # Check if at least one of our test requests made it into the log
    assert "users" in log_contents or "orders" in log_contents or "tableA" in log_contents, \
        f"Log file {log_path} does not appear to contain the incoming requests."