# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist():
    """Verify that all required files and binaries exist and have correct permissions."""
    expected_files = [
        "/home/user/rate_filter.c",
        "/home/user/build.sh",
        "/home/user/prop_test.py",
        "/home/user/rate_filter_strict",
        "/home/user/rate_filter_standard",
        "/home/user/test_results.log"
    ]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected file {filepath} does not exist."

    # Check executable permissions
    assert os.access("/home/user/build.sh", os.X_OK), "build.sh is not executable."
    assert os.access("/home/user/rate_filter_strict", os.X_OK), "rate_filter_strict is not executable."
    assert os.access("/home/user/rate_filter_standard", os.X_OK), "rate_filter_standard is not executable."

def test_test_results_log():
    """Verify that test_results.log contains exactly 'PASS'."""
    log_path = "/home/user/test_results.log"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "PASS", f"Expected test_results.log to contain 'PASS', but got '{content}'"

def test_rate_filter_strict():
    """Verify the logic of rate_filter_strict (MAX_REQ=2)."""
    input_data = (
        "1000 1.1.1.1 A\n"
        "1000 1.1.1.1 B\n"
        "1000 1.1.1.1 C\n"
        "1000 1.1.1.1 D\n"
        "1000 1.1.1.2 E\n"
        "1000 1.1.1.2 F\n"
        "1000 1.1.1.2 G\n"
        "1001 1.1.1.1 H\n"
        "1001 1.1.1.1 I\n"
        "1001 1.1.1.1 J\n"
    )
    expected_output = (
        "1000 1.1.1.1 A\n"
        "1000 1.1.1.1 B\n"
        "1000 1.1.1.2 E\n"
        "1000 1.1.1.2 F\n"
        "1001 1.1.1.1 H\n"
        "1001 1.1.1.1 I\n"
    )

    process = subprocess.run(
        ["/home/user/rate_filter_strict"],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert process.returncode == 0, "rate_filter_strict crashed or returned non-zero exit code."
    assert process.stdout == expected_output, "rate_filter_strict output did not match expected logic."

def test_rate_filter_standard():
    """Verify the logic of rate_filter_standard (MAX_REQ=5)."""
    input_data = (
        "1000 1.1.1.1 A\n"
        "1000 1.1.1.1 B\n"
        "1000 1.1.1.1 C\n"
        "1000 1.1.1.1 D\n"
        "1000 1.1.1.2 E\n"
        "1000 1.1.1.2 F\n"
        "1000 1.1.1.2 G\n"
        "1001 1.1.1.1 H\n"
        "1001 1.1.1.1 I\n"
        "1001 1.1.1.1 J\n"
    )
    expected_output = (
        "1000 1.1.1.1 A\n"
        "1000 1.1.1.1 B\n"
        "1000 1.1.1.1 C\n"
        "1000 1.1.1.1 D\n"
        "1000 1.1.1.2 E\n"
        "1000 1.1.1.2 F\n"
        "1000 1.1.1.2 G\n"
        "1001 1.1.1.1 H\n"
        "1001 1.1.1.1 I\n"
        "1001 1.1.1.1 J\n"
    )

    process = subprocess.run(
        ["/home/user/rate_filter_standard"],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert process.returncode == 0, "rate_filter_standard crashed or returned non-zero exit code."
    assert process.stdout == expected_output, "rate_filter_standard output did not match expected logic."