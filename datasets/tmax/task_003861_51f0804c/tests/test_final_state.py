# test_final_state.py

import os
import socket
import subprocess
import pytest

def test_bad_commit_identified():
    repo_path = "/home/user/math_server"
    bad_commit_file = "/home/user/bad_commit.txt"

    assert os.path.exists(bad_commit_file), f"Expected {bad_commit_file} to exist."

    # The setup creates 4 commits initially. 
    # Commit 1: Initial
    # Commit 2: Server
    # Commit 3: Regression (This is the bad one)
    # Commit 4: Crash
    # We can find the 3rd commit chronologically by looking at all commits in the reflog or assuming the first 4 commits of the original master branch.
    # To be safe against the user changing branches, we can search for the commit that introduced the regression by looking at the initial commits.
    # We'll use git rev-list to get the commits in chronological order from the original history (assuming they didn't rewrite the first 4 commits).
    try:
        # We can find the root commit and get its descendants, or just use `git log --reverse` on the original branch if it exists.
        # Assuming the original commits are still in the repository, we can find the commit with the message indicating regression, 
        # or simply get the first 4 commits from the reflog of HEAD.
        # A more robust way: find the commit that is the parent of the commit that crashes, or just the 3rd commit overall.
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%H"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split('\n')
        assert len(commits) >= 4, "Expected at least 4 commits in the repository history."
        expected_bad_commit = commits[2]  # 3rd commit
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git log: {e.stderr}")

    with open(bad_commit_file, "r") as f:
        actual_bad_commit = f.read().strip()

    assert actual_bad_commit == expected_bad_commit, (
        f"Incorrect bad commit hash in {bad_commit_file}. "
        f"Expected {expected_bad_commit}, got {actual_bad_commit}."
    )

def test_tcp_server_responses():
    host = "127.0.0.1"
    port = 8080

    test_cases = [
        ("5", "11"),
        ("10", "341"),
        ("0", "0"),
        ("1", "1"),
        ("6", "21"),
        ("7", "43")
    ]

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Failed to connect to the math server at {host}:{port}: {e}")

    for inp, expected in test_cases:
        try:
            s.sendall(f"{inp}\n".encode("utf-8"))

            response = b""
            while b"\n" not in response:
                chunk = s.recv(1024)
                if not chunk:
                    break
                response += chunk

            response_str = response.decode("utf-8").strip()
            assert response_str == expected, (
                f"Server returned incorrect result for input '{inp}'. "
                f"Expected '{expected}', got '{response_str}'."
            )
        except AssertionError:
            raise
        except Exception as e:
            pytest.fail(f"Error communicating with server for input '{inp}': {e}")

    try:
        s.close()
    except:
        pass