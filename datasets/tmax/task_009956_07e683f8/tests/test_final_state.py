# test_final_state.py

import os
import csv
import pytest

def test_failed_backups_csv_exists():
    csv_path = "/home/user/failed_backups.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

def test_failed_backups_csv_content():
    csv_path = "/home/user/failed_backups.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

    expected_rows = [
        ["timestamp", "absolute_file_path"],
        ["2023-09-15 01:50:33", "/home/user/archive_mounts/server_beta/app/logs/old/archive_2023.log"],
        ["2023-10-01 02:05:12", "/home/user/archive_mounts/server_alpha/var/log/backup.log"],
        ["2023-11-20 03:15:22", "/home/user/archive_mounts/server_gamma/sys/system.log"]
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, but got {actual}."