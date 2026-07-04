# test_final_state.py
import os
import hashlib
import pytest

WORKSPACE_DIR = "/home/user/traffic_inspector"
AUTH_LOGS_PATH = os.path.join(WORKSPACE_DIR, "auth_logs.txt")
FLAGGED_IPS_PATH = os.path.join(WORKSPACE_DIR, "flagged_ips.log")
MAKEFILE_PATH = os.path.join(WORKSPACE_DIR, "Makefile")
EXECUTABLE_PATH = os.path.join(WORKSPACE_DIR, "inspector")

def get_expected_flagged_ips():
    expected_ips = []
    if not os.path.exists(AUTH_LOGS_PATH):
        return expected_ips

    with open(AUTH_LOGS_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                continue

            ip, username, token, provided_hash = parts

            computed_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()

            if computed_hash == provided_hash and "EXPLOIT_PATTERN_X99" in token:
                expected_ips.append(ip)

    return expected_ips

def test_makefile_links_openssl():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile is missing at {MAKEFILE_PATH}"
    with open(MAKEFILE_PATH, "r") as f:
        content = f.read()

    assert "-lssl" in content and "-lcrypto" in content, "Makefile does not link OpenSSL libraries (-lssl -lcrypto)."

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}. Did you run 'make'?"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable."

def test_flagged_ips_log_correctness():
    assert os.path.isfile(FLAGGED_IPS_PATH), f"Output file not found at {FLAGGED_IPS_PATH}. Did you run the compiled program?"

    expected_ips = get_expected_flagged_ips()

    with open(FLAGGED_IPS_PATH, "r") as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips, (
        f"Contents of {FLAGGED_IPS_PATH} do not match expected logic.\n"
        f"Expected: {expected_ips}\n"
        f"Actual: {actual_ips}\n"
        "Ensure you are verifying the SHA-256 hash and checking for 'EXPLOIT_PATTERN_X99' before logging the IP."
    )