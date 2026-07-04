# test_final_state.py

import os
import json
import base64
import ctypes
import urllib.request
import urllib.error

def test_shared_library_exists_and_exports():
    """Verify that libchecksum.so exists and exports compute_weighted_checksum."""
    so_path = "/home/user/libchecksum.so"
    assert os.path.exists(so_path), f"Shared library {so_path} does not exist."

    try:
        lib = ctypes.CDLL(so_path)
    except OSError as e:
        assert False, f"Failed to load {so_path}: {e}"

    assert hasattr(lib, "compute_weighted_checksum"), "compute_weighted_checksum function is not exported by the shared library."

def test_api_running_and_correct():
    """Verify that the Flask API is running and returns the correct checksum."""
    url = "http://127.0.0.1:8080/checksum"

    # "test" -> bytes [116, 101, 115, 116]
    # checksum: 116*1 + 101*2 + 115*3 + 116*4 = 116 + 202 + 345 + 464 = 1127
    payload_bytes = b"test"
    encoded_payload = base64.b64encode(payload_bytes).decode("utf-8")

    data = json.dumps({"payload": encoded_payload}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            resp_body = response.read().decode("utf-8")
            resp_json = json.loads(resp_body)

            assert "checksum" in resp_json, "Response JSON missing 'checksum' key"
            assert resp_json["checksum"] == 1127, f"Expected checksum 1127, got {resp_json['checksum']}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to API or API returned error: {e}"
    except json.JSONDecodeError:
        assert False, "API did not return valid JSON."

def test_test_results_log():
    """Verify that test_results.log exists and indicates passed tests."""
    log_path = "/home/user/test_results.log"
    assert os.path.exists(log_path), f"Test results log {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "passed" in content.lower(), "Test results log does not indicate that tests passed. Expected 'passed' in log."