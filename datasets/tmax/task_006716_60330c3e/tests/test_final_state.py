# test_final_state.py

import os
import pytest

def test_strace_log_exists_and_valid():
    path = "/home/user/strace.log"
    assert os.path.isfile(path), f"File {path} does not exist. You must run strace to trace read and write syscalls."

    with open(path, "r") as f:
        content = f.read()

    assert "read(" in content, f"Expected to find 'read(' syscalls in {path}."
    assert "write(" in content, f"Expected to find 'write(' syscalls in {path}."

def test_fixed_output_csv():
    path = "/home/user/batch_data_fixed.csv"
    assert os.path.isfile(path), f"File {path} does not exist. You must generate the fixed output."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 100, f"Expected {path} to have exactly 100 lines, but found {len(lines)}."

    last_line = lines[-1]
    expected_last_line = "TX1099,198.99,USD-PROCESSED"
    assert last_line == expected_last_line, f"Expected last line to be '{expected_last_line}', but got '{last_line}'."

def test_go_source_fixed():
    path = "/home/user/tx-processor.go"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "len(records)-1" not in content, f"The off-by-one bug 'len(records)-1' is still present in {path}."