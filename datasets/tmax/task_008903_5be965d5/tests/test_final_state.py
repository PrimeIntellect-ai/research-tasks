# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    """Verify that the C++ source file exists."""
    source_path = "/home/user/vuln_scanner.cpp"
    assert os.path.isfile(source_path), f"C++ source file {source_path} does not exist."

def test_compiled_binary_exists():
    """Verify that the compiled binary exists and is executable."""
    binary_path = "/home/user/vuln_scanner"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_scan_results_file_exists():
    """Verify that the scan results file exists."""
    results_path = "/home/user/scan_results.txt"
    assert os.path.isfile(results_path), f"Scan results file {results_path} does not exist."

def test_scan_results_content():
    """Verify the content of the scan results file matches the expected output."""
    results_path = "/home/user/scan_results.txt"
    assert os.path.isfile(results_path), f"Scan results file {results_path} does not exist."

    expected_content = [
        "fake_bin: SUID=Yes, SHADOW_IN_RODATA=No",
        "safe_bin: SUID=No, SHADOW_IN_RODATA=No",
        "suid_bin: SUID=Yes, SHADOW_IN_RODATA=Yes"
    ]

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_content, f"Content of {results_path} does not match the expected output. Got: {lines}"