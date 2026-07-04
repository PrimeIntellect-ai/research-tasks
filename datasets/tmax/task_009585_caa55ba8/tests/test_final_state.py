# test_final_state.py

import os
import stat
import time
import urllib.request
import urllib.error
import pytest

SECRET = "987654321-NEW-SECRET"
LOG_PATH = "/home/user/legacy-svc/app.log"
API_KEY_PATH = "/home/user/secrets/api.key"
REPORT_PATH = "/home/user/rotation_report.txt"
BASE_URL = "http://127.0.0.1:8080/auth"

def test_api_key_file():
    assert os.path.isfile(API_KEY_PATH), f"File {API_KEY_PATH} does not exist."

    with open(API_KEY_PATH, "r") as f:
        content = f.read().strip()
    assert content == SECRET, f"File {API_KEY_PATH} does not contain the correct secret."

    st = os.stat(API_KEY_PATH)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"File {API_KEY_PATH} has permissions {oct(perms)}, expected 0o400."

def test_report_file():
    assert os.path.isfile(REPORT_PATH), f"File {REPORT_PATH} does not exist."
    with open(REPORT_PATH, "r") as f:
        assert "DONE" in f.read(), f"File {REPORT_PATH} does not contain the word 'DONE'."

def test_auth_success():
    req = urllib.request.Request(BASE_URL)
    req.add_header("Authorization", SECRET)
    try:
        with urllib.request.urlopen(req) as response:
            assert response.getcode() == 200, f"Expected HTTP 200 for valid auth, got {response.getcode()}."
            body = response.read().decode("utf-8")
            assert "OK" in body, "Expected 'OK' in response body for valid auth."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected HTTP 200 for valid auth, but got HTTP {e.code}.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the server: {e.reason}. Is it running?")

def test_auth_failure():
    req = urllib.request.Request(BASE_URL)
    req.add_header("Authorization", "WRONG_SECRET_VALUE")
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected HTTP 401 for invalid auth, but request succeeded with 200 OK.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected HTTP 401 for invalid auth, got HTTP {e.code}."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the server: {e.reason}. Is it running?")

def test_header_removal():
    req = urllib.request.Request(BASE_URL)
    req.add_header("Authorization", SECRET)
    req.add_header("X-Debug-Token", "test-token-123")
    try:
        with urllib.request.urlopen(req) as response:
            headers = response.headers
            # Case-insensitive check just in case
            header_keys = [k.lower() for k in headers.keys()]
            assert "x-debug-token" not in header_keys, "X-Debug-Token header was found in the response, but it should be removed."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect or got error: {e}")

def test_log_redaction():
    # Make a request that triggers logging with the secret in the header
    req = urllib.request.Request(BASE_URL)
    req.add_header("X-Debug-Token", SECRET)
    try:
        urllib.request.urlopen(req)
    except urllib.error.URLError:
        pass # Ignore auth errors, we just need the request to hit the logging middleware

    # Give the server a moment to flush to the log file
    time.sleep(1)

    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."

    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    assert SECRET not in log_content, "The new secret was found unredacted in the log file."
    assert "[REDACTED]" in log_content, "The string '[REDACTED]' was not found in the log file where the secret should have been."