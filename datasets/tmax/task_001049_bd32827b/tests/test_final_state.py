# test_final_state.py

import os
import pytest

def test_current_symlink():
    symlink_path = "/home/user/backups/current"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."
    target = os.readlink(symlink_path)
    # The task says it should point to the newly created backup directory (backup_2)
    # It might be an absolute path or relative path, so we resolve it.
    assert os.path.basename(target) == "backup_2", f"Expected symlink to point to backup_2, but points to {target}"

def test_backup_1_file1_content():
    path = "/home/user/backups/backup_1/file1.txt.rle"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    expected = "5A4B1C"
    assert content == expected, f"Content of {path} is '{content}', expected '{expected}'."

def test_backup_2_file1_content():
    path = "/home/user/backups/backup_2/file1.txt.rle"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    expected = "5A4B1C5Z"
    assert content == expected, f"Content of {path} is '{content}', expected '{expected}'."

def test_backup_1_file2_content():
    path = "/home/user/backups/backup_1/file2.txt.rle"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    expected = "4X4Y2Z"
    assert content == expected, f"Content of {path} is '{content}', expected '{expected}'."

def test_backup_2_file2_content():
    path = "/home/user/backups/backup_2/file2.txt.rle"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    expected = "4X4Y2Z"
    assert content == expected, f"Content of {path} is '{content}', expected '{expected}'."

def test_hard_link_for_file2():
    path1 = "/home/user/backups/backup_1/file2.txt.rle"
    path2 = "/home/user/backups/backup_2/file2.txt.rle"
    assert os.path.isfile(path1), f"File {path1} does not exist."
    assert os.path.isfile(path2), f"File {path2} does not exist."

    inode1 = os.stat(path1).st_ino
    inode2 = os.stat(path2).st_ino
    assert inode1 == inode2, f"Expected {path1} and {path2} to be hard linked (same inode), but got {inode1} and {inode2}."

def test_different_inodes_for_file1():
    path1 = "/home/user/backups/backup_1/file1.txt.rle"
    path2 = "/home/user/backups/backup_2/file1.txt.rle"
    assert os.path.isfile(path1), f"File {path1} does not exist."
    assert os.path.isfile(path2), f"File {path2} does not exist."

    inode1 = os.stat(path1).st_ino
    inode2 = os.stat(path2).st_ino
    assert inode1 != inode2, f"Expected {path1} and {path2} to have different inodes, but both have {inode1}."

def test_inode_log_format_and_content():
    log_path = "/home/user/inode_log.txt"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = 4
    assert len(lines) == expected_lines, f"Expected {expected_lines} lines in {log_path}, found {len(lines)}."

    expected_prefixes = [
        "file1_b1_inode:",
        "file1_b2_inode:",
        "file2_b1_inode:",
        "file2_b2_inode:"
    ]

    files = [
        "/home/user/backups/backup_1/file1.txt.rle",
        "/home/user/backups/backup_2/file1.txt.rle",
        "/home/user/backups/backup_1/file2.txt.rle",
        "/home/user/backups/backup_2/file2.txt.rle"
    ]

    for i in range(4):
        assert lines[i].startswith(expected_prefixes[i]), f"Line {i+1} does not start with '{expected_prefixes[i]}'."

        parts = lines[i].split(":", 1)
        assert len(parts) == 2, f"Line {i+1} is malformed: {lines[i]}"

        logged_inode = parts[1].strip()
        actual_inode = str(os.stat(files[i]).st_ino)
        assert logged_inode == actual_inode, f"Logged inode for {files[i]} was {logged_inode}, expected {actual_inode}."