# test_final_state.py

import os
import stat
import base64
import hashlib
import subprocess
import pytest

def test_exploit_job_exists_and_format():
    job_path = "/home/user/incoming_uploads/exploit.job"
    assert os.path.isfile(job_path), f"Exploit job file {job_path} does not exist."

    with open(job_path, "r") as f:
        content = f.read().strip()

    assert ":" in content, "Exploit job file does not contain the required ':' separator."
    filename, encoded_data = content.split(":", 1)

    assert "../" in filename, "Exploit job file does not appear to contain a path traversal payload."

    try:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to decode base64 data in exploit job: {e}")

    assert "ROTATED_SECRET_999" in decoded_data, "Decoded data does not contain the expected secret."

def test_master_token_overwritten():
    token_path = "/home/user/auth_keys/master_token.txt"
    assert os.path.isfile(token_path), f"Token file {token_path} does not exist."

    with open(token_path, "r") as f:
        content = f.read()

    assert content == "ROTATED_SECRET_999\n", f"Token file content is incorrect: {repr(content)}"

def test_secure_script_exists_and_executable():
    script_path = "/home/user/cred_rotator_secure.sh"
    assert os.path.isfile(script_path), f"Secure script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Secure script {script_path} is not executable."

def test_secure_script_sanitizes_filename(tmp_path):
    script_path = "/home/user/cred_rotator_secure.sh"
    upload_dir = "/home/user/incoming_uploads"
    certs_dir = "/home/user/certs"
    auth_keys_dir = "/home/user/auth_keys"

    # Clean up existing jobs to prevent interference
    for f in os.listdir(upload_dir):
        if f.endswith(".job"):
            os.remove(os.path.join(upload_dir, f))

    test_job_path = os.path.join(upload_dir, "test_escape.job")
    payload = base64.b64encode(b"test_content\n").decode('utf-8')

    with open(test_job_path, "w") as f:
        f.write(f"../../auth_keys/test_escape.txt:{payload}\n")

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Secure script execution failed: {result.stderr}"

    escaped_file = os.path.join(auth_keys_dir, "test_escape.txt")
    assert not os.path.exists(escaped_file), "Vulnerability still exists: file escaped to auth_keys directory."

    # Check if sanitized file exists in certs dir
    sanitized_filename = "auth_keystest_escapetxt"
    expected_cert_path = os.path.join(certs_dir, sanitized_filename)

    found = False
    for f in os.listdir(certs_dir):
        if "test_escape" in f:
            found = True
            break

    assert found, "Sanitized file was not found in the certs directory."

    # Clean up
    os.remove(test_job_path)

def test_token_checksum():
    checksum_path = "/home/user/token_checksum.txt"
    token_path = "/home/user/auth_keys/master_token.txt"

    assert os.path.isfile(checksum_path), f"Checksum file {checksum_path} does not exist."

    with open(token_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(checksum_path, "r") as f:
        checksum_content = f.read().strip()

    expected_format = f"{actual_hash}  {token_path}"
    assert checksum_content == expected_format, f"Checksum file content is incorrect. Expected: '{expected_format}', Got: '{checksum_content}'"