# test_final_state.py

import os
import re
import pytest

def test_c_source_exists_and_contains_required_functions():
    """Test that disk_nav.c exists and contains required system calls."""
    source_file = "/home/user/disk_nav.c"
    assert os.path.isfile(source_file), f"Source file {source_file} does not exist."

    with open(source_file, "r") as f:
        content = f.read()

    assert re.search(r'\b(flock|fcntl)\b', content), "Source file must contain 'flock' or 'fcntl' for file locking."
    assert re.search(r'\brename\b', content), "Source file must contain 'rename' for atomic file update."
    assert re.search(r'\bfork\b', content), "Source file must contain 'fork' for process creation."

def test_compiled_binary_exists():
    """Test that the compiled binary exists and is executable."""
    binary_file = "/home/user/disk_nav"
    assert os.path.isfile(binary_file), f"Compiled binary {binary_file} does not exist."
    assert os.access(binary_file, os.X_OK), f"Compiled binary {binary_file} is not executable."

def test_storage_root_structure():
    """Test that the required test directory structure and file sizes are correct."""
    expected_files = {
        "/home/user/storage_root/file_A.dat": 2000,
        "/home/user/storage_root/dir1/file_B.dat": 5000,
        "/home/user/storage_root/dir1/file_C.dat": 100,
        "/home/user/storage_root/dir2/sub/file_D.dat": 8000,
    }

    for filepath, expected_size in expected_files.items():
        assert os.path.isfile(filepath), f"Required test file {filepath} does not exist."
        actual_size = os.path.getsize(filepath)
        assert actual_size == expected_size, f"File {filepath} has size {actual_size}, expected {expected_size}."

def test_output_report_correctness():
    """Test that the output report contains the correct large files."""
    report_file = "/home/user/large_files_report.txt"
    assert os.path.isfile(report_file), f"Output report {report_file} does not exist."

    with open(report_file, "r") as f:
        lines = f.read().splitlines()

    # Remove empty lines and sort
    actual_lines = sorted([line.strip() for line in lines if line.strip()])

    expected_lines = [
        "5000 /home/user/storage_root/dir1/file_B.dat",
        "8000 /home/user/storage_root/dir2/sub/file_D.dat"
    ]

    assert actual_lines == sorted(expected_lines), f"Report contents are incorrect. Expected {expected_lines}, got {actual_lines}."