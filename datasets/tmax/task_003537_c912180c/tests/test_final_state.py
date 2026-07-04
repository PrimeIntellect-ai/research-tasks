# test_final_state.py

import os
import requests
import time
import pytest

def test_executable_exists():
    """Verify that the agent compiled the server to the expected location."""
    assert os.path.isfile("/home/user/diag_server"), "The compiled executable /home/user/diag_server is missing."

def test_server_running_and_responds():
    """Verify that the server is running on port 9090 and handles the requests without crashing."""
    # Give the server a moment if it was just started
    time.sleep(1)

    base_url = "http://127.0.0.1:9090"

    # 1. Test POST /auth with the correct PIN
    try:
        r_auth = requests.post(f"{base_url}/auth", data="8294", timeout=3)
        assert r_auth.status_code == 200, f"Expected HTTP 200 for correct PIN, got {r_auth.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on port 9090 for /auth: {e}")

    # 2. Test GET /diagnostics to ensure the crash is fixed
    try:
        r_diag = requests.get(f"{base_url}/diagnostics", timeout=3)
        assert r_diag.status_code == 200, f"Expected HTTP 200 for diagnostics after auth, got {r_diag.status_code}"

        # Check if the response contains the diagnostic text (or parts of it)
        # The original text was "Diagnostic data: CPU=45%, Mem=2GB, Status=Warning - Disk Almost Full"
        assert "Diagnostic" in r_diag.text or "CPU" in r_diag.text, \
            "Response did not contain expected diagnostic data. Check if the fix altered the output."

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to retrieve diagnostics (server might have crashed due to unfixed buffer overflow): {e}")