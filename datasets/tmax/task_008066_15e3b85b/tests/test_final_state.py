# test_final_state.py

import os
import pytest

def test_c_program_exists_and_executable():
    c_file = "/home/user/parse_logs.c"
    exe_file = "/home/user/parse_logs"

    assert os.path.isfile(c_file), f"C source file {c_file} does not exist."
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_raw_critical_txt_contents():
    raw_file = "/home/user/raw_critical.txt"
    assert os.path.isfile(raw_file), f"Output file {raw_file} does not exist."

    with open(raw_file, "r") as f:
        content = f.read()

    # Check for symlink outputs
    expected_symlinks = [
        "SYMLINK: /home/user/backup_data/folderB/link_to_A",
        "SYMLINK: /home/user/backup_data/folderA/link_to_B"
    ]
    for symlink in expected_symlinks:
        assert symlink in content, f"Expected symlink output missing in {raw_file}: '{symlink}'"

    # Check for critical failure outputs
    expected_db_log = (
        "/home/user/backup_data/folderA/db_backup.log: [2023-11-02] Backup progressing\n"
        "Writing to tape...\n"
        "CRITICAL_FAILURE: Tape drive jammed.\n"
        "Retrying..."
    )
    expected_sys_log = (
        "/home/user/backup_data/system.log: [2023-10-16] Rebooting\n"
        "Kernel panic...\n"
        "CRITICAL_FAILURE on boot sector.\n"
        "Please replace drive."
    )

    assert expected_db_log in content, f"Expected DB log entry missing or incorrectly formatted in {raw_file}."
    assert expected_sys_log in content, f"Expected system log entry missing or incorrectly formatted in {raw_file}."

def test_summary_csv_contents():
    csv_file = "/home/user/summary.csv"
    assert os.path.isfile(csv_file), f"Summary CSV file {csv_file} does not exist."

    with open(csv_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/backup_data/folderA/db_backup.log,2023-11-02",
        "/home/user/backup_data/system.log,2023-10-16"
    ]

    lines.sort()
    expected_lines.sort()

    assert lines == expected_lines, f"Contents of {csv_file} do not match expected output. Got: {lines}"