# test_final_state.py

import os
import pytest

def test_v1_link_exists_and_correct():
    link_path = '/home/user/valid_backups/v1.0_link.zip'
    target_path = '/home/user/archives/backup1.zip'

    assert os.path.exists(link_path), f"Expected link {link_path} does not exist."
    assert os.path.islink(link_path), f"{link_path} exists but is not a symbolic link."

    actual_target = os.readlink(link_path)
    assert actual_target == target_path, f"Link {link_path} points to {actual_target}, expected {target_path}."

def test_v2_link_exists_and_correct():
    link_path = '/home/user/valid_backups/v2.0_link.zip'
    target_path = '/home/user/archives/backup2.zip'

    assert os.path.exists(link_path), f"Expected link {link_path} does not exist."
    assert os.path.islink(link_path), f"{link_path} exists but is not a symbolic link."

    actual_target = os.readlink(link_path)
    assert actual_target == target_path, f"Link {link_path} points to {actual_target}, expected {target_path}."

def test_v3_link_does_not_exist():
    link_path = '/home/user/valid_backups/v3.0_link.zip'

    assert not os.path.exists(link_path) and not os.path.islink(link_path), \
        f"Link {link_path} should not exist because the archive is corrupted."

def test_no_unexpected_links():
    valid_dir = '/home/user/valid_backups'
    if os.path.isdir(valid_dir):
        files = os.listdir(valid_dir)
        expected_files = {'v1.0_link.zip', 'v2.0_link.zip'}
        actual_files = set(files)
        unexpected = actual_files - expected_files
        assert not unexpected, f"Found unexpected files in {valid_dir}: {unexpected}"