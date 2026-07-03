# test_final_state.py

import os
import hashlib
import pytest

def test_forge_c_exists():
    path = "/home/user/forge.c"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_forge_executable_exists():
    path = "/home/user/forge"
    assert os.path.exists(path), f"Executable {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"Executable {path} is not executable."

def test_audit_report_exists_and_content():
    path = "/home/user/audit_report.txt"
    assert os.path.exists(path), f"Audit report {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 3, f"Audit report should have exactly 3 lines, found {len(lines)}."

    token = lines[0]
    checksum = lines[1]
    output = lines[2]

    # Validate token format
    parts = token.split(":")
    assert len(parts) >= 3, "Forged token must have at least 3 colon-separated parts (ALG:USERNAME:ROLE)."

    alg = parts[0]
    user = parts[1]
    role = parts[2]

    assert alg.lower() == "none", f"Algorithm in token must be 'none' (case-insensitive), got '{alg}'."
    assert user == "<script>audit_bypass</script>", f"Username in token must be '<script>audit_bypass</script>', got '{user}'."
    assert role == "admin", f"Role in token must be 'admin', got '{role}'."

    # Validate checksum
    expected_checksum = hashlib.sha256(token.encode('utf-8')).hexdigest()
    assert checksum.lower() == expected_checksum, f"Checksum on line 2 is incorrect. Expected {expected_checksum}, got {checksum}."

    # Validate output
    expected_output = "AUDIT_LOG: Access Granted to admin user <script>audit_bypass</script>"
    assert output == expected_output, f"Output on line 3 is incorrect. Expected '{expected_output}', got '{output}'."