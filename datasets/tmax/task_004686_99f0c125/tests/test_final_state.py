# test_final_state.py

import os
import pytest

def test_cpp_file_exists():
    """Test that the C++ source file exists."""
    assert os.path.isfile("/home/user/log_processor.cpp"), "The file /home/user/log_processor.cpp does not exist."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/log_processor"
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_cpp_source_requirements():
    """Test that the C++ source code uses zlib and flock."""
    with open("/home/user/log_processor.cpp", "r", encoding="utf-8") as f:
        content = f.read()

    # Check for zlib usage
    assert "gzopen" in content or "zlib.h" in content, "The source code does not appear to use zlib directly."

    # Check for file locking usage
    assert "flock" in content, "The source code does not appear to use POSIX flock for file locking."

def test_csv_output_exists_and_correct():
    """Test that the output CSV exists and contains exactly the expected critical events."""
    csv_path = "/home/user/critical_events.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} does not exist."

    expected_lines = {
        "2023-10-25T08:05:12,CRITICAL,RAID array degraded.",
        "2023-10-26T02:45:55,CRITICAL,Kernel panic - not syncing: VFS: Unable to mount root fs."
    }

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Check if all expected lines are present
    actual_lines_set = set(lines)
    for expected in expected_lines:
        assert expected in actual_lines_set, f"Expected line '{expected}' not found in {csv_path}."

    # Check that no non-CRITICAL lines were included
    for line in lines:
        assert line in expected_lines, f"Unexpected line found in {csv_path}: '{line}'"

    # Check that there are exactly the correct number of lines
    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines, but found {len(lines)}."