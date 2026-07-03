# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

APP_DIR = "/home/user/app"
SO_FILE = os.path.join(APP_DIR, "libmathcore.so")
LOG_FILE = os.path.join(APP_DIR, "release_test.log")

def test_shared_library_exists():
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} does not exist."

    # Check if it's an ELF file
    with open(SO_FILE, "rb") as f:
        magic = f.read(4)
    assert magic == b'\x7fELF', f"File {SO_FILE} is not a valid ELF shared object."

def test_release_test_log():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        content = f.read().strip()

    # 4^3 + 3^2 - 4*3 = 64 + 9 - 12 = 61
    expected_result = "Result: 61.0"
    assert expected_result in content, f"Log file {LOG_FILE} does not contain the expected string '{expected_result}'. Found: {content}"

def test_server_eval_endpoint():
    # Test with x=2.0, y=5.0
    # 2^3 + 5^2 - 2*5 = 8 + 25 - 10 = 23
    url = "http://127.0.0.1:8080/eval?x=2.0&y=5.0"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            expected_body = "Result: 23.0"
            assert expected_body in body, f"Expected response to contain '{expected_body}', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the server or fetch the URL: {e}")