# test_final_state.py
import os

def test_c2_indicator_exists():
    """Verify that the C2 indicator file was created."""
    assert os.path.isfile("/home/user/c2_indicator.txt"), "The file /home/user/c2_indicator.txt is missing."

def test_c2_indicator_content():
    """Verify that the extracted IP address is correct."""
    assert os.path.isfile("/home/user/c2_indicator.txt"), "Cannot check content because /home/user/c2_indicator.txt is missing."
    with open("/home/user/c2_indicator.txt", "r") as f:
        content = f.read().strip()

    expected_ip = "198.51.100.42"
    assert content == expected_ip, f"The content of /home/user/c2_indicator.txt is incorrect. Expected '{expected_ip}', found '{content}'."

def test_decryptor_c_exists():
    """Verify that the decryptor C source code file exists."""
    assert os.path.isfile("/home/user/decryptor.c"), "The file /home/user/decryptor.c is missing. You must write your solution in this file."