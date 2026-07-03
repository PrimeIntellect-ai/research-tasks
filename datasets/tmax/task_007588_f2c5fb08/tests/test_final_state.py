# test_final_state.py

import os
import pytest

def test_processed_dat_files():
    file1_path = "/home/user/processed/dat/file1.dat"
    file2_path = "/home/user/processed/dat/file2.dat"

    assert os.path.isfile(file1_path), f"Missing processed file: {file1_path}"
    with open(file1_path, "rb") as f:
        assert f.read() == b"HELLO", f"Incorrect content in {file1_path}"

    assert os.path.isfile(file2_path), f"Missing processed file: {file2_path}"
    with open(file2_path, "rb") as f:
        assert f.read() == b"TEST", f"Incorrect content in {file2_path}"

def test_critical_errors_log():
    log_path = "/home/user/processed/critical_errors.txt"
    assert os.path.isfile(log_path), f"Missing critical errors log: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    # The records to look for (ignoring exact trailing/leading newlines on the whole file)
    record1 = "Warning: High memory usage\n[CRITICAL] Out of memory!\nPlease restart."
    record2 = "[CRITICAL] Database connection lost\nRetrying in 5 seconds..."

    # Check that both records are present
    assert record1 in content, "Missing or malformed first critical record in critical_errors.txt"
    assert record2 in content, "Missing or malformed second critical record in critical_errors.txt"

    # Check that the markers are NOT present
    assert "[RECORD_START]" not in content, "Found [RECORD_START] in critical_errors.txt, but markers should be excluded."
    assert "[RECORD_END]" not in content, "Found [RECORD_END] in critical_errors.txt, but markers should be excluded."

    # Check that non-critical records are NOT present
    assert "System booted" not in content, "Found non-critical record in critical_errors.txt."
    assert "User logged in" not in content, "Found non-critical record in critical_errors.txt."
    assert "Retry failed." not in content, "Found non-critical record in critical_errors.txt."