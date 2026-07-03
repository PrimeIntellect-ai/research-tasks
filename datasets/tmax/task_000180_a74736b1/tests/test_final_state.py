# test_final_state.py

import os
import stat

def test_recovered_pin_file_exists():
    """Verify that the recovered PIN file exists."""
    assert os.path.isfile('/home/user/recovered_pin.txt'), "The file /home/user/recovered_pin.txt does not exist."

def test_recovered_pin_contents():
    """Verify that the recovered PIN is correct."""
    file_path = '/home/user/recovered_pin.txt'
    assert os.path.exists(file_path), f"{file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "739184", f"The recovered PIN is incorrect. Expected '739184', got '{content}'."

def test_recovered_pin_permissions():
    """Verify that the recovered PIN file has exactly 0400 permissions."""
    file_path = '/home/user/recovered_pin.txt'
    assert os.path.exists(file_path), f"{file_path} is missing."

    st = os.stat(file_path)
    # Extract the lower 9 bits of the permission mode
    permissions = stat.S_IMODE(st.st_mode)

    assert permissions == 0o400, f"File permissions for {file_path} are incorrect. Expected 0400, got {oct(permissions)}."

def test_bruteforce_cpp_exists():
    """Verify that the C++ source code for the brute-forcer exists."""
    assert os.path.isfile('/home/user/bruteforce.cpp'), "The file /home/user/bruteforce.cpp does not exist."