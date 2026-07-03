# test_final_state.py

import os
import stat
import pytest

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy_update.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

def test_fstab_updated_idempotently():
    fstab_path = "/home/user/mock_etc/fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        lines = f.readlines()

    target_line = "UUID=99A1-B2C3 /home/user/app_backup ext4 defaults 0 2"
    count = sum(1 for line in lines if target_line in line)

    assert count == 1, f"Expected exactly 1 instance of '{target_line}' in {fstab_path}, found {count}."

def test_firewall_rules_updated_idempotently():
    firewall_path = "/home/user/mock_etc/firewall.rules"
    assert os.path.isfile(firewall_path), f"File {firewall_path} does not exist."

    with open(firewall_path, "r") as f:
        lines = f.readlines()

    target_line = "FORWARD TCP 8080 -> 9090"
    count = sum(1 for line in lines if target_line in line)

    assert count == 1, f"Expected exactly 1 instance of '{target_line}' in {firewall_path}, found {count}."

def test_app_data_directory_permissions():
    app_data_path = "/home/user/app_data"
    assert os.path.isdir(app_data_path), f"Directory {app_data_path} does not exist."

    st = os.stat(app_data_path)
    permissions = stat.S_IMODE(st.st_mode)

    assert permissions == 0o700, f"Expected permissions 0o700 for {app_data_path}, got {oct(permissions)}."

def test_deployment_log_contents():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    expected_lines = [
        "[SUCCESS] Mount configured",
        "[SUCCESS] Firewall updated",
        "[SUCCESS] Permissions set"
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in {log_path}."