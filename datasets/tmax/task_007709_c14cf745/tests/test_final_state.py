# test_final_state.py
import os
import subprocess
import pytest

def test_cwe_flaw_txt():
    path = "/home/user/cwe_flaw.txt"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip().upper()

    allowed_cwes = ["CWE-327", "CWE-345", "CWE-347"]
    found = any(cwe in content for cwe in allowed_cwes)
    assert found, f"File {path} does not contain an acceptable CWE ID (e.g., CWE-327, CWE-345, or CWE-347)."

def test_forge_c_exists():
    path = "/home/user/forge.c"
    assert os.path.exists(path), f"File {path} is missing. You must write your payload generator in C."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_payload_bin_exists_and_size():
    path = "/home/user/payload.bin"
    assert os.path.exists(path), f"File {path} is missing. You must generate the forged ticket."
    assert os.path.isfile(path), f"Path {path} is not a file."

    size = os.path.getsize(path)
    assert size == 36, f"File {path} is {size} bytes, but expected exactly 36 bytes."

def test_vuln_auth_bypass():
    binary_path = "/home/user/vuln_auth"
    payload_path = "/home/user/payload.bin"

    assert os.path.exists(binary_path), f"Binary {binary_path} is missing."
    assert os.path.exists(payload_path), f"Payload {payload_path} is missing."

    result = subprocess.run([binary_path, payload_path], capture_output=True, text=True)

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}. Output: {result.stdout}"
    assert "Access Granted: admin" in result.stdout, f"Expected 'Access Granted: admin' in output, got: {result.stdout}"

def test_payload_contents():
    path = "/home/user/payload.bin"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "rb") as f:
        data = f.read()

    assert len(data) == 36, "Payload size is incorrect."

    username_bytes = data[0:16]
    role_bytes = data[16:32]

    # Extract string up to first null byte
    username = username_bytes.split(b'\0')[0].decode('ascii', errors='ignore')
    role = role_bytes.split(b'\0')[0].decode('ascii', errors='ignore')

    assert username == "attacker", f"Expected username 'attacker', got '{username}'"
    assert role == "admin", f"Expected role 'admin', got '{role}'"