# test_final_state.py

import os
import stat

def test_recovered_key_exists():
    """Verify that the recovered_key file exists in the correct location."""
    recovered_path = "/home/user/recovered_key"
    assert os.path.isfile(recovered_path), f"Verification Failed: {recovered_path} does not exist."

def test_recovered_key_content():
    """Verify that the contents of the recovered_key match the target SSH key exactly."""
    truth_path = "/home/user/.hidden_vault/admin_id_rsa"
    recovered_path = "/home/user/recovered_key"

    assert os.path.isfile(truth_path), f"Setup Error: Target key {truth_path} is missing."
    assert os.path.isfile(recovered_path), f"Verification Failed: {recovered_path} does not exist."

    with open(truth_path, 'rb') as f:
        expected_content = f.read()

    with open(recovered_path, 'rb') as f:
        actual_content = f.read()

    assert actual_content == expected_content, "Verification Failed: Contents of recovered_key do not match the target SSH key."

def test_recovered_key_permissions():
    """Verify that the recovered_key has strict SSH key permissions (0600)."""
    recovered_path = "/home/user/recovered_key"
    assert os.path.isfile(recovered_path), f"Verification Failed: {recovered_path} does not exist."

    st = os.stat(recovered_path)
    # Extract the permission bits
    perms = stat.S_IMODE(st.st_mode)

    assert perms == 0o600, f"Verification Failed: Permissions are {oct(perms).replace('0o', '')}, expected 600."