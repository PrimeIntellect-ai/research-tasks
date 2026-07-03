# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    path = "/home/user/policy_scanner.cpp"
    assert os.path.isfile(path), f"Missing source file: {path}"

def test_cpp_binary_exists_and_executable():
    path = "/home/user/policy_scanner"
    assert os.path.isfile(path), f"Missing compiled binary: {path}"
    assert os.access(path, os.X_OK), f"Binary is not executable: {path}"

def test_scan_report_exists_and_correct():
    path = "/home/user/scan_report.log"
    assert os.path.isfile(path), f"Missing report file: {path}"

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "VULNERABILITY: JWT with alg=none found in app.conf",
        "VULNERABILITY: Weak password secret found in app.conf",
        "VULNERABILITY: Deprecated SSH key (ssh-dss) found in keys.txt"
    ]

    # Check that all expected lines are present
    for expected in expected_lines:
        assert expected in lines, f"Expected vulnerability not found in {path}: {expected}"

    # Check that no other vulnerabilities are incorrectly reported
    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} vulnerabilities, found {len(lines)}"

    # Check the sorting requirement (sorted by filename)
    # The lines for app.conf should appear before keys.txt
    app_conf_indices = [i for i, line in enumerate(lines) if "app.conf" in line]
    keys_txt_indices = [i for i, line in enumerate(lines) if "keys.txt" in line]

    assert len(app_conf_indices) == 2, "Expected exactly 2 vulnerabilities for app.conf"
    assert len(keys_txt_indices) == 1, "Expected exactly 1 vulnerability for keys.txt"

    assert max(app_conf_indices) < min(keys_txt_indices), "Vulnerabilities must be grouped and sorted alphabetically by filename"