# test_final_state.py

import os
import re
import pytest

def test_output_txt_content():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} was not created."
    with open(path, "r") as f:
        content = f.read().strip()

    # "Hello" encoded as 16-bit LE hex:
    # H = 0x48 -> 4800
    # e = 0x65 -> 6500
    # l = 0x6c -> 6c00
    # l = 0x6c -> 6c00
    # o = 0x6f -> 6f00
    expected = "480065006c006c006f00"
    assert content.lower() == expected, f"Expected output '{expected}', but got '{content}'."

def test_valgrind_log_no_leaks():
    path = "/home/user/valgrind.log"
    assert os.path.isfile(path), f"Valgrind log file {path} was not created."

    with open(path, "r") as f:
        content = f.read()

    # Valgrind output format can vary slightly but should indicate 0 bytes definitely lost
    # We look for "definitely lost: 0 bytes in 0 blocks"
    assert "definitely lost: 0 bytes in 0 blocks" in content, (
        "Valgrind log does not indicate that 0 bytes were definitely lost. "
        "Make sure memory is freed properly."
    )