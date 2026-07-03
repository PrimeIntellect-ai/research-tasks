# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import pytest
import re

def test_secret_key_permissions():
    key_path = "/home/user/auth_daemon/secret.key"
    assert os.path.isfile(key_path), f"{key_path} does not exist."
    st = os.stat(key_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Permissions of {key_path} are not 0400 (read-only for owner). Got {oct(permissions)}."

def get_expected_token():
    key_path = "/home/user/auth_daemon/secret.key"
    assert os.path.isfile(key_path), f"{key_path} does not exist."
    with open(key_path, "rb") as f:
        key_bytes = f.read().strip()

    # XOR each byte with 0x7F and convert to hex
    hex_token = "".join(f"{b ^ 0x7F:02x}" for b in key_bytes)
    return hex_token

def test_daemon_valid_token():
    expected_token = get_expected_token()
    req = urllib.request.Request("http://127.0.0.1:9000/")
    req.add_header("Cookie", f"auth_token={expected_token}")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 for valid token, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Daemon returned HTTP {e.code} for valid token instead of 200.")
    except Exception as e:
        pytest.fail(f"Could not connect to daemon on port 9000: {e}")

def test_daemon_invalid_token():
    req = urllib.request.Request("http://127.0.0.1:9000/")
    req.add_header("Cookie", "auth_token=badtoken123456789012345678901234")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail(f"Expected HTTP 403 for invalid token, got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 for invalid token, got {e.code}"
    except Exception as e:
        pytest.fail(f"Could not connect to daemon on port 9000: {e}")

def test_daemon_buffer_overflow_fix():
    # Send a massive token to ensure it doesn't crash (testing the fix)
    massive_token = "A" * 200
    req = urllib.request.Request("http://127.0.0.1:9000/")
    req.add_header("Cookie", f"auth_token={massive_token}")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            pass # Might be 200 or 403 depending on implementation, we just care it doesn't crash
    except urllib.error.HTTPError as e:
        pass # 403 is fine
    except Exception as e:
        pytest.fail(f"Daemon crashed or failed to respond to large token (buffer overflow not fixed?): {e}")

    # Verify the daemon is still up by sending a valid request again
    test_daemon_valid_token()

def test_audit_report():
    log_path = "/home/user/audit_report.log"
    assert os.path.isfile(log_path), f"Audit report not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert re.search(r"PERMISSIONS:\s*0?400", content), "Audit report missing or incorrect PERMISSIONS (should be 400 or 0400)"
    assert re.search(r"CWE_FIXED:\s*CWE-1(20|19)", content), "Audit report missing or incorrect CWE_FIXED (should be CWE-120 or CWE-119)"
    assert re.search(r"VALID_RESPONSE:\s*200", content), "Audit report missing or incorrect VALID_RESPONSE (should be 200)"
    assert re.search(r"INVALID_RESPONSE:\s*403", content), "Audit report missing or incorrect INVALID_RESPONSE (should be 403)"
    assert re.search(r"CRASH_TEST:\s*SUCCESS", content), "Audit report missing or incorrect CRASH_TEST (should be SUCCESS)"