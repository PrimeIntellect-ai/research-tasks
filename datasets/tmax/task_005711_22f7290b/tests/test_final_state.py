# test_final_state.py

import os
import stat

def test_access_key_file_exists():
    """Test that the access_key.txt file exists."""
    file_path = "/home/user/access_key.txt"
    assert os.path.exists(file_path), f"Error: The file {file_path} is missing."
    assert os.path.isfile(file_path), f"Error: {file_path} is not a regular file."

def test_access_key_content():
    """Test that the access_key.txt file contains the correct flag."""
    file_path = "/home/user/access_key.txt"
    assert os.path.exists(file_path), f"Error: The file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{jwt_alg_none_bypass_success_8831}"
    assert content == expected_flag, f"Error: The content of {file_path} is incorrect. Expected '{expected_flag}', got '{content}'."

def test_access_key_permissions():
    """Test that the access_key.txt file has exactly 0400 permissions."""
    file_path = "/home/user/access_key.txt"
    assert os.path.exists(file_path), f"Error: The file {file_path} is missing."

    file_stat = os.stat(file_path)
    permissions = stat.S_IMODE(file_stat.st_mode)

    expected_permissions = 0o400
    assert permissions == expected_permissions, f"Error: The permissions of {file_path} are incorrect. Expected 0o400, got {oct(permissions)}."