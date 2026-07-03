# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/project"

def test_shared_library_exists():
    lib_path = os.path.join(PROJECT_DIR, "lib", "libprocessor.so")
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did you compile it?"

    # Check if it's an ELF file (shared object)
    with open(lib_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"File {lib_path} is not a valid ELF binary."

def test_output_log():
    log_path = os.path.join(PROJECT_DIR, "output.log")
    assert os.path.isfile(log_path), f"Output log {log_path} does not exist. Did you run process.py?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in output.log, but found {len(lines)}."

    expected_lines = {
        "ID:1|VAL:3.14|NAME:alpha",
        "ID:2|VAL:2.71|NAME:beta"
    }

    actual_lines = set(lines)

    missing = expected_lines - actual_lines
    assert not missing, f"Missing expected lines in output.log: {missing}"

    unexpected = actual_lines - expected_lines
    assert not unexpected, f"Found unexpected lines in output.log (perhaps invalid files were processed?): {unexpected}"

    # Explicitly check that ID:3 is not present
    for line in lines:
        assert "ID:3" not in line, "Found data from invalid file (record_3.dat) in output.log."