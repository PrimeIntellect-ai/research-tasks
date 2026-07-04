# test_final_state.py

import os
import json
import re
import pytest

BASE_DIR = "/home/user/observability"
LOGS_DIR = os.path.join(BASE_DIR, "logs")

def test_directories_exist():
    """Verify that the base and logs directories exist."""
    assert os.path.isdir(BASE_DIR), f"{BASE_DIR} does not exist"
    assert os.path.isdir(LOGS_DIR), f"{LOGS_DIR} does not exist"

def test_files_exist():
    """Verify that all required scripts and configuration files exist."""
    expected_files = [
        os.path.join(BASE_DIR, "telemetry_generator.py"),
        "/home/user/.config/systemd/user/telemetry.service",
        os.path.join(BASE_DIR, "logrotate.conf"),
        os.path.join(BASE_DIR, "deploy.py"),
        os.path.join(BASE_DIR, "version.txt")
    ]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"File missing: {filepath}"

def test_version_file_content():
    """Verify that version.txt ends up with the final version v1.2."""
    version_path = os.path.join(BASE_DIR, "version.txt")
    with open(version_path, 'r') as f:
        version = f.read().strip()
    assert version == "v1.2", f"Expected version.txt to be 'v1.2', got '{version}'"

def test_systemd_service_content():
    """Verify the contents of the systemd service file."""
    service_path = "/home/user/.config/systemd/user/telemetry.service"
    with open(service_path, 'r') as f:
        content = f.read()
    assert "ExecStart=" in content, "Service file missing ExecStart directive"
    assert "telemetry_generator.py" in content, "Service file missing script reference in ExecStart"
    assert "Restart=always" in content or "Restart=on-failure" in content, "Service missing restart condition (Restart=always or Restart=on-failure)"
    assert "WorkingDirectory=/home/user/observability" in content, "Service missing WorkingDirectory=/home/user/observability"

def test_logrotate_conf_content():
    """Verify the contents of the logrotate configuration."""
    logrotate_path = os.path.join(BASE_DIR, "logrotate.conf")
    with open(logrotate_path, 'r') as f:
        content = f.read()

    # Check for size 1k or size 1024
    assert re.search(r'size\s+(1k|1024)', content, re.IGNORECASE) or "size=1k" in content.replace(" ", ""), "logrotate.conf missing size 1k requirement"
    assert "rotate 3" in content, "logrotate.conf missing 'rotate 3'"
    assert "compress" in content, "logrotate.conf missing 'compress'"

def test_logs_and_rotation():
    """Verify that logs were generated and rotated by deploy.py."""
    log_files = os.listdir(LOGS_DIR)
    assert "telemetry.log" in log_files, "telemetry.log missing from logs directory"

    compressed_logs = [f for f in log_files if f.endswith(".gz")]
    assert len(compressed_logs) > 0, "No compressed rotated logs found. deploy.py may not have successfully run logrotate."

def test_telemetry_json_format():
    """Verify that the generated telemetry logs are in the correct JSON format."""
    telemetry_path = os.path.join(LOGS_DIR, "telemetry.log")
    with open(telemetry_path, 'r') as f:
        lines = f.readlines()

    # It's possible the file was just rotated and is empty, but if there are lines, check them
    for line in lines[-5:]:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            assert "timestamp" in data, "JSON log missing 'timestamp' key"
            assert "cpu" in data, "JSON log missing 'cpu' key"
            assert "version" in data, "JSON log missing 'version' key"

            assert isinstance(data["timestamp"], (int, float)), "'timestamp' should be a float/int"
            assert isinstance(data["cpu"], int), "'cpu' should be an integer"
            assert 0 <= data["cpu"] <= 100, "'cpu' should be between 0 and 100"
        except json.JSONDecodeError:
            pytest.fail(f"Log line is not valid JSON: {line}")