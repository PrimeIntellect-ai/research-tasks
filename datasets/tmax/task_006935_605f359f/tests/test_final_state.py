# test_final_state.py

import os
import pytest

def test_clean_new_manifest():
    clean_manifest_path = "/home/user/clean_new_manifest.csv"
    assert os.path.isfile(clean_manifest_path), f"File {clean_manifest_path} is missing."

    with open(clean_manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ART-001,/home/user/storage/vol1/artA.bin,1",
        "ART-002,/home/user/storage/vol1/artB.bin,3",
        "ART-003,/home/user/storage/vol2/artC.bin,1",
        "ART-004,/home/user/storage/vol2/artD.bin,1"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {clean_manifest_path}, got {len(lines)}."
    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {clean_manifest_path}."

def test_incremental_backup_directory_contents():
    backup_dir = "/home/user/incremental_backup"
    assert os.path.isdir(backup_dir), f"Directory {backup_dir} is missing."

    files = set(os.listdir(backup_dir))
    expected_files = {"artB.bin", "artD.bin"}

    assert files == expected_files, f"Expected backup directory to contain exactly {expected_files}, but got {files}."

    with open(os.path.join(backup_dir, "artB.bin"), "r") as f:
        assert f.read() == "binarydataB_v2", "Content of artB.bin in backup is incorrect."

    with open(os.path.join(backup_dir, "artD.bin"), "r") as f:
        assert f.read() == "binarydataD_v3", "Content of artD.bin in backup is incorrect."

def test_backup_log_contents():
    log_path = "/home/user/backup_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/storage/vol1/artB.bin",
        "/home/user/storage/vol2/artD.bin"
    ]

    assert lines == expected_lines, f"Expected log file lines to be exactly {expected_lines}, but got {lines}."