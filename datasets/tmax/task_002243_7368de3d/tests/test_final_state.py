# test_final_state.py

import os
import pytest

def test_admin_cookie_file_exists():
    """Test that the admin_cookie.txt file exists."""
    assert os.path.isfile("/home/user/admin_cookie.txt"), "The file /home/user/admin_cookie.txt does not exist."

def test_bruteforce_c_file_exists():
    """Test that the bruteforce.c file exists."""
    assert os.path.isfile("/home/user/bruteforce.c"), "The file /home/user/bruteforce.c does not exist."

def test_admin_cookie_content():
    """Test that the admin_cookie.txt contains the correct forged cookie."""
    with open("/home/user/admin_cookie.txt", "r") as f:
        content = f.read().strip()

    expected_cookie = "Cookie: user=admin;sig=415309657"
    assert content == expected_cookie, f"Expected cookie '{expected_cookie}', but found '{content}'."