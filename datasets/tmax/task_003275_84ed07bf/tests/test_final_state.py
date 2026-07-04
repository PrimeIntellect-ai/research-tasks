# test_final_state.py

import os
import stat
import pytest

def test_incident_report():
    report_path = "/home/user/incident_report.txt"
    assert os.path.isfile(report_path), f"Incident report missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_timestamps = [
        "2023/10/24 11:20:05",
        "2023/10/24 12:25:10",
        "2023/10/24 13:30:15",
        "2023/10/24 14:35:20",
        "2023/10/24 15:40:25"
    ]

    assert lines == expected_timestamps, (
        f"Incident report does not contain the exact expected 5 timestamps. "
        f"Expected: {expected_timestamps}, Got: {lines}"
    )

def test_nginx_config_fixed():
    conf_path = "/home/user/nginx/conf/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    expected_directive = "proxy_pass http://unix:/home/user/app/run/backend.sock;"
    assert expected_directive in content, (
        f"The nginx.conf does not contain the correct proxy_pass directive. "
        f"Expected to find: '{expected_directive}'"
    )
    assert "wrong_backend.sock" not in content, "The nginx.conf still contains 'wrong_backend.sock'."

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script missing at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deploy script {script_path} is not executable."

def test_backup_created():
    backup_path = "/home/user/backup/nginx.conf.bak"
    conf_path = "/home/user/nginx/conf/nginx.conf"

    assert os.path.isfile(backup_path), f"Backup file missing at {backup_path}"

    with open(backup_path, "r") as f:
        backup_content = f.read()

    with open(conf_path, "r") as f:
        conf_content = f.read()

    assert backup_content == conf_content, "The backup file content does not match the current nginx.conf."

def test_log_rotation_occurred():
    app_log_path = "/home/user/app/logs/app.log"
    rotated_log_path = "/home/user/app/logs/app.log.1"

    assert os.path.isfile(rotated_log_path), (
        f"Rotated log file missing at {rotated_log_path}. "
        f"Ensure deploy.sh was executed and rotates logs correctly."
    )

    assert os.path.isfile(app_log_path), f"New empty log file missing at {app_log_path}"

    with open(app_log_path, "r") as f:
        content = f.read()

    assert content == "", f"The new {app_log_path} is not empty. It should be recreated as an empty file."