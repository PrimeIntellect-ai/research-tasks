# test_final_state.py

import os
import stat
import pytest

def test_filter_c_exists():
    """Verify that the C source file exists."""
    path = "/home/user/filter.c"
    assert os.path.isfile(path), f"Expected C source file {path} does not exist."

def test_filter_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    path = "/home/user/filter"
    assert os.path.isfile(path), f"Expected executable {path} does not exist."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {path} is not executable."

def test_fatal_errors_log_content():
    """Verify the output log contains exactly the FATAL error blocks from the raw log."""
    raw_log_path = "/home/user/raw_docs.log"
    output_log_path = "/home/user/fatal_errors.log"

    assert os.path.isfile(raw_log_path), f"Raw log file {raw_log_path} is missing."
    assert os.path.isfile(output_log_path), f"Output file {output_log_path} does not exist."

    expected_lines = []
    current_block = []
    in_block = False
    has_fatal = False

    with open(raw_log_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "[DOC-ERROR]":
                in_block = True
                current_block = [line]
                has_fatal = False
            elif in_block:
                current_block.append(line)
                if line.startswith("Severity: FATAL"):
                    has_fatal = True
                if stripped == "[END-ERROR]":
                    in_block = False
                    if has_fatal:
                        expected_lines.extend(current_block)

    with open(output_log_path, "r") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"The content of {output_log_path} does not match the expected output. "
        "It should contain only the blocks with 'Severity: FATAL' exactly as they appeared in the raw log."
    )