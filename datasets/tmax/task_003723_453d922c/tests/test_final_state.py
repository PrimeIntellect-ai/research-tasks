# test_final_state.py

import os
import re
import subprocess
import tempfile

WORKSPACE_DIR = "/home/user/workspace"
AUTH_LOG_PATH = os.path.join(WORKSPACE_DIR, "auth.log")
COMPROMISED_IPS_PATH = os.path.join(WORKSPACE_DIR, "compromised_ips.txt")
SECURE_READER_C = os.path.join(WORKSPACE_DIR, "secure_reader.c")
SECURE_READER_EXE = os.path.join(WORKSPACE_DIR, "secure_reader")
SECRET_PATH = os.path.join(WORKSPACE_DIR, "new_secret.txt")
VERIFIED_SECRET_PATH = os.path.join(WORKSPACE_DIR, "verified_secret.txt")

def test_compromised_ips_content():
    assert os.path.isfile(COMPROMISED_IPS_PATH), f"File {COMPROMISED_IPS_PATH} does not exist."

    # Compute the expected IPs from the auth.log dynamically
    expected_ips = set()
    if os.path.isfile(AUTH_LOG_PATH):
        with open(AUTH_LOG_PATH, 'r') as f:
            for line in f:
                if "password=hunter2" in line:
                    match = re.search(r"src_ip=([0-9\.]+)", line)
                    if match:
                        expected_ips.add(match.group(1))

    expected_ips_sorted = sorted(list(expected_ips))

    with open(COMPROMISED_IPS_PATH, 'r') as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips_sorted, f"Expected IPs {expected_ips_sorted}, but got {actual_ips} in {COMPROMISED_IPS_PATH}"

def test_verified_secret_content():
    assert os.path.isfile(VERIFIED_SECRET_PATH), f"File {VERIFIED_SECRET_PATH} does not exist."
    assert os.path.isfile(SECRET_PATH), f"Original secret file {SECRET_PATH} does not exist."

    with open(SECRET_PATH, 'r') as f:
        expected_secret = f.read()

    with open(VERIFIED_SECRET_PATH, 'r') as f:
        actual_secret = f.read()

    assert actual_secret == expected_secret, f"Content of {VERIFIED_SECRET_PATH} does not match {SECRET_PATH}"

def test_secure_reader_c_source():
    assert os.path.isfile(SECURE_READER_C), f"Source file {SECURE_READER_C} does not exist."
    with open(SECURE_READER_C, 'r') as f:
        source_code = f.read()

    assert "PR_SET_SECCOMP" in source_code, f"PR_SET_SECCOMP not found in {SECURE_READER_C}"
    assert "SECCOMP_MODE_STRICT" in source_code, f"SECCOMP_MODE_STRICT not found in {SECURE_READER_C}"

def test_secure_reader_executable_exists():
    assert os.path.isfile(SECURE_READER_EXE), f"Executable {SECURE_READER_EXE} does not exist."
    assert os.access(SECURE_READER_EXE, os.X_OK), f"File {SECURE_READER_EXE} is not executable."

def test_secure_reader_rejects_bad_hash():
    assert os.path.isfile(SECURE_READER_EXE), f"Executable {SECURE_READER_EXE} does not exist."

    # Create a temporary file with a different content (and thus different hash)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("BadSecret123")
        tmp_path = tmp.name

    try:
        result = subprocess.run([SECURE_READER_EXE, tmp_path], capture_output=True)
        assert result.returncode == 1, f"Expected exit code 1 for bad hash, but got {result.returncode}"
    finally:
        os.remove(tmp_path)