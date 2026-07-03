# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

WORKSPACE_DIR = "/home/user/workspace"
SCHEDULER_C_PATH = "/home/user/workspace/scheduler.c"
LIBSCHEDULER_SO_PATH = "/home/user/workspace/libscheduler.so"
FINAL_SCHEDULE_JSON_PATH = "/home/user/workspace/final_schedule.json"

def test_c_code_fixed():
    """Test that the C code has been modified to fix the three bugs."""
    assert os.path.exists(SCHEDULER_C_PATH), f"File missing: {SCHEDULER_C_PATH}"

    with open(SCHEDULER_C_PATH, 'r') as f:
        content = f.read()

    # Bug 1: Off-by-one error in malloc
    assert "malloc(strlen(input))" not in content.replace(" ", ""), "Bug 1 (Off-by-one in malloc) is not fixed."

    # Bug 2: Buffer overflow in task name array
    assert "char name[10]" not in content, "Bug 2 (Buffer overflow with char name[10]) is not fixed."

    # Bug 3: Memory leak of 'copy'
    assert "free(" in content, "Bug 3 (Memory leak) is not fixed. Missing free() call."

def test_shared_library_compiled():
    """Test that the shared library was compiled."""
    assert os.path.exists(LIBSCHEDULER_SO_PATH), f"Shared library missing: {LIBSCHEDULER_SO_PATH}"
    assert os.path.isfile(LIBSCHEDULER_SO_PATH), f"Expected a file: {LIBSCHEDULER_SO_PATH}"

def test_final_schedule_json():
    """Test that the final_schedule.json contains the expected output."""
    assert os.path.exists(FINAL_SCHEDULE_JSON_PATH), f"File missing: {FINAL_SCHEDULE_JSON_PATH}"

    with open(FINAL_SCHEDULE_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON in final_schedule.json")

    expected = [
        {"name": "DesignSystemArchitecture", "start": 0},
        {"name": "ImplementFFI", "start": 15},
        {"name": "WriteTests", "start": 23}
    ]

    assert data == expected, f"Data mismatch in final_schedule.json. Got: {data}"

def test_web_service_running_and_correct():
    """Test that the web service is running and correctly processes a schedule request."""
    payload = [
        {"name": "TaskA", "duration": 10},
        {"name": "TaskB", "duration": 20}
    ]
    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        "http://127.0.0.1:8080/schedule",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            resp_data = json.loads(resp_body)

            expected_resp = [
                {"name": "TaskA", "start": 0},
                {"name": "TaskB", "start": 10}
            ]
            assert resp_data == expected_resp, f"Service returned incorrect schedule. Got: {resp_data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Web service is not reachable or failed: {e}")
    except json.JSONDecodeError:
        pytest.fail("Web service did not return valid JSON.")