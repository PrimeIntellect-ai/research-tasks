# test_final_state.py

import os
import pytest

def test_libdecoder_so_exists():
    path = "/home/user/libdecoder.so"
    assert os.path.isfile(path), f"Shared library not found: {path}. Did you compile the C code?"

def test_results_txt_content():
    path = "/home/user/results.txt"
    assert os.path.isfile(path), f"Results file not found: {path}. Did you run the Python script?"

    expected_lines = [
        "Hello World",
        "This is a very long string that will overflow the thirty two byte buffer",
        "Secret Data!"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.txt, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_decoder_c_fixed():
    path = "/home/user/decoder.c"
    assert os.path.isfile(path), f"Source file not found: {path}"

    with open(path, "r") as f:
        content = f.read()

    # Check that the fixed size buffer is removed or modified
    assert "char buffer[32];" not in content, "The C code still contains the buggy fixed-size buffer 'char buffer[32];'."