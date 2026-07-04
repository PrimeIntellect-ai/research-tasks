# test_final_state.py

import urllib.request
import urllib.error
import time
import json
import os
import pytest

BASE_URL = "http://127.0.0.1:8080/api/build"

def test_rust_project_exists():
    """Verify the build_broker project directory exists."""
    assert os.path.isdir("/home/user/build_broker"), "The build_broker directory does not exist."

def test_invalid_target_returns_400():
    """Verify that a target other than rust or cpp returns a 400 Bad Request."""
    req = urllib.request.Request(
        f"{BASE_URL}/java", 
        data=b"CMD javac\nRUN", 
        method="POST"
    )
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected HTTP 400 for invalid target 'java', but got a successful response.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 for invalid target, got {e.code}."

def test_valid_target_parsing_and_rate_limiting():
    """Verify target processing, mini-language parsing, rate limiting, and WS dispatch."""
    # Wait to ensure any previous manual tests don't trigger the rate limit
    time.sleep(1.1)

    unique_id = int(time.time() * 1000)
    cmd1 = f"gcc main_{unique_id}.c"

    # Test 1: Valid request
    script1 = f"ENV OPT=-O3\nCMD {cmd1}\nENV DEBUG=1\nRUN\nCMD ignore"
    req1 = urllib.request.Request(
        f"{BASE_URL}/cpp", 
        data=script1.encode("utf-8"), 
        method="POST"
    )
    try:
        resp1 = urllib.request.urlopen(req1)
        assert resp1.getcode() == 200, f"Expected HTTP 200, got {resp1.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 for valid request, got {e.code}")

    # Test 2: Immediate second request should be rate limited
    req2 = urllib.request.Request(
        f"{BASE_URL}/cpp", 
        data=b"CMD g++\nRUN", 
        method="POST"
    )
    try:
        urllib.request.urlopen(req2)
        pytest.fail("Expected HTTP 429 Too Many Requests due to rate limiting.")
    except urllib.error.HTTPError as e:
        assert e.code == 429, f"Expected HTTP 429 for rate limit, got {e.code}."

    # Test 3: Wait for rate limit to expire, then send another request
    time.sleep(1.2)

    cmd2 = f"g++ main_{unique_id}.cpp"
    req3 = urllib.request.Request(
        f"{BASE_URL}/cpp", 
        data=f"CMD {cmd2}\nRUN".encode("utf-8"), 
        method="POST"
    )
    try:
        resp3 = urllib.request.urlopen(req3)
        assert resp3.getcode() == 200, f"Expected HTTP 200 after waiting, got {resp3.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 after rate limit expired, got {e.code}")

    # Give the WebSocket server a moment to write to the log
    time.sleep(0.5)

    # Test 4: Verify WebSocket dispatch
    log_path = "/home/user/ws_out.log"
    assert os.path.exists(log_path), f"WebSocket log file {log_path} not found."

    with open(log_path, "r") as f:
        lines = f.read().strip().split("\n")

    job1 = None
    job2 = None

    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            if data.get("cmd") == cmd1:
                job1 = data
            elif data.get("cmd") == cmd2:
                job2 = data
        except json.JSONDecodeError:
            continue

    assert job1 is not None, "The first job was not correctly dispatched to the WebSocket server."
    assert job1.get("target") == "cpp", f"Expected target 'cpp', got {job1.get('target')}"
    assert job1.get("env", {}).get("OPT") == "-O3", "Environment variable OPT was not parsed correctly."
    assert job1.get("env", {}).get("DEBUG") == "1", "Environment variable DEBUG was not parsed correctly."

    assert job2 is not None, "The second job was not correctly dispatched to the WebSocket server."
    assert job2.get("target") == "cpp", f"Expected target 'cpp', got {job2.get('target')}"