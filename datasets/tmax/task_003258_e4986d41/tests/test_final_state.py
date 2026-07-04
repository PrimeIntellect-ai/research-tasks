# test_final_state.py

import os
import hashlib
import stat
import pytest

def test_ci_sign_script_exists():
    """Verify that the ci_sign.sh script is present."""
    file_path = "/home/user/ci_sign.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing. You need to create the Bash script."

def test_websocat_binary_exists_and_executable():
    """Verify that websocat is downloaded and executable."""
    file_path = "/home/user/websocat"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you download websocat?"

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {file_path} is not executable. You need to run chmod +x on it."

def test_signature_file_content():
    """Verify that the signature.txt file contains the correct signature."""
    file_path = "/home/user/signature.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you save the output?"

    artifact_name = "mobile-release-v2.1.apk"
    expected_checksum = hashlib.sha256(artifact_name.encode('utf-8')).hexdigest()
    expected_signature = f"SIG-{expected_checksum}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_signature, f"The content of {file_path} is incorrect. Expected '{expected_signature}', but got '{content}'."