# test_final_state.py

import os
import tarfile
import pytest

def test_filter_executable_exists():
    executable_path = "/home/user/filter"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_processed_log1():
    expected = (
        "BEGIN_RECORD\n"
        "ID: 102\n"
        "LEVEL: ERROR\n"
        "MESSAGE: Disk space low\n"
        "END_RECORD"
    )
    path = "/home/user/data/processed_logs/log1.log"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected, f"Content of {path} is incorrect. Expected ERROR record only."

def test_processed_log2():
    expected = (
        "BEGIN_RECORD\n"
        "ID: 201\n"
        "LEVEL: CRITICAL\n"
        "MESSAGE: Kernel panic\n"
        "END_RECORD"
    )
    path = "/home/user/data/processed_logs/log2.log"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected, f"Content of {path} is incorrect. Expected CRITICAL record only."

def test_incremental_backup():
    tar_path = "/home/user/data/inc_backup.tar"
    assert os.path.isfile(tar_path), f"Backup archive {tar_path} does not exist."

    try:
        with tarfile.open(tar_path, "r") as tar:
            names = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"Could not read {tar_path} as a valid tar archive.")

    # Check that the archived paths are relative to processed_logs/
    assert any("processed_logs/log1.log" in name for name in names), "processed_logs/log1.log is missing from the incremental backup."
    assert any("processed_logs/log2.log" in name for name in names), "processed_logs/log2.log is missing from the incremental backup."

    # Ensure the old log is not included, as it was in the base backup
    assert not any("old_log.log" in name for name in names), "processed_logs/old_log.log should NOT be in the incremental backup."