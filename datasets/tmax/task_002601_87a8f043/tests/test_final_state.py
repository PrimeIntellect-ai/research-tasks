# test_final_state.py

import os
import pytest

def test_deploy_script_exists():
    script_path = "/home/user/deploy.py"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."

def test_v2_config_symlink():
    v2_config_symlink = "/home/user/migration/v2/config.json"
    expected_target = "/home/user/migration/config.json"

    assert os.path.islink(v2_config_symlink), f"{v2_config_symlink} is not a symlink. Ensure the script creates this symlink."
    actual_target = os.readlink(v2_config_symlink)
    assert actual_target == expected_target, f"{v2_config_symlink} points to {actual_target}, expected {expected_target}."

def test_app_current_symlink():
    app_current_symlink = "/home/user/app_current"
    expected_target = "/home/user/migration/v2"

    assert os.path.islink(app_current_symlink), f"{app_current_symlink} is not a symlink. Ensure the script updates this symlink atomically."
    actual_target = os.readlink(app_current_symlink)
    assert actual_target == expected_target, f"{app_current_symlink} points to {actual_target}, expected {expected_target}."

def test_deploy_log_updated():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Deployment log {log_path} is missing."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"Deployment log {log_path} is empty."

    last_line = lines[-1]
    expected_line = "DEPLOYED v2 TO /home/user/migration/v2 WITH CONFIG /home/user/migration/v2/config.json"

    assert last_line == expected_line, f"The last line of {log_path} was '{last_line}', expected '{expected_line}'."