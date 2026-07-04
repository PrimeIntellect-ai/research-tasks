# test_final_state.py

import os
import json
import urllib.request
import subprocess
import sys
import importlib.util

def test_success_file():
    success_file = "/home/user/workspace/SUCCESS"
    assert os.path.exists(success_file), f"{success_file} does not exist."
    with open(success_file, "r") as f:
        content = f.read().strip()
    assert "DONE" in content, f"{success_file} does not contain 'DONE'."

def test_pytest_suite_passes():
    test_file = "/home/user/workspace/test_sanitizer.py"
    assert os.path.exists(test_file), f"{test_file} does not exist."

    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file],
        cwd="/home/user/workspace",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest suite failed:\n{result.stdout}\n{result.stderr}"

def test_sanitizer_module():
    sanitizer_path = "/home/user/workspace/sanitizer.py"
    assert os.path.exists(sanitizer_path), f"{sanitizer_path} does not exist."

    spec = importlib.util.spec_from_file_location("sanitizer", sanitizer_path)
    sanitizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sanitizer)

    assert hasattr(sanitizer, "sanitize_payload"), "sanitize_payload function missing in sanitizer.py"

    raw_payload = b'{"z": 1, "_hidden": "secret", "a": {"_ignore": true, "c": [3, 2, 1], "b": 2}}'
    expected = b'{"a":{"b":2,"c":[3,2,1]},"z":1}'

    result = sanitizer.sanitize_payload(raw_payload)
    assert result == expected, f"sanitize_payload returned {result} instead of {expected}"

def test_proxy_server():
    raw_payload = b'{"z": 1, "_hidden": "secret", "a": {"_ignore": true, "c": [3, 2, 1], "b": 2}}'
    expected_body = '{"a":{"b":2,"c":[3,2,1]},"z":1}'

    req = urllib.request.Request(
        "http://127.0.0.1:8080/api/test",
        data=raw_payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Proxy returned status {response.status}"
            resp_body = response.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to communicate with proxy server on port 8080: {e}")

    try:
        resp_json = json.loads(resp_body)
    except json.JSONDecodeError:
        pytest.fail(f"Proxy did not return valid JSON: {resp_body}")

    received_body = resp_json.get("received_body", "")
    assert received_body == expected_body, f"Proxy did not sanitize correctly. Expected: '{expected_body}', Got: '{received_body}'"
    assert resp_json.get("received_path") == "/api/test", "Proxy did not preserve the URL path."