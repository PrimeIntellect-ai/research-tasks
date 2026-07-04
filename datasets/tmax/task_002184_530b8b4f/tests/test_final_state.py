# test_final_state.py

import os
import tarfile
import pytest

def test_deploy_sh_executable():
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_directories_exist():
    assert os.path.isdir("/home/user/backups"), "Directory /home/user/backups does not exist."
    assert os.path.isdir("/home/user/smtp_spool"), "Directory /home/user/smtp_spool does not exist."
    assert os.path.isdir("/home/user/edge_agent"), "Directory /home/user/edge_agent does not exist."

def test_tarball_exists_and_valid():
    tar_path = "/home/user/backups/telemetry_latest.tar.gz"
    assert os.path.isfile(tar_path), f"Backup archive {tar_path} does not exist."

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            names = tar.getnames()
            # The files might be stored with absolute or relative paths, so we check if the filenames are present
            has_sensor_1 = any("sensor_1.json" in name for name in names)
            has_sensor_2 = any("sensor_2.json" in name for name in names)
            assert has_sensor_1, "sensor_1.json not found in the backup tarball."
            assert has_sensor_2, "sensor_2.json not found in the backup tarball."
    except tarfile.ReadError:
        pytest.fail(f"{tar_path} is not a valid gzip tarball.")

def test_alert_email_content():
    eml_path = "/home/user/smtp_spool/alert.eml"
    assert os.path.isfile(eml_path), f"Alert email {eml_path} does not exist."

    with open(eml_path, "r") as f:
        content = f.read()

    assert "From: edge-daemon@iot.local" in content, "Missing or incorrect 'From' header in alert.eml."
    assert "To: noc@edge-corp.local" in content, "Missing or incorrect 'To' header in alert.eml."
    assert "Subject: [ALERT] Edge Device Failure" in content, "Missing or incorrect 'Subject' header in alert.eml."
    assert "Hardware watchdog reported a CRITICAL error." in content, "Missing or incorrect body text in alert.eml."

    lines = content.splitlines()
    body_idx = -1
    for i, line in enumerate(lines):
        if "Hardware watchdog reported a CRITICAL error." in line:
            body_idx = i
            break

    assert body_idx > 0, "Body text not found in alert.eml."
    assert lines[body_idx - 1].strip() == "", "There must be exactly one empty line between the headers and the body."