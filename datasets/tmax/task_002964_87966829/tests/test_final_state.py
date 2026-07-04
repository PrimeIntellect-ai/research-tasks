# test_final_state.py

import os
import pytest

def test_result_txt_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you save the IP address?"

    with open(result_path, "r") as f:
        content = f.read()

    assert content == "203.0.113.85", f"Content of {result_path} is incorrect. Expected exactly '203.0.113.85', but got '{content}'."

def test_decoded_dat_content():
    decoded_path = "/home/user/decoded.dat"
    assert os.path.isfile(decoded_path), f"File {decoded_path} is missing. Did you run the fixed Go script?"

    expected_text = "Suspicious dropper connecting to C2 at 203.0.113.85. Initiate sequence."
    with open(decoded_path, "r") as f:
        content = f.read().strip()

    assert content == expected_text, f"Content of {decoded_path} does not match the expected decrypted text. The Go script might still be assembling chunks out of order."