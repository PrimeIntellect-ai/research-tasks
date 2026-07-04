# test_final_state.py

import os
import socket
import subprocess
import pytest

def get_actual_bad_commit():
    """Find the first commit after v1.0 that introduced the bug."""
    repo_path = "/home/user/sensor_repo"

    # Get all commits from v1.0 to master, in chronological order
    result = subprocess.run(
        ["git", "rev-list", "--reverse", "v1.0..master"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    commits = result.stdout.strip().split('\n')

    for commit in commits:
        if not commit:
            continue
        # Check the contents of server.sh at this commit
        show_result = subprocess.run(
            ["git", "show", f"{commit}:server.sh"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        content = show_result.stdout
        # The bad commit introduced a loop with '<' instead of '<=' or removed kahan_oracle
        if "kahan_oracle" not in content or "<${#" in content.replace(" ", ""):
            return commit
    return None

def test_bad_commit_identified():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        student_commit = f.read().strip()

    actual_bad_commit = get_actual_bad_commit()
    assert actual_bad_commit is not None, "Could not determine the actual bad commit from the repository."

    # Allow full hash or short hash
    assert student_commit and actual_bad_commit.startswith(student_commit), \
        f"Incorrect bad commit identified. Expected {actual_bad_commit}, got {student_commit}."

def test_server_invalid_auth():
    try:
        with socket.create_connection(("127.0.0.1", 8888), timeout=3) as s:
            s.sendall(b"AUTH: bad_token\n")
            response = s.recv(1024).decode('utf-8')
            assert response == "AUTH_FAIL\n", f"Expected AUTH_FAIL\\n, got {repr(response)}"
            # Socket should be closed by server
            assert s.recv(1024) == b"", "Server did not close the connection after AUTH_FAIL"
    except ConnectionRefusedError:
        pytest.fail("Server is not listening on 127.0.0.1:8888")

def test_server_valid_auth_and_data():
    try:
        with socket.create_connection(("127.0.0.1", 8888), timeout=3) as s:
            s.sendall(b"AUTH: v2_auth_token_xyz\n")
            response = s.recv(1024).decode('utf-8')
            assert response == "AUTH_OK\n", f"Expected AUTH_OK\\n, got {repr(response)}"

            s.sendall(b"DATA: 10.5 0.1 0.1\n")
            response2 = s.recv(1024).decode('utf-8')
            assert response2 == "RESULT: 10.700000\n", f"Expected RESULT: 10.700000\\n, got {repr(response2)}"
    except ConnectionRefusedError:
        pytest.fail("Server is not listening on 127.0.0.1:8888")

def test_server_precision_and_parsing():
    try:
        with socket.create_connection(("127.0.0.1", 8888), timeout=3) as s:
            s.sendall(b"AUTH: v2_auth_token_xyz\n")
            response = s.recv(1024).decode('utf-8')
            assert response == "AUTH_OK\n", f"Expected AUTH_OK\\n, got {repr(response)}"

            # This tests both the off-by-one error (last element must be processed) 
            # and precision (catastrophic cancellation if not using Kahan)
            s.sendall(b"DATA: 100000000.0 0.000001 -100000000.0\n")
            response2 = s.recv(1024).decode('utf-8')
            assert response2 == "RESULT: 0.000001\n", f"Expected RESULT: 0.000001\\n, got {repr(response2)}"
    except ConnectionRefusedError:
        pytest.fail("Server is not listening on 127.0.0.1:8888")