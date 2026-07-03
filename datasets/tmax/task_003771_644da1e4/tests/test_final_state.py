# test_final_state.py

import os
import json
import pytest

def test_extracted_directories():
    assert os.path.isdir("/home/user/app_restored/config"), "The config directory was not extracted to /home/user/app_restored/config"
    assert os.path.isdir("/home/user/app_restored/system"), "The system directory was not extracted to /home/user/app_restored/system"

def test_symlink_active_config():
    link_path = "/home/user/active_config"
    expected_target = "/home/user/app_restored/config"
    assert os.path.islink(link_path), f"{link_path} is not a symbolic link"
    assert os.readlink(link_path) == expected_target, f"Symlink {link_path} does not point to {expected_target}"

def test_setup_env_script():
    script_path = "/home/user/setup_env.sh"
    assert os.path.isfile(script_path), f"Setup script {script_path} does not exist"
    with open(script_path, "r") as f:
        content = f.read()
    assert "APP_RESTORE_MODE" in content or ".env" in content, f"Setup script {script_path} does not seem to export variables from .env"

def test_bashrc_sourcing():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist"
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "setup_env.sh" in content, f"{bashrc_path} does not source setup_env.sh"

def test_identity_map_json():
    json_path = "/home/user/identity_map.json"
    assert os.path.isfile(json_path), f"Identity map {json_path} does not exist"
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON")

    expected_map = {
        "root": "root",
        "svc_app": "app_group",
        "bkp_admin": "bkp_operators"
    }
    assert data == expected_map, f"Identity map content {data} does not match expected {expected_map}"

def test_restore_report_json():
    report_path = "/home/user/restore_report.json"
    assert os.path.isfile(report_path), f"Restore report {report_path} does not exist"
    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON")

    expected_report = {
        "config_link_valid": True,
        "app_mode": "dry_run_validation",
        "mapped_users": {
            "root": "root",
            "svc_app": "app_group",
            "bkp_admin": "bkp_operators"
        }
    }
    assert data == expected_report, f"Restore report content {data} does not match expected {expected_report}"