# test_final_state.py

import os
import pytest

def test_result_txt():
    """Test that the result.txt file exists and contains the correct output."""
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"{result_path} is missing. Did you redirect the output?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "1000", f"Expected output to be '1000', but got '{content}'."

def test_check_backup_c_parameterization():
    """Test that check_backup.c has been refactored to use parameterized queries."""
    c_file_path = '/home/user/check_backup.c'
    assert os.path.isfile(c_file_path), f"{c_file_path} is missing."

    with open(c_file_path, 'r') as f:
        content = f.read()

    assert "sqlite3_bind" in content, "The C program must use sqlite3_bind_* to parameterize the query."
    # Ensure sprintf is not used for injecting the ID into the query.
    # While we can't strictly forbid all sprintf, we can check that %s is not used in the query string.
    assert "%s" not in content, "The C program still appears to use string interpolation (%s) for the query."

def test_executable_exists():
    """Test that the compiled executable exists."""
    exe_path = '/home/user/check_backup'
    assert os.path.isfile(exe_path), f"{exe_path} is missing. Did you compile the program?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."