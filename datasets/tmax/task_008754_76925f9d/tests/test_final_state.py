# test_final_state.py

import os
import stat
import base64
import pytest

def test_rotation_log_contents():
    log_path = '/home/user/rotation.log'
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    expected = "admin:super_secret_password_123\ndb_user:db_pass_4567\n"
    # Allow missing trailing newline
    assert content.strip() == expected.strip(), "The contents of rotation.log do not match the expected plaintext credentials."

def test_cred_server_fixed_rs():
    fixed_path = '/home/user/cred_server_fixed.rs'
    assert os.path.isfile(fixed_path), f"The file {fixed_path} does not exist."

    with open(fixed_path, 'r') as f:
        content = f.read()

    assert 'Command::new("sh")' not in content, "The fixed Rust code still contains 'Command::new(\"sh\")'."
    assert 'Command::new("bash")' not in content, "The fixed Rust code still contains 'Command::new(\"bash\")'."

    assert 'fs::read_to_string' in content or 'File::open' in content, "The fixed Rust code must use 'fs::read_to_string' or 'File::open' for safe file reading."

def test_creds_v2_enc_exists_and_permissions():
    creds_v2_path = '/home/user/data/creds_v2.enc'
    assert os.path.isfile(creds_v2_path), f"The file {creds_v2_path} does not exist."

    st = os.stat(creds_v2_path)
    # Check if permissions are exactly 0400
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"The permissions of {creds_v2_path} are {oct(perms)}, expected 0o400."

def test_creds_v2_enc_content():
    creds_v2_path = '/home/user/data/creds_v2.enc'
    assert os.path.isfile(creds_v2_path), f"The file {creds_v2_path} does not exist."

    with open(creds_v2_path, 'rb') as f:
        encoded_data = f.read()

    try:
        encrypted_bytes = base64.b64decode(encoded_data)
    except Exception as e:
        pytest.fail(f"Failed to base64 decode {creds_v2_path}: {e}")

    key = "NEW_KEY_99887766"
    decrypted = bytearray()
    for i in range(len(encrypted_bytes)):
        decrypted.append(encrypted_bytes[i] ^ ord(key[i % len(key)]))

    expected_pt = b"admin:super_secret_password_123\ndb_user:db_pass_4567\n"
    # Allow missing trailing newline if the student wrote it without one
    assert decrypted.strip() == expected_pt.strip(), "The decrypted contents of creds_v2.enc do not match the expected plaintext."