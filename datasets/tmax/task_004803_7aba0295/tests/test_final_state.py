# test_final_state.py

import os
import pytest

def test_archive_bin_size_and_mmap():
    log_dir = "/home/user/raw_logs"
    archive_bin = "/home/user/archive.bin"
    archiver_c = "/home/user/archiver.c"

    # Check if raw_logs directory exists
    assert os.path.isdir(log_dir), f"Directory not found: {log_dir}"

    total_lines = 0
    log_files_found = False
    for f in os.listdir(log_dir):
        if f.endswith('.log'):
            log_files_found = True
            with open(os.path.join(log_dir, f), 'r') as log_file:
                total_lines += sum(1 for _ in log_file)

    assert log_files_found, f"No .log files found in {log_dir}"

    # Check if archive.bin exists
    assert os.path.isfile(archive_bin), f"Output binary not found: {archive_bin}"

    expected_size = total_lines * 21
    actual_size = os.path.getsize(archive_bin)

    assert actual_size == expected_size, (
        f"Metric failed: Expected {expected_size} bytes (21 bytes per record for {total_lines} records), "
        f"got {actual_size} bytes."
    )

    # Verify mmap was used in the source code
    assert os.path.isfile(archiver_c), f"Source code not found: {archiver_c}"
    with open(archiver_c, "r") as f:
        source = f.read()
        assert "mmap" in source, "Metric failed: Source code does not use mmap."

def test_user_dict_csv_exists():
    user_dict = "/home/user/user_dict.csv"
    assert os.path.isfile(user_dict), f"User dictionary not found: {user_dict}"