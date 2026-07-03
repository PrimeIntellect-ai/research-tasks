# test_final_state.py
import os
import hashlib
import re

def test_authorized_keys_hardened():
    path = '/home/user/.ssh/authorized_keys'
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        assert not line.startswith('ssh-rsa'), "ssh-rsa key found in authorized_keys"

    assert len(lines) == 2, f"Expected exactly 2 keys in authorized_keys, found {len(lines)}"

def test_upload_server_cpp_fixed():
    path = '/home/user/upload_server.cpp'
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, 'r') as f:
        content = f.read()

    assert 'void save_uploaded_file(std::string filename)' in content, "Function signature changed or missing"
    assert '..' in content, "Missing check for '..'"
    assert '/' in content or "'/'" in content or '"/"' in content, "Missing check for '/'"

def test_security_report():
    report_path = '/home/user/security_report.txt'
    cpp_path = '/home/user/upload_server.cpp'

    assert os.path.isfile(report_path), f"{report_path} is missing"
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing"

    with open(cpp_path, 'rb') as f:
        cpp_hash = hashlib.sha256(f.read()).hexdigest()

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 3, f"Expected exactly 3 lines in security_report.txt, found {len(lines)}"

    mangled_name = lines[0]
    assert 'save_uploaded_file' in mangled_name and mangled_name.startswith('_Z'), f"Line 1 does not look like a mangled symbol for save_uploaded_file: {mangled_name}"

    assert lines[1] == cpp_hash, f"Line 2 (SHA256) is incorrect. Expected {cpp_hash}, got {lines[1]}"

    assert lines[2] == '2', f"Line 3 (key count) is incorrect. Expected '2', got {lines[2]}"