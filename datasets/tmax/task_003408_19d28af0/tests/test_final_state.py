# test_final_state.py

import os
import stat
import pytest

def test_systemd_service_file_updated():
    service_file = "/home/user/.config/systemd/user/data-analyzer.service"
    assert os.path.isfile(service_file), f"Systemd service file {service_file} is missing."

    with open(service_file, "r") as f:
        content = f.read()

    assert "After=data-collector.service" in content, "Service file does not contain the required 'After=data-collector.service' directive."

    # Basic check to ensure it's in the [Unit] section (simplistic check)
    unit_idx = content.find("[Unit]")
    service_idx = content.find("[Service]")
    after_idx = content.find("After=data-collector.service")

    assert unit_idx != -1, "Missing [Unit] section."
    if service_idx != -1:
        assert unit_idx < after_idx < service_idx, "'After=' directive is not in the [Unit] section."

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

def test_deploy_v3_directory_and_config():
    v3_dir = "/home/user/deploy/releases/v3"
    assert os.path.isdir(v3_dir), f"Directory {v3_dir} was not created."

    config_file = os.path.join(v3_dir, "config.ini")
    assert os.path.isfile(config_file), f"Config file {config_file} is missing."

    with open(config_file, "r") as f:
        content = f.read().strip()
    assert content == "secure_mode=true", f"Config file contains incorrect text: {content}"

    # Check permissions (0400)
    st = os.stat(config_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Config file permissions are {oct(perms)}, expected 0o400."

def test_current_symlink_points_to_v3():
    symlink_path = "/home/user/deploy/current"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    assert target == "/home/user/deploy/releases/v3", f"Symlink points to {target} instead of /home/user/deploy/releases/v3."

def test_verification_log():
    log_file = "/home/user/verification.log"
    assert os.path.isfile(log_file), f"Verification log {log_file} is missing."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, "Verification log does not contain at least 3 lines."
    assert lines[0] == "/home/user/deploy/releases/v3", f"Line 1 is incorrect: {lines[0]}"
    assert lines[1] in ["400", "0400"], f"Line 2 is incorrect: {lines[1]}"
    assert lines[2] == "After=data-collector.service", f"Line 3 is incorrect: {lines[2]}"