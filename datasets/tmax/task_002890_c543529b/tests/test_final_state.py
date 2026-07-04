# test_final_state.py

import os
import subprocess
import pytest

def test_filter_script_behavior():
    """Verify that the deploy_filter.py correctly classifies all clean and evil files."""
    filter_script = "/home/user/deploy_filter.py"
    assert os.path.isfile(filter_script), f"Filter script missing: {filter_script}"

    clean_dir = "/home/user/configs/clean"
    evil_dir = "/home/user/configs/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run(["python3", filter_script, cf], capture_output=True, text=True)
        if result.stdout.strip() != "ACCEPT":
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run(["python3", filter_script, ef], capture_output=True, text=True)
        if result.stdout.strip() != "REJECT":
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_integration_script_effects():
    """Verify that apply_config.sh created the required directory, config, and daemon."""
    service_dir = "/home/user/deploy_service/"
    config_file = "/home/user/deploy_service/config.ini"
    pid_file = "/home/user/deploy_service/daemon.pid"

    assert os.path.isdir(service_dir), f"Service directory missing: {service_dir}"
    assert os.path.isfile(config_file), f"Config file missing: {config_file}"

    with open(config_file, "r") as f:
        content = f.read()

    assert "PreflightFilter=/home/user/deploy_filter.py" in content, "PreflightFilter not found in config.ini"

    assert os.path.isfile(pid_file), f"PID file missing: {pid_file}"
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid PID: {pid_str}"

    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Daemon process with PID {pid} is not running")