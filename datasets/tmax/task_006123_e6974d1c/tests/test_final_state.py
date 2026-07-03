# test_final_state.py

import os
import pytest

def test_extracted_directory_and_files():
    extract_dir = "/home/user/extracted"
    assert os.path.exists(extract_dir), f"Directory {extract_dir} does not exist."
    assert os.path.isdir(extract_dir), f"{extract_dir} is not a directory."

    expected_files = ["valid_log_A.txt", "valid_log_B.txt"]
    for fname in expected_files:
        fpath = os.path.join(extract_dir, fname)
        assert os.path.exists(fpath), f"Valid log file {fname} was not extracted to {extract_dir}."
        assert os.path.isfile(fpath), f"{fpath} is not a file."

    # Check that malicious files were not extracted
    extracted_contents = os.listdir(extract_dir)
    for item in extracted_contents:
        assert item in expected_files, f"Unexpected file {item} found in {extract_dir}. Malicious files should not be extracted."

def test_quarantine_log():
    quarantine_path = "/home/user/quarantine.log"
    assert os.path.exists(quarantine_path), f"Quarantine log {quarantine_path} does not exist."
    assert os.path.isfile(quarantine_path), f"{quarantine_path} is not a file."

    with open(quarantine_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_quarantined = [
        "../../../etc/passwd",
        "/home/user/.bashrc_override"
    ]

    for expected in expected_quarantined:
        assert expected in lines, f"Malicious path '{expected}' is missing from {quarantine_path}."

    assert len(lines) == len(expected_quarantined), f"{quarantine_path} contains unexpected entries."

def test_critical_errors_file():
    errors_path = "/home/user/critical_errors.txt"
    assert os.path.exists(errors_path), f"Critical errors file {errors_path} does not exist."
    assert os.path.isfile(errors_path), f"{errors_path} is not a file."

    with open(errors_path, "r") as f:
        content = f.read()

    expected_error_1 = (
        "[2023-10-25 10:05:00] ERROR Disk usage high.\n"
        "CRITICAL_SPACE_ERROR: Partition /dev/sda1 is at 99%.\n"
        "Please clean up old logs immediately."
    )

    expected_error_2 = (
        "[2023-10-26 11:20:00] ERROR Another disk error.\n"
        "CRITICAL_SPACE_ERROR: Failed to write to database.\n"
        "Check storage backend."
    )

    assert expected_error_1 in content, f"First critical error block is missing or formatted incorrectly in {errors_path}."
    assert expected_error_2 in content, f"Second critical error block is missing or formatted incorrectly in {errors_path}."

    # Ensure they are separated by a blank line
    assert expected_error_1 + "\n\n" + expected_error_2 in content or expected_error_2 + "\n\n" + expected_error_1 in content, \
        f"Critical errors in {errors_path} are not separated by a blank line as requested."