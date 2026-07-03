# test_final_state.py
import os
import hashlib
import pytest

def get_expected_redacted_content():
    active_conf_path = "/home/user/active.conf"
    assert os.path.exists(active_conf_path), f"{active_conf_path} does not exist"

    with open(active_conf_path, "r") as f:
        lines = f.readlines()

    redacted_lines = []
    for line in lines:
        if line.startswith("password="):
            redacted_lines.append("password=***\n")
        elif line.startswith("token="):
            redacted_lines.append("token=***\n")
        else:
            redacted_lines.append(line)

    return "".join(redacted_lines)

def test_tracker_script_exists():
    script_path = "/home/user/tracker.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_backup_files_and_hardlink():
    redacted_content = get_expected_redacted_content()
    expected_hash = hashlib.sha256(redacted_content.encode('utf-8')).hexdigest()

    hash_file_path = f"/home/user/backups/{expected_hash}.conf"
    latest_file_path = "/home/user/backups/latest.conf"

    assert os.path.isfile(hash_file_path), f"Backup file {hash_file_path} does not exist."
    assert os.path.isfile(latest_file_path), f"Hard link {latest_file_path} does not exist."

    with open(hash_file_path, "r") as f:
        actual_content = f.read()
    assert actual_content == redacted_content, f"Content of {hash_file_path} is not correctly redacted."

    stat_hash = os.stat(hash_file_path)
    stat_latest = os.stat(latest_file_path)

    assert stat_hash.st_ino == stat_latest.st_ino, f"{latest_file_path} is not a hard link to {hash_file_path}."
    assert stat_hash.st_dev == stat_latest.st_dev, f"{latest_file_path} and {hash_file_path} are on different devices."