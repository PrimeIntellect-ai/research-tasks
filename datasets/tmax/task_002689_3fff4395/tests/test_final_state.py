# test_final_state.py
import os
import socket
import subprocess
import requests
import pytest

def test_minimal_repro_exists():
    path = "/home/user/minimal_repro.sh"
    assert os.path.isfile(path), f"Missing minimal repro script at {path}"

def test_bad_commit_hash():
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"Missing bad commit file at {path}"

    with open(path, "r") as f:
        user_hash = f.read().strip()

    # Get the actual bad commit hash from the git repository
    repo_dir = "/app/services/proxy_src/"
    try:
        result = subprocess.run(
            ["git", "log", "--grep=Refactor header parsing", "--format=%H"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True
        )
        expected_hash = result.stdout.strip().split("\n")[0].strip()
    except Exception as e:
        pytest.fail(f"Could not retrieve expected commit hash from git repo: {e}")

    assert expected_hash, "Could not find commit with message 'Refactor header parsing'"
    assert user_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {user_hash}"

def test_proxy_http_basic():
    try:
        response = requests.get("http://localhost:9000/", timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Basic HTTP request to proxy failed: {e}")

def test_proxy_tcp_mgmt():
    try:
        with socket.create_connection(("localhost", 9002), timeout=5) as s:
            s.sendall(b"STATUS\n")
            data = s.recv(1024)
            response = data.decode("utf-8").strip()
            assert "PROXY_OK" in response, f"Expected PROXY_OK, got {response}"
    except Exception as e:
        pytest.fail(f"TCP management request to proxy failed: {e}")

def test_proxy_leak_fix():
    # Perform leak test: open and abruptly close 2000 connections
    for _ in range(2000):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(("localhost", 9000))
            # Abruptly close the connection without sending data
            s.close()
        except Exception:
            # If we can't even connect 2000 times, the proxy might have already crashed
            pass

    # Verify the proxy is still alive and responding
    try:
        response = requests.get("http://localhost:9000/", timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200 OK after leak test, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to proxy failed after leak test (likely exhausted file descriptors): {e}")