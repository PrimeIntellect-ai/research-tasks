# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_cracked_txt_content():
    """Verify that cracked.txt contains the correct plaintext password."""
    cracked_path = "/home/user/cracked.txt"
    assert os.path.isfile(cracked_path), f"File {cracked_path} does not exist."

    with open(cracked_path, "r") as f:
        content = f.read().strip()

    assert content == "7391_backup", f"Expected password '7391_backup', but found '{content}' in {cracked_path}."

def test_new_store_exists_and_permissions():
    """Verify that new_store.p12 exists and has strict 600 permissions."""
    store_path = "/home/user/new_store.p12"
    assert os.path.isfile(store_path), f"File {store_path} does not exist."

    st = os.stat(store_path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o600, f"Expected permissions 600 for {store_path}, but got {oct(mode)}."

def test_new_store_validity_and_password():
    """Verify that new_store.p12 is a valid PKCS#12 file protected with the new password."""
    store_path = "/home/user/new_store.p12"
    assert os.path.isfile(store_path), f"File {store_path} does not exist."

    # Use openssl to verify the password and structure of the new p12 file
    cmd = [
        "openssl", "pkcs12",
        "-info",
        "-in", store_path,
        "-passin", "pass:RotatedSecure123!",
        "-noout"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read {store_path} with the new password 'RotatedSecure123!'. OpenSSL error: {e.stderr}")