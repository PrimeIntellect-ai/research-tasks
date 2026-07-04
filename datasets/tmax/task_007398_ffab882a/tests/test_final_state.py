# test_final_state.py

import os
import pytest

def test_safe_extraction_valid_files():
    valid_file_path = '/home/user/project_data/valid_file.txt'
    deep_file_path = '/home/user/project_data/nested/deep_file.txt'

    assert os.path.isfile(valid_file_path), f"Expected file {valid_file_path} does not exist."
    with open(valid_file_path, 'r') as f:
        assert f.read() == 'This is a valid file.', f"Content of {valid_file_path} is incorrect."

    assert os.path.isfile(deep_file_path), f"Expected file {deep_file_path} does not exist."
    with open(deep_file_path, 'r') as f:
        assert f.read() == 'This is a deep file.', f"Content of {deep_file_path} is incorrect."

def test_safe_extraction_zip_slip_protection():
    escaped_file_path = '/home/user/escaped_file.txt'
    sneaky_file_path = '/home/user/sneaky.txt'

    assert not os.path.exists(escaped_file_path), f"Zip Slip vulnerability detected: {escaped_file_path} was extracted."
    assert not os.path.exists(sneaky_file_path), f"Zip Slip vulnerability detected: {sneaky_file_path} was extracted."

def test_symlink_creation():
    symlink_path = '/home/user/latest.txt'
    target_path = '/home/user/project_data/valid_file.txt'

    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."
    assert os.readlink(symlink_path) == target_path, f"Symlink {symlink_path} does not point to {target_path}."

def test_hard_link_backup():
    orig_valid = '/home/user/project_data/valid_file.txt'
    backup_valid = '/home/user/new_backup/valid_file.txt'

    orig_deep = '/home/user/project_data/nested/deep_file.txt'
    backup_deep = '/home/user/new_backup/nested/deep_file.txt'

    assert os.path.isfile(backup_valid), f"Backup file {backup_valid} does not exist."
    stat_orig = os.stat(orig_valid)
    stat_backup = os.stat(backup_valid)
    assert stat_orig.st_ino == stat_backup.st_ino, f"{backup_valid} is not a hard link to {orig_valid}."

    assert os.path.isfile(backup_deep), f"Backup file {backup_deep} does not exist."
    stat_orig_deep = os.stat(orig_deep)
    stat_backup_deep = os.stat(backup_deep)
    assert stat_orig_deep.st_ino == stat_backup_deep.st_ino, f"{backup_deep} is not a hard link to {orig_deep}."