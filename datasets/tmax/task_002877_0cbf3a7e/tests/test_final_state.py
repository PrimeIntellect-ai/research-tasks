# test_final_state.py

import os
import http.client
import pytest

def test_httplib_fixed():
    path = "/app/vendored/cpp-httplib/httplib.h"
    assert os.path.isfile(path), f"Expected vendored httplib header to exist at {path}"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    assert "class BrokenServerXYZ" not in content, "The httplib.h file still contains the broken class name 'BrokenServerXYZ'"
    assert "class Server {" in content or "class Server" in content, "The httplib.h file does not contain the fixed 'class Server'"

def test_server_binary_exists():
    path = "/app/server/waf_server"
    assert os.path.isfile(path), f"Expected C++ server binary to exist at {path}"
    assert os.access(path, os.X_OK), f"Expected {path} to be executable"

def test_tester_go_exists():
    path = "/app/tester/tester.go"
    assert os.path.isfile(path), f"Expected Go tester file to exist at {path}"

@pytest.mark.parametrize("path, expected_status, expected_body", [
    ("/hello", 200, "OK"),
    ("/..%2f", 403, "Blocked"),
    ("/%252e%252e%2f", 403, "Blocked"),
    ("/%c0%ae%c0%ae%c0%af", 403, "Blocked"),
])
def test_waf_behavior(path, expected_status, expected_body):
    conn = http.client.HTTPConnection("127.0.0.1", 8080, timeout=5)
    try:
        # Using http.client to prevent any client-side URL normalization
        conn.request("GET", path)
        response = conn.getresponse()
        status = response.status
        body = response.read().decode("utf-8").strip()
    except Exception as e:
        pytest.fail(f"Failed to connect or read from server at 127.0.0.1:8080: {e}")
    finally:
        conn.close()

    assert status == expected_status, f"Expected status {expected_status} for path {path}, got {status}"
    assert body == expected_body, f"Expected body '{expected_body}' for path {path}, got '{body}'"