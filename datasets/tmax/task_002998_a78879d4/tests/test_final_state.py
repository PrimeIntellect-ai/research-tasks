# test_final_state.py

import os
import stat
import ctypes
import subprocess
import hashlib
import pytest

def test_ssh_authorized_keys_cleaned():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"File not found: {auth_keys_path}"

    with open(auth_keys_path, "r") as f:
        content = f.read()

    assert "evil@hacker.com" not in content, "The attacker's SSH key (evil@hacker.com) was not removed."
    assert "good@user.com" in content, "A legitimate SSH key (good@user.com) was incorrectly removed."
    assert "admin@company.com" in content, "A legitimate SSH key (admin@company.com) was incorrectly removed."

def test_admin_token_forged():
    token_path = "/home/user/admin_token.txt"
    assert os.path.isfile(token_path), f"File not found: {token_path}"

    # Compute the expected token using glibc's rand()
    try:
        libc = ctypes.CDLL("libc.so.6")
    except OSError:
        pytest.fail("Could not load libc.so.6 to verify the token.")

    libc.srand(1700000000)
    secret = libc.rand()
    xor_byte = secret % 256

    expected_token = "".join(f"{ord(c) ^ xor_byte:02x}" for c in "admin")

    with open(token_path, "r") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_token, f"The forged token in {token_path} is incorrect."

def test_auth_daemon_fixed():
    binary_path = "/home/user/auth_daemon_fixed"
    source_path = "/home/user/auth_daemon.cpp"

    assert os.path.isfile(binary_path), f"Compiled binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"File is not executable: {binary_path}"

    # Verify the source code uses SHA256
    with open(source_path, "r") as f:
        source_code = f.read()

    assert "SHA256" in source_code or "EVP_sha256" in source_code, "The fixed source code does not appear to use SHA256."
    assert "SecureSecretKey" in source_code, "The fixed source code does not contain the required salt/key 'SecureSecretKey'."

    # Run the binary. Assuming main() was untouched, it should output the hash for "guest".
    # If main() was changed to print for "admin", we can check for either.
    try:
        result = subprocess.run([binary_path], capture_output=True, text=True, timeout=2)
        output = result.stdout.strip()
    except Exception as e:
        pytest.fail(f"Failed to execute {binary_path}: {e}")

    expected_guest_hash = hashlib.sha256(b"guestSecureSecretKey").hexdigest()
    expected_admin_hash = hashlib.sha256(b"adminSecureSecretKey").hexdigest()

    assert output in (expected_guest_hash, expected_admin_hash), (
        f"The binary output '{output}' does not match the expected SHA-256 hash for 'guest' or 'admin' concatenated with 'SecureSecretKey'."
    )