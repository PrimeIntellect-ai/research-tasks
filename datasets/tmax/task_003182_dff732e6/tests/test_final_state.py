# test_final_state.py
import os
import glob
import pytest

def test_summary_txt_exists_and_content():
    summary_path = "/home/user/dataset_processed/summary.txt"
    assert os.path.isfile(summary_path), f"File {summary_path} is missing."

    with open(summary_path, "r", encoding="utf-8") as f:
        content = f.read().splitlines()

    expected_lines = [
        "sensor_A.csv: 30.7",
        "sensor_B.csv: 150.4"
    ]

    for expected in expected_lines:
        assert expected in content, f"Expected line '{expected}' not found in {summary_path}"

def test_backup_script_exists_and_executable():
    script_path = "/home/user/backup.sh"
    assert os.path.isfile(script_path), f"Backup script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Backup script {script_path} is not executable."

def test_snapshot_file_exists():
    snapshot_path = "/home/user/backup/snapshot.snar"
    assert os.path.isfile(snapshot_path), f"Snapshot file {snapshot_path} is missing."

def test_backup_tar_gz_exists():
    backup_dir = "/home/user/backup/"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} is missing."

    tar_files = glob.glob(os.path.join(backup_dir, "*.tar.gz"))
    assert len(tar_files) == 1, f"Expected exactly one .tar.gz file in {backup_dir}, found {len(tar_files)}."