# test_final_state.py

import os
import stat
import subprocess
import urllib.request
import urllib.error
import pytest

def test_file_permissions():
    leaf_cert = "/app/keys/leaf_cert.pem"
    root_ca = "/app/keys/root_ca.pem"

    assert os.path.exists(leaf_cert), f"{leaf_cert} is missing."
    assert os.path.exists(root_ca), f"{root_ca} is missing."

    leaf_mode = stat.S_IMODE(os.stat(leaf_cert).st_mode)
    root_mode = stat.S_IMODE(os.stat(root_ca).st_mode)

    assert leaf_mode == 0o400, f"Expected 0400 permissions for {leaf_cert}, got {oct(leaf_mode)}"
    assert root_mode == 0o400, f"Expected 0400 permissions for {root_ca}, got {oct(root_mode)}"

def test_validator_adversarial_corpus():
    validator_path = "/app/validator"
    assert os.path.isfile(validator_path), f"Validator binary {validator_path} is missing."
    assert os.access(validator_path, os.X_OK), f"Validator binary {validator_path} is not executable."

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run([validator_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run([validator_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_end_to_end_flow():
    # Ensure services are running
    subprocess.run(["bash", "/app/start_services.sh"], check=False)

    try:
        req_auth = urllib.request.Request("http://127.0.0.1:8080/auth")
        with urllib.request.urlopen(req_auth, timeout=5) as response:
            token = response.read().decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to fetch token from /auth endpoint: {e}")

    assert token, "Received empty token from /auth"

    try:
        req_api = urllib.request.Request("http://127.0.0.1:8080/api/data")
        req_api.add_header("Token", token)
        with urllib.request.urlopen(req_api, timeout=5) as response:
            data = response.read().decode('utf-8').strip()
            status = response.getcode()
    except urllib.error.HTTPError as e:
        pytest.fail(f"API request failed with HTTP {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to fetch data from /api/data endpoint: {e}")

    assert status == 200, f"Expected HTTP 200, got {status}"
    assert data == "SECURE_DATA_ACCESSED", f"Expected 'SECURE_DATA_ACCESSED', got '{data}'"