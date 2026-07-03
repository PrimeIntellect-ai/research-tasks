# test_final_state.py

import os
import pytest

def test_endpoints_log_content():
    log_file = "/home/user/endpoints.log"
    assert os.path.isfile(log_file), f"Expected log file {log_file} does not exist."

    expected_lines = [
        "app1.conf | CACHE | 10.0.0.6:6379",
        "app1.conf | DB | 10.0.0.5:5432",
        "app2.conf | DB | 192.168.1.100:3306",
        "app3.conf | CACHE | 172.16.0.4:11211",
        "app4.conf | DB | db.internal.net:27017"
    ]

    with open(log_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The content of endpoints.log does not match the expected output."

def test_remote_backup_sync():
    sync_dir = "/home/user/remote_backup/configs_sync"
    assert os.path.isdir(sync_dir), f"Expected backup directory {sync_dir} does not exist."

    expected_files = {"app1.conf", "app2.conf", "app3.conf", "app4.conf"}
    actual_files = set(os.listdir(sync_dir))

    assert expected_files.issubset(actual_files), f"Expected files {expected_files} are not all present in {sync_dir}."

def test_tracker_script_exists():
    script_file = "/home/user/tracker.py"
    assert os.path.isfile(script_file), f"Expected script {script_file} does not exist."
    assert os.access(script_file, os.R_OK), f"Script {script_file} is not readable."