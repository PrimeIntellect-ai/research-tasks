# test_final_state.py

import os
import pytest

def test_max_value_report():
    report_path = "/home/user/max_value_report.txt"
    truth_path = "/tmp/ground_truth.txt"

    assert os.path.isfile(report_path), f"File {report_path} does not exist. The analysis script was not run or did not output correctly."
    assert os.path.isfile(truth_path), f"Ground truth file {truth_path} is missing."

    with open(truth_path, "r") as f:
        expected_val = f.read().strip()

    with open(report_path, "r") as f:
        actual_val = f.read().strip()

    assert actual_val == expected_val, f"The value in {report_path} ({actual_val}) does not match the expected maximum value ({expected_val})."

def test_extracted_v1_contents():
    extracted_dir = "/home/user/extracted_v1"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    expected_files = ["measurements.bin", "notes.txt", "update.log"]
    for f in expected_files:
        file_path = os.path.join(extracted_dir, f)
        assert os.path.isfile(file_path), f"Expected file {f} is missing from {extracted_dir}."

def test_backup_v1_contents():
    backup_v1_dir = "/home/user/backups/v1"
    assert os.path.isdir(backup_v1_dir), f"Directory {backup_v1_dir} does not exist."

    expected_files = ["measurements.bin", "notes.txt"]
    for f in expected_files:
        file_path = os.path.join(backup_v1_dir, f)
        assert os.path.isfile(file_path), f"Expected file {f} is missing from {backup_v1_dir}."

    unexpected_file = os.path.join(backup_v1_dir, "update.log")
    assert not os.path.exists(unexpected_file), f"File {unexpected_file} should not exist in the v1 backup."

def test_backup_v2_contents():
    backup_v2_dir = "/home/user/backups/v2"
    assert os.path.isdir(backup_v2_dir), f"Directory {backup_v2_dir} does not exist."

    expected_files = ["measurements.bin", "notes.txt", "update.log"]
    for f in expected_files:
        file_path = os.path.join(backup_v2_dir, f)
        assert os.path.isfile(file_path), f"Expected file {f} is missing from {backup_v2_dir}."

def test_hard_links():
    file_v1 = "/home/user/backups/v1/measurements.bin"
    file_v2 = "/home/user/backups/v2/measurements.bin"

    assert os.path.isfile(file_v1), f"File {file_v1} is missing."
    assert os.path.isfile(file_v2), f"File {file_v2} is missing."

    stat_v1 = os.stat(file_v1)
    stat_v2 = os.stat(file_v2)

    assert stat_v1.st_ino == stat_v2.st_ino, (
        f"Hard link verification failed: {file_v1} (inode {stat_v1.st_ino}) and "
        f"{file_v2} (inode {stat_v2.st_ino}) do not share the same inode. "
        "Incremental backup did not use hard links properly."
    )

    # Also verify notes.txt
    notes_v1 = "/home/user/backups/v1/notes.txt"
    notes_v2 = "/home/user/backups/v2/notes.txt"
    if os.path.isfile(notes_v1) and os.path.isfile(notes_v2):
        stat_notes_v1 = os.stat(notes_v1)
        stat_notes_v2 = os.stat(notes_v2)
        assert stat_notes_v1.st_ino == stat_notes_v2.st_ino, "notes.txt was not hard-linked between v1 and v2 backups."