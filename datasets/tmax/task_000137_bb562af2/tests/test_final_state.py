# test_final_state.py

import os
import pytest

def test_symlink_rolled_back():
    symlink_path = "/home/user/app_current"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symlink."
    target = os.readlink(symlink_path)
    expected_target = "/home/user/deployments/v2"
    assert target == expected_target, f"Symlink points to {target}, expected {expected_target} after rollback."

def test_log_rotated_to_archive():
    archive_path = "/home/user/archives/v2_app.log.archive"
    assert os.path.isfile(archive_path), f"Expected archived log file at {archive_path}."

    with open(archive_path, "r") as f:
        content = f.read()
    assert "ERROR: database timeout" in content, f"Archived log {archive_path} does not contain the expected ERROR message."

def test_new_app_log_created_and_empty():
    new_log_path = "/home/user/deployments/v2/app.log"
    assert os.path.isfile(new_log_path), f"Expected new log file at {new_log_path}."

    size = os.path.getsize(new_log_path)
    assert size == 0, f"Expected {new_log_path} to be empty (0 bytes), but got {size} bytes."

def test_other_logs_untouched():
    v1_log = "/home/user/deployments/v1/app.log"
    v3_log = "/home/user/deployments/v3/app.log"

    assert os.path.isfile(v1_log), f"Expected {v1_log} to still exist."
    with open(v1_log, "r") as f:
        assert "Log v1: All good" in f.read(), f"{v1_log} content was unexpectedly altered."

    assert os.path.isfile(v3_log), f"Expected {v3_log} to still exist."
    with open(v3_log, "r") as f:
        assert "Log v3: startup" in f.read(), f"{v3_log} content was unexpectedly altered."