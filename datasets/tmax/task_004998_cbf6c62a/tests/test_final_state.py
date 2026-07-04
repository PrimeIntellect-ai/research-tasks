# test_final_state.py
import os

def test_cracker_c_exists():
    path = "/home/user/cracker.c"
    assert os.path.isfile(path), f"The file {path} is missing. You must write the C program."

def test_recovered_password():
    path = "/home/user/recovered_password.txt"
    assert os.path.isfile(path), f"The file {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "proxy", f"The recovered password in {path} is incorrect. Expected 'proxy', got '{content}'."

def test_new_credential():
    path = "/home/user/new_credential.txt"
    assert os.path.isfile(path), f"The file {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "0x78ab5a78", f"The new credential in {path} is incorrect. Expected '0x78ab5a78', got '{content}'."