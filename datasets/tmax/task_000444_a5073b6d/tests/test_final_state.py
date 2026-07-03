# test_final_state.py
import os
import requests

def test_payload_eval_binary_exists():
    binary_path = "/home/user/helper_tool/payload_eval"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist. Did you fix CMakeLists.txt and build?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_server_behavior():
    TOKEN = "QA-BASH-TOKEN-8832"
    URL = "http://127.0.0.1:8080/submit"

    # 1. Send POST without auth -> Expect 401 Unauthorized
    try:
        r1 = requests.post(URL, data="150", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {URL}. Is it running? Error: {e}"

    assert r1.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {r1.status_code}"

    headers = {"Authorization": f"Bearer {TOKEN}"}

    # 2. Send POST with auth and bad payload -> Expect 400 Bad Request
    # The C program checks if sqrt(val) > 10.0. So val <= 100 is invalid.
    r2 = requests.post(URL, headers=headers, data="50", timeout=5)
    assert r2.status_code == 400, f"Expected 400 Bad Request for invalid payload, got {r2.status_code}"

    # 3. Send POST with auth and good payload 3 times rapidly -> Expect 200 OK
    for i in range(3):
        r_success = requests.post(URL, headers=headers, data="150", timeout=5)
        assert r_success.status_code == 200, f"Expected 200 OK on successful request {i+1}, got {r_success.status_code}"

    # 4. Send a 4th POST immediately -> Expect 429 Too Many Requests
    r_rate_limit = requests.post(URL, headers=headers, data="150", timeout=5)
    assert r_rate_limit.status_code == 429, f"Expected 429 Too Many Requests on 4th rapid request, got {r_rate_limit.status_code}"