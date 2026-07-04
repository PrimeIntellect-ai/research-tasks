# test_final_state.py

import os
import pytest

def test_backup1_txt():
    path = "/home/user/backups/backup1.txt"
    assert os.path.isfile(path), f"File {path} was not created."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "AAAAABBB", f"Content of {path} is incorrect. Expected 'AAAAABBB', got '{content}'."

def test_backup3_txt():
    path = "/home/user/backups/backup3.txt"
    assert os.path.isfile(path), f"File {path} was not created."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "CC", f"Content of {path} is incorrect. Expected 'CC', got '{content}'."

def test_backup4_skipped():
    path = "/home/user/backups/backup4.txt"
    assert not os.path.exists(path), f"File {path} should not exist because backup4.rle has an invalid magic header."

def test_hardlinks_created():
    path1 = "/home/user/backups/backup1.txt"
    path2 = "/home/user/backups/backup2.txt"
    path5 = "/home/user/backups/backup5.txt"

    assert os.path.isfile(path1), f"Original file {path1} missing."
    assert os.path.isfile(path2), f"Deduplicated file {path2} missing."
    assert os.path.isfile(path5), f"Deduplicated file {path5} missing."

    stat1 = os.stat(path1)
    stat2 = os.stat(path2)
    stat5 = os.stat(path5)

    assert stat1.st_ino == stat2.st_ino, f"{path2} is not a hard link to {path1}."
    assert stat1.st_ino == stat5.st_ino, f"{path5} is not a hard link to {path1}."

def test_log_file():
    log_path = "/home/user/link_count.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "2", f"Log file {log_path} contains incorrect count. Expected '2', got '{content}'."