# test_final_state.py

import os
import json
import pytest

def test_symlink_fixed():
    symlink_path = "/home/user/service_configs/monitor.json"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symlink."

    target = os.readlink(symlink_path)
    expected_target = "/home/user/system_data/monitor.json"
    assert target == expected_target, f"Symlink target is incorrect. Expected {expected_target}, got {target}."

def test_supervisor_script_exists():
    script_path = "/home/user/supervisor.py"
    assert os.path.isfile(script_path), f"Supervisor script {script_path} does not exist."

def test_services_json_correct():
    services_path = "/home/user/services.json"
    assert os.path.isfile(services_path), f"Services definition file {services_path} does not exist."

    with open(services_path, "r") as f:
        try:
            services = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{services_path} is not a valid JSON file.")

    assert isinstance(services, list), f"Expected {services_path} to contain a JSON array."
    assert "qemu-system-x86_64 -display vnc=127.0.0.1:2 -nodefaults -no-reboot" in services, "QEMU command missing from services.json."
    assert "python3 /home/user/monitor.py" in services, "Monitor command missing from services.json."

def test_uptime_log_vnc_ok():
    uptime_log_path = "/home/user/uptime.log"
    assert os.path.isfile(uptime_log_path), f"Uptime log {uptime_log_path} does not exist."

    with open(uptime_log_path, "r") as f:
        lines = f.readlines()

    vnc_ok_count = sum(1 for line in lines if "VNC_OK" in line)
    assert vnc_ok_count >= 5, f"Expected at least 5 'VNC_OK' lines in {uptime_log_path}, found {vnc_ok_count}."

def test_supervisor_log_started_format():
    supervisor_log_path = "/home/user/supervisor.log"
    assert os.path.isfile(supervisor_log_path), f"Supervisor log {supervisor_log_path} does not exist."

    with open(supervisor_log_path, "r") as f:
        content = f.read()

    qemu_started = "STARTED: qemu-system-x86_64 -display vnc=127.0.0.1:2 -nodefaults -no-reboot"
    monitor_started = "STARTED: python3 /home/user/monitor.py"

    assert qemu_started in content, f"Expected '{qemu_started}' in {supervisor_log_path}."
    assert monitor_started in content, f"Expected '{monitor_started}' in {supervisor_log_path}."