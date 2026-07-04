# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Test that the C source code file exists."""
    assert os.path.isfile("/home/user/wal_compiler.c"), "The source file /home/user/wal_compiler.c is missing."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    executable_path = "/home/user/wal_compiler"
    assert os.path.isfile(executable_path), f"The executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_compiled_config_output():
    """Test that the final configuration output matches the expected state."""
    output_path = "/home/user/compiled_config.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} is missing. Did the program run?"

    expected_output = (
        "debug=false\n"
        "hostname=server02\n"
        "port=8081\n"
        "retry_count=5\n"
    )

    with open(output_path, "r") as f:
        actual_output = f.read()

    # Strip trailing whitespace to be lenient about final newlines
    assert actual_output.strip() == expected_output.strip(), (
        f"The content of {output_path} is incorrect.\n"
        f"Expected:\n{expected_output.strip()}\n"
        f"Actual:\n{actual_output.strip()}"
    )

    # Also verify sorting and format explicitly
    lines = [line for line in actual_output.strip().split("\n") if line]
    assert sorted(lines) == lines, "The output lines are not sorted alphabetically by key."