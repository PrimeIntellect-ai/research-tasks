# test_final_state.py

import os
import stat
import subprocess
import hashlib
import pytest

def test_audit_hash():
    hash_file = "/home/user/audit_hash.txt"
    assert os.path.isfile(hash_file), f"{hash_file} does not exist."

    with open(hash_file, "r") as f:
        content = f.read().strip()

    assert len(content) == 64, f"The content of {hash_file} does not look like a valid SHA256 hash."
    assert all(c in "0123456789abcdefABCDEF" for c in content), f"The content of {hash_file} contains non-hexadecimal characters."

def test_poc_script():
    poc_script = "/home/user/poc.sh"
    target_file = "/home/user/target.txt"

    assert os.path.isfile(poc_script), f"{poc_script} does not exist."

    # Ensure target file does not exist or remove it
    if os.path.exists(target_file):
        os.remove(target_file)

    # Run the PoC script
    result = subprocess.run(["bash", poc_script], capture_output=True, text=True)

    assert os.path.isfile(target_file), f"PoC script did not create {target_file}."

    with open(target_file, "r") as f:
        content = f.read().strip()

    assert content == "EXPLOIT_SUCCESS", f"Target file contains '{content}' instead of 'EXPLOIT_SUCCESS'."

def test_uploads_permissions():
    uploads_dir = "/home/user/uploader/uploads"
    assert os.path.isdir(uploads_dir), f"{uploads_dir} does not exist."

    st = os.stat(uploads_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions of {uploads_dir} are {oct(perms)}, expected 0o700."

def test_uploader_fixed_binary():
    fixed_binary = "/home/user/uploader_fixed"
    assert os.path.isfile(fixed_binary), f"{fixed_binary} does not exist."
    assert os.access(fixed_binary, os.X_OK), f"{fixed_binary} is not executable."

    # Test 1: path traversal with slash
    res1 = subprocess.run([fixed_binary, "../test.txt", "dGVzdA=="], capture_output=True, text=True)
    assert res1.returncode == 1, f"Expected exit code 1 when filename contains '/', got {res1.returncode}."
    assert "Access Denied" in res1.stdout, "Expected 'Access Denied' in stdout when filename contains '/'."

    # Test 2: filename with dot
    res2 = subprocess.run([fixed_binary, "test.txt", "dGVzdA=="], capture_output=True, text=True)
    assert res2.returncode == 1, f"Expected exit code 1 when filename contains '.', got {res2.returncode}."
    assert "Access Denied" in res2.stdout, "Expected 'Access Denied' in stdout when filename contains '.'."

    # Test 3: valid filename
    test_file = "/home/user/uploader/uploads/test"
    if os.path.exists(test_file):
        os.remove(test_file)

    res3 = subprocess.run([fixed_binary, "test", "dGVzdA=="], capture_output=True, text=True)
    assert res3.returncode == 0, f"Expected exit code 0 for valid filename, got {res3.returncode}."

    assert os.path.isfile(test_file), f"Expected {test_file} to be created for valid filename."
    with open(test_file, "r") as f:
        content = f.read().strip()
    assert content == "test", f"Expected decoded payload 'test' in {test_file}, got '{content}'."