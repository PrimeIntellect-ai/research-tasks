# test_final_state.py

import os
import requests
import time

def test_api_server_responses():
    url = "http://127.0.0.1:8080/analyze"
    headers = {"X-Ops-Token": "triage-2024"}

    # Retry a few times in case the server is just starting
    max_retries = 5
    for i in range(max_retries):
        try:
            # Test 1: Normal frame range
            params1 = {"start_frame": 10, "end_frame": 30}
            resp1 = requests.get(url, params=params1, headers=headers, timeout=5)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                assert False, "API server is not running or not reachable on 127.0.0.1:8080"
            time.sleep(1)

    assert resp1.status_code == 200, f"Expected 200 OK, got {resp1.status_code}. Response: {resp1.text}"

    try:
        data1 = resp1.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {resp1.text}"

    assert "motion_index" in data1, "Response missing 'motion_index' key"
    assert isinstance(data1["motion_index"], (float, int)), "motion_index must be a number"

    # Test 2: Highly static frame range to check for numerical instability fix
    params2 = {"start_frame": 0, "end_frame": 2}
    resp2 = requests.get(url, params=params2, headers=headers, timeout=5)

    assert resp2.status_code == 200, (
        f"Expected 200 OK for static frame range, got {resp2.status_code}. "
        f"The numerical instability bug might not be fixed. Response: {resp2.text}"
    )

    try:
        data2 = resp2.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {resp2.text}"

    assert "motion_index" in data2, "Response missing 'motion_index' key"
    assert isinstance(data2["motion_index"], (float, int)), "motion_index must be a number"

def test_api_code_assertions():
    api_path = "/home/user/api.py"
    assert os.path.exists(api_path), f"File not found: {api_path}"

    with open(api_path, "r") as f:
        content = f.read()

    assert "assert " in content, "No 'assert' statement found in the code. You must add assertion-based intermediate validation."