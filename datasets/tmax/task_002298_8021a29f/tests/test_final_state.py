# test_final_state.py

import os
import json
import tarfile
import urllib.request
import urllib.error
import pytest

def test_config_json_exists():
    config_path = "/home/user/config.json"
    assert os.path.isfile(config_path), f"Expected configuration file is missing: {config_path}"

    with open(config_path, "r") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} is not valid JSON.")

    assert config_data.get("device_id") == "EDGE-404", "Incorrect device_id in config.json"
    assert config_data.get("telemetry") is True, "Incorrect telemetry setting in config.json"
    assert config_data.get("port") == 8080, "Incorrect port in config.json"

def test_backup_tarball_created():
    backup_path = "/home/user/backup/data_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup tarball missing: {backup_path}"
    assert tarfile.is_tarfile(backup_path), f"File {backup_path} is not a valid tar archive."

    with tarfile.open(backup_path, "r:gz") as tar:
        names = tar.getnames()
        # Verify that the readings.txt file from sensor_data is in the archive
        # The exact path in the archive depends on how they packed it, but it should contain readings.txt
        assert any("readings.txt" in name for name in names), "Backup archive does not contain readings.txt"

def test_deploy_report_json():
    report_path = "/home/user/deploy_report.json"
    assert os.path.isfile(report_path), f"Deployment report missing: {report_path}"

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert report_data.get("config_generated") is True, "Report 'config_generated' should be True."
    assert report_data.get("backup_created") is True, "Report 'backup_created' should be True."
    assert report_data.get("health_status") == "OK-EDGE-ACTIVE", "Report 'health_status' does not match expected output."

def test_service_is_running_and_healthy():
    url = "http://127.0.0.1:8080/health"
    try:
        req = urllib.request.urlopen(url, timeout=2)
        resp = req.read().decode('utf-8')
        assert resp == "OK-EDGE-ACTIVE", f"Service responded with unexpected payload: {resp}"
        assert req.getcode() == 200, f"Service responded with unexpected status code: {req.getcode()}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to service at {url}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during health check: {e}")