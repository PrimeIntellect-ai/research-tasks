# test_final_state.py
import os
import json
import pytest

def test_backup_files_state():
    backup_dir = "/home/user/backups"

    expected_kept = ["backup_2.wal", "backup_4.wal"]
    expected_deleted = ["backup_1.wal", "backup_3.wal", "backup_5.wal"]

    for filename in expected_kept:
        filepath = os.path.join(backup_dir, filename)
        assert os.path.isfile(filepath), f"Expected backup file {filename} to be kept, but it is missing."

    for filename in expected_deleted:
        filepath = os.path.join(backup_dir, filename)
        assert not os.path.exists(filepath), f"Expected backup file {filename} to be deleted, but it still exists."

def test_cleanup_report_content():
    report_path = "/home/user/cleanup_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "backup_1.wal: 1500000000, arch: 0x3e",
        "backup_3.wal: 1400000000, arch: 0x28",
        "backup_5.wal: 1550000000, arch: 0xf3"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report, found {len(lines)}."

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in the report."