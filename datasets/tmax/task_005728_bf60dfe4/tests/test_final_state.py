# test_final_state.py

import os
import pytest

def test_organizer_script_exists_and_executable():
    """Test that the organizer.sh script exists and is executable."""
    script_path = "/home/user/organizer.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_valid_route_organized_correctly():
    """Test that libauth.so is correctly organized."""
    lib_path = "/home/user/organized_routes/api/v1/auth/libauth.so"
    status_path = "/home/user/organized_routes/api/v1/auth/status.txt"

    assert os.path.isfile(lib_path), f"Expected valid library at {lib_path} but it was not found."
    assert os.path.isfile(status_path), f"Expected status file at {status_path} but it was not found."

    with open(status_path, "r") as f:
        content = f.read().strip()
    assert content == "VALID", f"Expected status.txt to contain 'VALID', but got '{content}'."

def test_invalid_abi_route_skipped():
    """Test that libdata.so (invalid ABI) is skipped."""
    dir_path = "/home/user/organized_routes/api/v1/data"
    assert not os.path.exists(dir_path), f"Directory {dir_path} should not exist because libdata.so has an invalid ABI."

def test_invalid_checksum_route_skipped():
    """Test that libuser.so (invalid checksum) is skipped."""
    dir_path = "/home/user/organized_routes/api/v2/user"
    assert not os.path.exists(dir_path), f"Directory {dir_path} should not exist because libuser.so has an invalid checksum."

def test_missing_file_route_skipped():
    """Test that libmiss.so (missing file) is skipped."""
    dir_path = "/home/user/organized_routes/api/v2/settings"
    assert not os.path.exists(dir_path), f"Directory {dir_path} should not exist because libmiss.so is missing."