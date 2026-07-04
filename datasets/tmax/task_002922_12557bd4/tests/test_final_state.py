# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_decrypted_id_rsa_exists_and_permissions():
    path = "/home/user/decrypted_id_rsa"
    assert os.path.isfile(path), f"Decrypted SSH key not found at {path}"

    st = os.stat(path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Expected permissions 0600 for {path}, but got {oct(permissions)}"

def test_decrypted_id_rsa_is_valid():
    path = "/home/user/decrypted_id_rsa"
    with open(path, 'r') as f:
        content = f.read()

    assert "BEGIN RSA PRIVATE KEY" in content or "BEGIN OPENSSH PRIVATE KEY" in content, \
        f"File {path} does not appear to be a valid private key."
    assert "ENCRYPTED" not in content, \
        f"File {path} appears to still be encrypted."

def test_sanitizer_binary_exists():
    path = "/home/user/sanitizer"
    assert os.path.isfile(path), f"Sanitizer binary not found at {path}"
    assert os.access(path, os.X_OK), f"Sanitizer binary at {path} is not executable"

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus"
    assert len(clean_files) > 0, "No files found in clean corpus"

    bypassed_evil = []
    for evil_file in evil_files:
        with open(evil_file, 'r') as f:
            result = subprocess.run([sanitizer_path], stdin=f, capture_output=True)
            if result.returncode != 1:
                bypassed_evil.append(os.path.basename(evil_file))

    modified_clean = []
    for clean_file in clean_files:
        with open(clean_file, 'r') as f:
            result = subprocess.run([sanitizer_path], stdin=f, capture_output=True)
            if result.returncode != 0:
                modified_clean.append(os.path.basename(clean_file))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil[:5])}{'...' if len(bypassed_evil) > 5 else ''}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(modified_clean[:5])}{'...' if len(modified_clean) > 5 else ''}")

    assert not bypassed_evil and not modified_clean, " | ".join(error_msgs)