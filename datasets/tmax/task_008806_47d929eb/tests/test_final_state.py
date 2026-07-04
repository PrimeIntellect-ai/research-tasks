# test_final_state.py

import os
import re

def test_cert_verify_log():
    log_path = "/home/user/cert_verify.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you save the openssl verify output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "service.pem: OK" in content, f"{log_path} does not contain 'service.pem: OK'. Certificate validation may have failed or output was not saved correctly."

def test_safe_auth_compiled():
    exe_path = "/home/user/safe_auth"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you compile the C code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_rotation_success_log():
    log_path = "/home/user/rotation_success.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The safe_auth program may not have run successfully."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Credential rotated successfully." in content, f"{log_path} does not contain the expected success message."

def test_legacy_auth_c_patched():
    c_file = "/home/user/legacy_auth.c"
    assert os.path.isfile(c_file), f"Source file {c_file} is missing."

    with open(c_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        # Ignore lines checking argc or printing usage which might legitimately use argv[0]
        if "argv[0]" in line:
            continue
        # Check if any other argv usage is present
        assert not re.search(r'argv\[\s*[1-9]\d*\s*\]', line), "The source code still accesses argv for the password, which leaks credentials."
        assert not re.search(r'argv\[\s*[a-zA-Z_]\w*\s*\]', line), "The source code still accesses argv using a variable, which may leak credentials."