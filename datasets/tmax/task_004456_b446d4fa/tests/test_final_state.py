# test_final_state.py

import os
import pytest

def test_decrypt_cpp_exists():
    path = "/home/user/decrypt.cpp"
    assert os.path.isfile(path), f"Missing file: {path}. The task requires writing a C++ decrypter."

def test_admin_pass_correct():
    path = "/home/user/admin_pass.txt"
    assert os.path.isfile(path), f"Missing file: {path}. The task requires saving the recovered password to this file."

    with open(path, "r") as f:
        content = f.read()

    expected_password = "Pwn3d_Pr0c_M3m0ry!"
    assert content == expected_password, f"The content of {path} is incorrect. Expected '{expected_password}', but got '{content}'."