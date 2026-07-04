# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_output_directory_permissions():
    """Test that the output directory exists and has permissions 750."""
    path = "/home/user/migration/output"
    assert os.path.isdir(path), f"Directory {path} does not exist."

    st = os.stat(path)
    mode = oct(st.st_mode)[-3:]
    assert mode == "750", f"Directory {path} has permissions {mode}, expected 750."

def test_systemd_service_unit():
    """Test that the systemd service unit exists and has the correct configuration."""
    path = "/home/user/.config/systemd/user/data-migrator.service"
    assert os.path.isfile(path), f"Service file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "ExecStart=/home/user/migration/worker.py" in content, "ExecStart is missing or incorrect in service file."
    assert "WORKER_DATA_DIR=/home/user/migration/output" in content, "WORKER_DATA_DIR environment variable is missing or incorrect."
    assert "NODE_ENV=production" in content, "NODE_ENV environment variable is missing or incorrect."

def test_systemd_timer_unit():
    """Test that the systemd timer unit exists and has the correct configuration."""
    path = "/home/user/.config/systemd/user/data-migrator.timer"
    assert os.path.isfile(path), f"Timer file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "OnCalendar=" in content, "OnCalendar configuration is missing in timer file."
    # Check for 5-minute interval patterns
    assert re.search(r"OnCalendar=.*(\*:0/5|\*:0,5|/\s*5)", content), "Timer does not appear to be configured for every 5 minutes."

def test_health_check_script():
    """Test that the health check script exists, is executable, and contains required logic."""
    path = "/home/user/migration/health_check.sh"
    assert os.path.isfile(path), f"Health check script {path} does not exist."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/migration/output/data.txt" in content, "Script does not check for the correct data file."
    assert "STATUS: HEALTHY" in content, "Script does not contain the HEALTHY status string."
    assert "STATUS: DEGRADED" in content, "Script does not contain the DEGRADED status string."
    assert "/home/user/migration/metrics.log" in content, "Script does not write to the correct metrics log file."

def test_crontab_configuration():
    """Test that the crontab is configured correctly."""
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab or no crontab exists."

    content = result.stdout
    assert "health_check.sh" in content, "Crontab does not reference health_check.sh."
    assert "WORKER_DATA_DIR=/home/user/migration/output" in content, "Crontab does not set WORKER_DATA_DIR correctly."

    # Check for every minute schedule (* * * * * or similar)
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]
    found_cron = False
    for line in lines:
        if "health_check.sh" in line:
            parts = line.split()
            if parts[:5] == ["*", "*", "*", "*", "*"]:
                found_cron = True
                break

    assert found_cron, "Crontab does not schedule the script to run every minute (* * * * *)."