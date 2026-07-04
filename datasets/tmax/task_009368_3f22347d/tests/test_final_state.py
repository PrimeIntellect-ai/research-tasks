# test_final_state.py

import os
import urllib.request
import json
import subprocess
import time

def test_files_exist():
    """Ensure all required files have been created."""
    expected_files = [
        "/home/user/workspace/src/mergediff.c",
        "/home/user/workspace/libmergediff.so",
        "/home/user/workspace/server.py",
        "/home/user/workspace/nginx.conf",
        "/home/user/workspace/status.log"
    ]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected file {filepath} is missing."

def test_status_ready():
    """Ensure status.log contains READY."""
    with open("/home/user/workspace/status.log", "r") as f:
        content = f.read()
    assert "READY" in content, "status.log does not contain 'READY'."

def test_api_endpoint_via_nginx():
    """Test the /diff endpoint via Nginx reverse proxy on port 8080."""
    payload = {
        "a": [1, 2, 4, 8, 16],
        "b": [2, 4, 10, 20]
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:8080/diff",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            resp_json = json.loads(resp_body)
    except Exception as e:
        assert False, f"Failed to communicate with the API via Nginx on port 8080: {e}"

    expected = {
        "only_a": [1, 8, 16],
        "only_b": [10, 20],
        "both": [2, 4]
    }

    assert resp_json.get("only_a") == expected["only_a"], f"Incorrect only_a. Expected {expected['only_a']}, got {resp_json.get('only_a')}"
    assert resp_json.get("only_b") == expected["only_b"], f"Incorrect only_b. Expected {expected['only_b']}, got {resp_json.get('only_b')}"
    assert resp_json.get("both") == expected["both"], f"Incorrect both. Expected {expected['both']}, got {resp_json.get('both')}"

def test_minimal_build():
    """Check that the shared library doesn't use standard IO/stdlib functions if MINIMAL_BUILD is defined."""
    # We check the undefined symbols in the shared library.
    try:
        output = subprocess.check_output(["nm", "-u", "/home/user/workspace/libmergediff.so"], stderr=subprocess.STDOUT).decode('utf-8')
        forbidden_symbols = ["printf", "malloc", "free", "puts"]
        for sym in forbidden_symbols:
            assert sym not in output, f"Shared library contains forbidden symbol '{sym}' despite MINIMAL_BUILD requirement."
    except FileNotFoundError:
        # nm might not be installed, skip this strict check if so
        pass
    except subprocess.CalledProcessError:
        # nm failed, maybe the file is not a valid ELF
        assert False, "Failed to run nm on /home/user/workspace/libmergediff.so. Is it a valid shared library?"