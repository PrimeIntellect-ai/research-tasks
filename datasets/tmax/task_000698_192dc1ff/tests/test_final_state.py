# test_final_state.py

import os
import pytest

def test_backup_files_exist():
    # Check that new files are backed up
    assert os.path.exists("/workspace/backup/file_new.txt"), "/workspace/backup/file_new.txt was not backed up."
    assert os.path.exists("/workspace/backup/dirA/file_new_2.txt"), "/workspace/backup/dirA/file_new_2.txt was not backed up."
    assert os.path.exists("/workspace/backup/dirB/nested/link_to_A/file_new_2.txt"), "/workspace/backup/dirB/nested/link_to_A/file_new_2.txt was not backed up."

def test_old_file_not_backed_up():
    # Check that old files are NOT backed up
    assert not os.path.exists("/workspace/backup/file_old.txt"), "/workspace/backup/file_old.txt should not be backed up because it is older than last_backup_time."

def test_backup_log_contains_loops():
    log_path = "/workspace/backup.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_lines = [
        "LOOP DETECTED: /workspace/data/dirA/loop_link",
        "LOOP DETECTED: /workspace/data/dirB/nested/link_to_A/loop_link",
        "LOOP DETECTED: /workspace/data/dirC/self_loop"
    ]

    for expected_line in expected_lines:
        assert expected_line in log_content, f"Expected log line '{expected_line}' not found in {log_path}."