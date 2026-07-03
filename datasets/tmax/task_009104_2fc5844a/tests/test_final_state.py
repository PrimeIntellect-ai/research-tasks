# test_final_state.py

import os
import pytest

def test_exploit_gen_c_exists():
    """Test that the C program exploit_gen.c was created."""
    path = "/home/user/exploit_gen.c"
    assert os.path.isfile(path), f"Missing required file: {path}"

def test_payload_bin_exists():
    """Test that the generated payload.bin exists."""
    path = "/home/user/payload.bin"
    assert os.path.isfile(path), f"Missing required file: {path}"

    # The payload should be at least 25 bytes
    size = os.path.getsize(path)
    assert size >= 25, f"Payload {path} is too short (expected at least 25 bytes, got {size})"

def test_flag_txt_content():
    """Test that the flag.txt contains the correct flag."""
    path = "/home/user/flag.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{R3v3rs3_3ng1n33r1ng_M4st3r}"
    assert content == expected_flag, f"Incorrect flag in {path}. Expected '{expected_flag}', got '{content}'"