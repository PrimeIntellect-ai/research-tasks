# test_final_state.py
import os
import stat

def test_cert_cn_extracted():
    """Validates that the correct Common Name was extracted from the certificate."""
    cn_file = "/home/user/cert_cn.txt"
    assert os.path.isfile(cn_file), f"The file {cn_file} does not exist."

    with open(cn_file, "r") as f:
        content = f.read().strip()

    expected_cn = "admin-sec-ops"
    assert content == expected_cn, f"Expected CN '{expected_cn}', but found '{content}'."

def test_ssh_key_permissions_and_content():
    """Validates that the SSH key was extracted and secured with appropriate permissions."""
    key_file = "/home/user/extracted_id_rsa"
    assert os.path.isfile(key_file), f"The file {key_file} does not exist."

    # Verify file permissions are strictly 0600 (read/write for owner only)
    file_stat = os.stat(key_file)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o600, f"Expected file permissions to be 0600, but found {oct(permissions)}."

    # Verify the file contains a private key structure
    with open(key_file, "r") as f:
        content = f.read()

    assert "PRIVATE KEY" in content, f"The file {key_file} does not appear to contain a private key."