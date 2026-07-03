# test_final_state.py
import os
import socket
import pytest

def test_ordered_files_content():
    ordered_files_path = "/home/user/ordered_files.txt"
    assert os.path.isfile(ordered_files_path), f"Missing {ordered_files_path}"

    with open(ordered_files_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "125 /home/user/project/src/main.c",
        "16 /home/user/project/src/auth.sh",
        "10 /home/user/project/docs/readme.md"
    ]

    assert content == expected_content, f"Contents of {ordered_files_path} do not match expected priorities and paths."

def test_order_diff_patch_exists():
    patch_path = "/home/user/order_diff.patch"
    assert os.path.isfile(patch_path), f"Missing {patch_path}"

    with open(patch_path, "r") as f:
        content = f.read()

    # A standard unified diff should have these diff markers
    assert "---" in content and "+++" in content, f"{patch_path} does not look like a unified diff"
    assert "/home/user/project/src/auth.sh" in content, "Patch missing expected file paths"

def send_query(query_str: str) -> str:
    host = "127.0.0.1"
    port = 9000
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(query_str.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with service on {host}:{port}. Error: {e}")

def test_tcp_service_query_1():
    response = send_query("QUERY 2^4\n")
    assert response == "/home/user/project/src/auth.sh\n", f"Unexpected response: {response}"

def test_tcp_service_query_2():
    response = send_query("QUERY 100/10\n")
    assert response == "/home/user/project/docs/readme.md\n", f"Unexpected response: {response}"

def test_tcp_service_query_3():
    response = send_query("QUERY 5*5*5\n")
    assert response == "/home/user/project/src/main.c\n", f"Unexpected response: {response}"

def test_tcp_service_not_found():
    response = send_query("QUERY 999\n")
    assert response == "NOT_FOUND\n", f"Unexpected response: {response}"