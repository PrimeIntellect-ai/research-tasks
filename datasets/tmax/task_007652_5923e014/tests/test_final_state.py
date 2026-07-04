# test_final_state.py

import os
import re
import pytest

def test_systemd_service_fixed():
    service_path = "/home/user/.config/systemd/user/storage-monitor.service"
    assert os.path.exists(service_path), f"Service file missing: {service_path}"

    with open(service_path, 'r') as f:
        content = f.read()

    # Check that After=local-fs.target is in the [Unit] section
    unit_section_match = re.search(r'\[Unit\](.*?)(\[|$)', content, re.DOTALL)
    assert unit_section_match is not None, "Missing [Unit] section in service file"

    unit_section = unit_section_match.group(1)
    assert "After=local-fs.target" in unit_section.replace(" ", ""), "Service file missing 'After=local-fs.target' in [Unit] section"

def test_monitor_script_exists_and_executable():
    script_path = "/home/user/monitor.sh"
    assert os.path.exists(script_path), f"Monitor script missing: {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Monitor script is not executable: {script_path}"

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.exists(conf_path), f"Logrotate config missing: {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read().lower()

    assert "size 100" in content or "size=100" in content, "logrotate.conf missing 'size 100'"
    assert "rotate 5" in content or "rotate=5" in content, "logrotate.conf missing 'rotate 5'"
    assert "compress" in content, "logrotate.conf missing 'compress'"
    assert "missingok" in content, "logrotate.conf missing 'missingok'"
    assert "/home/user/storage-monitor.log" in content, "logrotate.conf must specify the correct log file"

def test_logrotate_success():
    rotated_log_path = "/home/user/storage-monitor.log.1.gz"
    assert os.path.exists(rotated_log_path), f"Rotated log file missing: {rotated_log_path}. Did you run the script, append 150 bytes, and run logrotate?"