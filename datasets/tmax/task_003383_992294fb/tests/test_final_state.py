# test_final_state.py

import os
import pytest

def test_source_code_and_executable():
    assert os.path.isfile("/home/user/archiver.c"), "/home/user/archiver.c is missing"
    assert os.path.isfile("/home/user/archiver"), "/home/user/archiver executable is missing"
    assert os.access("/home/user/archiver", os.X_OK), "/home/user/archiver is not executable"

def test_backup_dir_contents():
    backup_dir = "/home/user/backup_dir"
    assert os.path.isdir(backup_dir), f"{backup_dir} directory is missing"

    # Get inodes of the resolved files
    ls_inode = os.stat("/home/user/app_tree/dirA/utility_ls").st_ino
    cat_inode = os.stat("/home/user/app_tree/dirC/utility_cat").st_ino

    expected_files = {
        f"utility_ls_{ls_inode}.bak",
        f"utility_cat_{cat_inode}.bak",
        f"link_ls_{ls_inode}.bak"
    }

    actual_files = set(os.listdir(backup_dir))

    for ef in expected_files:
        assert ef in actual_files, f"Expected file {ef} is missing from {backup_dir}"

    for f in actual_files:
        assert "readme" not in f.lower(), "Non-ELF file readme.txt was incorrectly backed up"
        assert "random" not in f.lower(), "Non-ELF file random.bin was incorrectly backed up"

def test_backup_log():
    log_file = "/home/user/backup_log.txt"
    assert os.path.isfile(log_file), f"{log_file} is missing"

    with open(log_file, "r") as f:
        log_contents = f.read()

    ls_inode = os.stat("/home/user/app_tree/dirA/utility_ls").st_ino
    cat_inode = os.stat("/home/user/app_tree/dirC/utility_cat").st_ino

    ls_real = os.path.realpath("/home/user/app_tree/dirA/utility_ls")
    cat_real = os.path.realpath("/home/user/app_tree/dirC/utility_cat")
    link_ls_real = os.path.realpath("/home/user/app_tree/dirC/link_ls")

    expected_lines = [
        f"COPIED: {ls_real} -> /home/user/backup_dir/utility_ls_{ls_inode}.bak",
        f"COPIED: {cat_real} -> /home/user/backup_dir/utility_cat_{cat_inode}.bak",
        f"COPIED: {link_ls_real} -> /home/user/backup_dir/link_ls_{ls_inode}.bak"
    ]

    for line in expected_lines:
        assert line in log_contents, f"Expected log entry missing or malformed: {line}"