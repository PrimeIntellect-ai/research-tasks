# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_success_log_content():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The verify script may not have run or failed to create it."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_text = "Backend Service Operational"
    assert expected_text in content, f"Expected '{expected_text}' in {log_path}, but found: {content}"

def test_verify_script_exists():
    script_path = "/home/user/verify.py"
    assert os.path.isfile(script_path), f"File {script_path} does not exist. You must create the verification script."

def test_nginx_and_backend_running():
    url = "http://127.0.0.1:8080"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode("utf-8").strip()

            assert status == 200, f"Expected HTTP status 200, got {status}."
            assert "Backend Service Operational" in body, f"Unexpected response body: {body}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP request failed with status {e.code}. Nginx might still be returning a 502 Bad Gateway.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url}: {e.reason}. Nginx might not be running or listening on port 8080.")
    except Exception as e:
        pytest.fail(f"Unexpected error when connecting to {url}: {e}")

def test_server_py_port_fixed():
    server_path = "/home/user/app/server.py"
    assert os.path.isfile(server_path), f"File {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    assert "8081" in content, "The port in server.py does not appear to be updated to 8081."
    assert "9000" not in content, "The incorrect port 9000 is still present in server.py."