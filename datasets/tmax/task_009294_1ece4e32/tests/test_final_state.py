# test_final_state.py

import os
import hashlib
import pytest

def test_cpp_source_exists():
    """Test that the C++ source file was created."""
    cpp_path = "/home/user/generate_audit.cpp"
    assert os.path.exists(cpp_path), f"C++ source file missing: {cpp_path}"
    assert os.path.isfile(cpp_path), f"Path is not a file: {cpp_path}"

def test_compiled_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/generate_audit"
    assert os.path.exists(exe_path), f"Compiled executable missing: {exe_path}"
    assert os.path.isfile(exe_path), f"Path is not a file: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

def test_audit_trail_content():
    """Test that the audit trail file contains the exactly correct verifiable log."""
    audit_path = "/home/user/audit_trail.txt"
    assert os.path.exists(audit_path), f"Audit trail file missing: {audit_path}"
    assert os.path.isfile(audit_path), f"Path is not a file: {audit_path}"

    target_url = "http://attacker.com/steal_cookie"
    expected_hash = hashlib.sha256(target_url.encode('utf-8')).hexdigest()
    expected_line = f"OPEN_REDIRECT_VERIFIED: {target_url} | SHA256: {expected_hash}"

    with open(audit_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_line, (
        f"Audit trail content does not match expected output.\n"
        f"Expected: {expected_line}\n"
        f"Found:    {content}"
    )