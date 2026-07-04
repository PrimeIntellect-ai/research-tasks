# test_final_state.py

import os
import tarfile
import subprocess
import pytest

def test_backup_exists_and_valid():
    backup_path = "/home/user/services_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if at least one service.conf is in the tarball
            assert any("db/service.conf" in name for name in names), "Backup does not contain db/service.conf."
    except tarfile.TarError:
        pytest.fail(f"Backup file {backup_path} is not a valid gzip-compressed tarball.")

def test_scripts_exist():
    assert os.path.isfile("/home/user/fix_network.sh"), "Script /home/user/fix_network.sh is missing."
    assert os.path.isfile("/home/user/generate_report.sh"), "Script /home/user/generate_report.sh is missing."

def test_report_content():
    report_path = "/home/user/network_report.log"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    expected_lines = [
        "db:9001:none",
        "auth:9002:http://localhost:9001",
        "api:9003:http://localhost:9002",
        "web:9004:http://localhost:9003"
    ]

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, "Report content does not match the expected format and order."

def test_config_files_updated():
    base_dir = "/home/user/services"

    expected_configs = {
        "db": {"LISTEN_PORT": "9001", "UPSTREAM_URL": None, "extra": "TIMEOUT=30"},
        "auth": {"LISTEN_PORT": "9002", "UPSTREAM_URL": "http://localhost:9001", "extra": "LOG_LEVEL=debug"},
        "api": {"LISTEN_PORT": "9003", "UPSTREAM_URL": "http://localhost:9002", "extra": None},
        "web": {"LISTEN_PORT": "9004", "UPSTREAM_URL": "http://localhost:9003", "extra": "THEME=dark"}
    }

    for service, expected in expected_configs.items():
        conf_file = os.path.join(base_dir, service, "service.conf")
        assert os.path.isfile(conf_file), f"Config file {conf_file} is missing."

        with open(conf_file, "r") as f:
            content = f.read()

        assert f"LISTEN_PORT={expected['LISTEN_PORT']}" in content, f"Incorrect LISTEN_PORT in {service}/service.conf"

        if expected["UPSTREAM_URL"]:
            assert f"UPSTREAM_URL={expected['UPSTREAM_URL']}" in content, f"Incorrect UPSTREAM_URL in {service}/service.conf"

        if expected["extra"]:
            assert expected["extra"] in content, f"Original config line '{expected['extra']}' was removed from {service}/service.conf"

def test_idempotency():
    base_dir = "/home/user/services"
    script_path = "/home/user/fix_network.sh"

    # Read state before
    state_before = {}
    for service in ["db", "auth", "api", "web"]:
        conf_file = os.path.join(base_dir, service, "service.conf")
        with open(conf_file, "r") as f:
            state_before[service] = f.read()

    # Run script again
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed on second run."

    # Read state after and compare
    for service in ["db", "auth", "api", "web"]:
        conf_file = os.path.join(base_dir, service, "service.conf")
        with open(conf_file, "r") as f:
            state_after = f.read()

        assert state_before[service] == state_after, f"Script is not idempotent: {service}/service.conf changed on second run."