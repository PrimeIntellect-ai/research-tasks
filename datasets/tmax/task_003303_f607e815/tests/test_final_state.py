# test_final_state.py

import os
import pytest

def test_c_program_exists():
    assert os.path.isfile("/home/user/process.c"), "C source file /home/user/process.c does not exist."
    assert os.path.isfile("/home/user/process"), "Compiled executable /home/user/process does not exist."
    assert os.access("/home/user/process", os.X_OK), "Compiled file /home/user/process is not executable."

def test_processed_files_content():
    expected_files = {
        "year_2018.rle": "5A5G5C5T\n2A2T2C2G\n",
        "year_2019.rle": "10G2A\n",
        "year_2020.rle": "5T6A6C3G\n1A1T1C1G\n",
        "year_2021.rle": "16A1T\n"
    }

    processed_dir = "/home/user/processed"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(processed_dir, filename)
        assert os.path.isfile(filepath), f"Expected processed file {filepath} is missing."

        with open(filepath, "r") as f:
            content = f.read()

        assert content == expected_content, f"Content of {filepath} does not match expected RLE output."

def test_backup_hard_links():
    processed_dir = "/home/user/processed"
    backup_dir = "/home/user/backup"

    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    expected_files = ["year_2018.rle", "year_2019.rle", "year_2020.rle", "year_2021.rle"]

    for filename in expected_files:
        processed_path = os.path.join(processed_dir, filename)
        backup_path = os.path.join(backup_dir, filename)

        assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

        stat_processed = os.stat(processed_path)
        stat_backup = os.stat(backup_path)

        assert stat_processed.st_ino == stat_backup.st_ino, f"{backup_path} is not a hard link to {processed_path} (inodes differ)."

def test_latest_year_symlink():
    symlink_path = "/home/user/latest_year.sym"
    expected_target = "/home/user/processed/year_2021.rle"

    assert os.path.islink(symlink_path), f"{symlink_path} does not exist or is not a symbolic link."

    actual_target = os.readlink(symlink_path)
    # The symlink could be relative or absolute, we resolve it to absolute to compare
    if not os.path.isabs(actual_target):
        actual_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), actual_target))

    assert actual_target == expected_target, f"Symlink {symlink_path} points to {actual_target}, expected {expected_target}."