# test_final_state.py

import os
import pytest

def test_decoder_c_exists():
    path = "/home/user/decoder.c"
    assert os.path.exists(path), f"File {path} does not exist. You must write your C program to this location."
    assert os.path.isfile(path), f"{path} is not a file."

def test_decoder_binary_exists():
    path = "/home/user/decoder"
    assert os.path.exists(path), f"Executable {path} does not exist. You must compile your C program to this location."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_secret_txt_content():
    path = "/home/user/secret.txt"
    assert os.path.exists(path), f"File {path} does not exist. You must redirect the output of your decoder to this file."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "EXFILTRATION_COMPLETE"
    assert content == expected, f"Content of {path} is incorrect. Expected '{expected}', got '{content}'."