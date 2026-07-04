# test_final_state.py

import os
import subprocess
import pytest

def get_expected_key() -> str:
    """Decrypt the key using openssl to get the expected content."""
    enc_file = '/home/user/new_key.pub.enc'
    if not os.path.exists(enc_file):
        pytest.fail(f"Encrypted key file {enc_file} is missing.")

    result = subprocess.run(
        ['openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2', '-in', enc_file, '-pass', 'pass:SecureRotate2024!'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        pytest.fail("Failed to decrypt the key using openssl internally for test verification.")
    return result.stdout

def test_decrypted_key_exists_and_correct():
    """Verify that the decrypted key file exists and has correct content."""
    dec_file = '/home/user/new_key.pub'
    assert os.path.isfile(dec_file), f"Decrypted key file {dec_file} is missing. Did you decrypt it?"

    expected_content = get_expected_key()
    with open(dec_file, 'r') as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The content of the decrypted key file does not match the expected decrypted content."

def test_cpp_client_fixed():
    """Verify that the C++ client has been modified correctly."""
    cpp_file = '/home/user/upload_client.cpp'
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

    with open(cpp_file, 'r') as f:
        content = f.read()

    assert "../../../home/user/.ssh/authorized_keys" not in content, "The path traversal vulnerability is still present in the C++ code."
    assert "file=authorized_keys" in content, "The file parameter in the HTTP URI should be strictly 'authorized_keys'."
    assert "Cookie: auth=admin_rotate" in content, "The required 'Cookie: auth=admin_rotate' header is missing from the HTTP request."

def test_client_compiled():
    """Verify that the client was compiled."""
    bin_file = '/home/user/upload_client'
    assert os.path.isfile(bin_file), f"Compiled client binary {bin_file} is missing. Did you compile the code?"
    assert os.access(bin_file, os.X_OK), f"The file {bin_file} is not executable."

def test_server_upload_successful():
    """Verify that the key was successfully uploaded to the server."""
    uploaded_file = '/home/user/server_uploads/authorized_keys'
    assert os.path.isfile(uploaded_file), f"The uploaded file {uploaded_file} is missing. The client may not have successfully uploaded the key."

    expected_content = get_expected_key()
    with open(uploaded_file, 'r') as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The content of the uploaded key on the server does not match the expected decrypted key."