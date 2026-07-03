# test_final_state.py

import os
import pytest

def test_file3_modified():
    file3_path = "/home/user/data/file3.txt"
    assert os.path.isfile(file3_path), f"File {file3_path} does not exist."
    with open(file3_path, "r") as f:
        content = f.read()
    assert "new data v2" in content, f"Content of {file3_path} does not contain expected 'new data v2'. Got: {content}"

def test_backup_v2_hardlinks():
    v1_file1 = "/home/user/backup_v1/file1.txt"
    v2_file1 = "/home/user/backup_v2/file1.txt"
    v1_file2 = "/home/user/backup_v1/file2.txt"
    v2_file2 = "/home/user/backup_v2/file2.txt"

    assert os.path.isfile(v2_file1), f"File {v2_file1} does not exist."
    assert os.path.isfile(v2_file2), f"File {v2_file2} does not exist."

    inode_v1_f1 = os.stat(v1_file1).st_ino
    inode_v2_f1 = os.stat(v2_file1).st_ino
    assert inode_v1_f1 == inode_v2_f1, f"{v2_file1} is not a hard link to {v1_file1}."

    inode_v1_f2 = os.stat(v1_file2).st_ino
    inode_v2_f2 = os.stat(v2_file2).st_ino
    assert inode_v1_f2 == inode_v2_f2, f"{v2_file2} is not a hard link to {v1_file2}."

def test_backup_v2_rev_file():
    rev_file_path = "/home/user/backup_v2/file3.txt.rev"
    assert os.path.isfile(rev_file_path), f"File {rev_file_path} does not exist."
    with open(rev_file_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 1, f"File {rev_file_path} is empty."
    assert lines[0] == "2v atad wen", f"Content of {rev_file_path} is incorrect. Expected '2v atad wen', got: {lines[0]}"

def test_symlink():
    symlink_path = "/home/user/backup_latest"
    target_path = "/home/user/backup_v2"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    assert target == target_path, f"Symbolic link {symlink_path} points to {target}, expected {target_path}."