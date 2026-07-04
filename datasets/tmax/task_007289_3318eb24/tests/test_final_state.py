# test_final_state.py

import os
import re

def test_test_results_log():
    """Verify that test_results.log exists and contains PASS."""
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "PASS" in content, "Tests did not pass or 'PASS' is missing from test_results.log."

def test_proxy_test_log_header():
    """Verify that proxy_test.log exists and contains the required security header."""
    log_path = "/home/user/proxy_test.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert re.search(r"X-Deployment-Sec:\s*Ready", content, re.IGNORECASE), "Missing security header 'X-Deployment-Sec: Ready' in proxy response."

def test_proxy_test_log_body():
    """Verify that proxy_test.log contains the correct entropy calculation output."""
    log_path = "/home/user/proxy_test.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for "entropy": 2 or "entropy": 2.0
    match = re.search(r'"entropy"\s*:\s*2(?:\.0)?', content)
    assert match is not None, "Incorrect entropy calculation or missing JSON response in proxy_test.log."

def test_source_code_structure():
    """Verify that the required source code directories and files exist."""
    assert os.path.isdir("/home/user/analyzer"), "/home/user/analyzer directory does not exist."
    assert os.path.isfile("/home/user/analyzer/go.mod"), "/home/user/analyzer/go.mod does not exist."
    assert os.path.isfile("/home/user/analyzer/entropy.go"), "/home/user/analyzer/entropy.go does not exist."
    assert os.path.isfile("/home/user/analyzer/entropy_test.go"), "/home/user/analyzer/entropy_test.go does not exist."
    assert os.path.isfile("/home/user/analyzer/main.go"), "/home/user/analyzer/main.go does not exist."

    assert os.path.isdir("/home/user/proxy"), "/home/user/proxy directory does not exist."
    assert os.path.isfile("/home/user/proxy/go.mod"), "/home/user/proxy/go.mod does not exist."
    assert os.path.isfile("/home/user/proxy/main.go"), "/home/user/proxy/main.go does not exist."