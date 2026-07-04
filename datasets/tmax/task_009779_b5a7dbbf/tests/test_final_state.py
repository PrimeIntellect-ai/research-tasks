# test_final_state.py

import os

def test_merged_archives_directory():
    """Verify that the merged_archives directory exists and contains the merged tarballs."""
    merged_dir = "/home/user/merged_archives"
    assert os.path.isdir(merged_dir), f"Directory {merged_dir} does not exist."

    merged_files = os.listdir(merged_dir)
    assert any("backup_A" in f for f in merged_files), "backup_A.tar (or similar) not found in merged_archives."
    assert any("backup_B" in f for f in merged_files), "backup_B.tar (or similar) not found in merged_archives."

def test_unsafe_paths_log():
    """Verify that unsafe paths are correctly identified and sorted alphabetically."""
    log_path = "/home/user/unsafe_paths.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_paths = [
        "../../../etc/shadow",
        "../../var/backups/shadow.bak",
        "/root/.ssh/authorized_keys",
        "safe_directory/../../etc/passwd"
    ]
    expected_paths.sort()

    assert lines == expected_paths, f"Unsafe paths log content is incorrect. Expected {expected_paths}, got {lines}"

def test_critical_disk_errors_txt():
    """Verify that the critical disk error timestamps are correctly extracted and sorted chronologically."""
    txt_path = "/home/user/critical_disk_errors.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist."

    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_timestamps = [
        "2023-10-15T14:22:10Z",
        "2023-11-01T09:12:34Z"
    ]

    assert lines == expected_timestamps, f"Critical disk errors content is incorrect. Expected {expected_timestamps}, got {lines}"