# test_final_state.py
import os
import json
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_unit_tests_log():
    log_path = "/home/user/unit_tests.log"
    assert os.path.isfile(log_path), f"Unit test log missing at {log_path}"
    with open(log_path, 'r') as f:
        content = f.read()
    assert "PASS" in content, "The unit tests did not pass or 'PASS' is missing from the log."

def test_e2e_results():
    res_path = "/home/user/e2e_results.json"
    assert os.path.isfile(res_path), f"E2E results missing at {res_path}"
    with open(res_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("e2e_results.json is not valid JSON")

    assert "distance" in data, "Key 'distance' not found in e2e_results.json"
    assert data["distance"] == 2, f"Expected distance 2 for 'book' and 'back', got {data['distance']}"

def test_api_server():
    app_dir = "/home/user/app"
    assert os.path.isdir(app_dir), f"{app_dir} does not exist"

    # Build the server
    build_proc = subprocess.run(
        ["go", "build", "-o", "server", "."], 
        cwd=app_dir, 
        capture_output=True
    )
    assert build_proc.returncode == 0, f"Failed to build Go app: {build_proc.stderr.decode('utf-8')}"

    # Run the server
    server_proc = subprocess.Popen(["./server"], cwd=app_dir)

    try:
        # Wait for server to start
        time.sleep(2)

        # Make a valid request
        req = urllib.request.Request(
            "http://localhost:8080/api/v1/levenshtein",
            data=json.dumps({"str1": "apple", "str2": "apply"}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                resp_body = response.read().decode('utf-8')
                try:
                    data = json.loads(resp_body)
                except json.JSONDecodeError:
                    pytest.fail(f"API response is not valid JSON: {resp_body}")

                assert data.get("distance") == 1, f"Expected distance 1 for 'apple' and 'apply', got {data.get('distance')}"
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to API or request failed: {e}")

        # Test 400 Bad Request
        req_bad = urllib.request.Request(
            "http://localhost:8080/api/v1/levenshtein",
            data=b"invalid json",
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req_bad) as response:
                pytest.fail("Expected 400 Bad Request for invalid JSON, but got 200 OK")
        except urllib.error.HTTPError as e:
            assert e.code == 400, f"Expected HTTP 400 Bad Request, got {e.code}"

    finally:
        server_proc.terminate()
        server_proc.wait()