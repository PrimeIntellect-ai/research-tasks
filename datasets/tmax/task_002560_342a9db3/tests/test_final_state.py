# test_final_state.py

import os
import pytest

def test_symlinks_created():
    expected_symlinks = {
        "/home/user/restore/app1/config.json": "/home/user/backup_data/app1/config.json",
        "/home/user/restore/app1/data.db": "/home/user/backup_data/app1/data.db",
        "/home/user/restore/app2/cache.bin": "/home/user/backup_data/app2/cache.bin"
    }

    for link_path, target_path in expected_symlinks.items():
        assert os.path.exists(link_path), f"Expected symlink {link_path} does not exist"
        assert os.path.islink(link_path), f"Path {link_path} is not a symlink"
        assert os.readlink(link_path) == target_path, f"Symlink {link_path} points to {os.readlink(link_path)}, expected {target_path}"

def test_missing_directory_ignored():
    missing_dest = "/home/user/restore/missing"
    assert not os.path.exists(missing_dest), f"Directory {missing_dest} should not have been created"

def test_log_files_exist_and_rotated():
    log_files = [
        "/home/user/restore_process.log",
        "/home/user/restore_process.log.1",
        "/home/user/restore_process.log.2"
    ]

    for log_file in log_files:
        assert os.path.exists(log_file), f"Log file {log_file} does not exist"
        assert os.path.isfile(log_file), f"Path {log_file} is not a file"

    # Check sizes for rotated logs (should be around 1024 bytes)
    size_1 = os.path.getsize("/home/user/restore_process.log.1")
    size_2 = os.path.getsize("/home/user/restore_process.log.2")

    assert 500 < size_1 < 2000, f"Rotated log 1 size {size_1} is not close to 1024 bytes"
    assert 500 < size_2 < 2000, f"Rotated log 2 size {size_2} is not close to 1024 bytes"

def test_no_extra_log_files():
    # backupCount=2 means .3 should not exist
    assert not os.path.exists("/home/user/restore_process.log.3"), "Found restore_process.log.3, but backupCount should be 2"

def test_log_content():
    # Check that the mock container output is in the logs
    content = ""
    for log_file in ["/home/user/restore_process.log", "/home/user/restore_process.log.1", "/home/user/restore_process.log.2"]:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                content += f.read()

    assert "Log line" in content, "Mock container output not found in log files"