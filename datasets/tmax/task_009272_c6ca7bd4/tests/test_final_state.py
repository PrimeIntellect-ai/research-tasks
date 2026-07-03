# test_final_state.py

import os
import subprocess
import pytest

def test_admin_token_file():
    token_file = "/home/user/admin_token.txt"
    assert os.path.exists(token_file), f"{token_file} does not exist."
    assert os.path.isfile(token_file), f"{token_file} is not a file."

    with open(token_file, "r") as f:
        content = f.read()

    assert content.strip() == "84", f"The token in {token_file} is incorrect. Expected '84', got '{content}'."

def test_forge_c_exists():
    source_file = "/home/user/forge.c"
    assert os.path.exists(source_file), f"{source_file} does not exist."
    assert os.path.isfile(source_file), f"{source_file} is not a file."

def test_forge_executable_exists():
    binary_path = "/home/user/forge"
    assert os.path.exists(binary_path), f"{binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_forge_executable_output():
    binary_path = "/home/user/forge"

    # Test for 'admin'
    result_admin = subprocess.run([binary_path, "admin"], capture_output=True, text=True)
    assert result_admin.returncode == 0, f"Running {binary_path} admin failed."
    assert result_admin.stdout.strip() == "84", f"Expected output '84' for admin, got '{result_admin.stdout.strip()}'."

    # Test for 'guest'
    result_guest = subprocess.run([binary_path, "guest"], capture_output=True, text=True)
    assert result_guest.returncode == 0, f"Running {binary_path} guest failed."
    assert result_guest.stdout.strip() == "161", f"Expected output '161' for guest, got '{result_guest.stdout.strip()}'."