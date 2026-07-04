# test_final_state.py

import os
import stat
import hashlib
import pytest

def test_proof_file_exists_and_content():
    proof_path = "/home/user/proof.txt"
    assert os.path.exists(proof_path), f"File {proof_path} does not exist. The vulnerability was not verified."
    assert os.path.isfile(proof_path), f"{proof_path} is not a file."

    with open(proof_path, "r") as f:
        content = f.read().strip()

    assert content == "VULN_VERIFIED", f"Content of {proof_path} is '{content}', expected 'VULN_VERIFIED'."

def test_hash_script_and_log_exist_and_correct():
    script_path = "/home/user/hash_check.py"
    log_path = "/home/user/hash_log.txt"
    bin_path = "/home/user/suspicious_bin"

    assert os.path.exists(script_path), f"Python script {script_path} does not exist."
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.exists(bin_path), f"Suspicious binary {bin_path} is missing."

    # Calculate the expected SHA256 hash
    sha256 = hashlib.sha256()
    with open(bin_path, "rb") as f:
        sha256.update(f.read())
    expected_hash = sha256.hexdigest()

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == expected_hash, f"Hash in {log_path} is incorrect. Expected {expected_hash}, got {log_content}."

def test_ssh_directory_permissions():
    ssh_dir = "/home/user/.ssh"
    assert os.path.exists(ssh_dir), f"Directory {ssh_dir} does not exist."

    st = os.stat(ssh_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions for {ssh_dir} are {oct(perms)}, expected 0o700."

def test_authorized_keys_permissions():
    keys_file = "/home/user/.ssh/authorized_keys"
    assert os.path.exists(keys_file), f"File {keys_file} does not exist."

    st = os.stat(keys_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions for {keys_file} are {oct(perms)}, expected 0o600."