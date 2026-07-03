# test_final_state.py

import os
import pytest

def test_data_bin_exists_and_size():
    path = "/home/user/data.bin"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the Go generator?"

    # Calculate expected size:
    # 10 events (0-9): 1 byte len + 7 bytes string = 8 bytes each -> 80 bytes
    # 40 events (10-49): 1 byte len + 8 bytes string = 9 bytes each -> 360 bytes
    # Total = 440 bytes
    expected_size = 440
    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, f"Expected {path} to be {expected_size} bytes, got {actual_size} bytes."

def test_parser_executable_exists():
    path = "/home/user/parser"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the C++ parser?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_decoded_log_content():
    path = "/home/user/decoded.log"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the parser and redirect output?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected exactly 50 lines in {path}, got {len(lines)}."

    expected_lines = sorted([f"Parsed: Event-{i}" for i in range(50)])

    assert lines == expected_lines, f"The contents of {path} do not match the expected sorted output."