# test_final_state.py

import os
import json
import pwd
import subprocess

def test_health_monitor_script_exists_and_executable():
    script_path = "/home/user/health_monitor.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    with open(script_path, "r") as f:
        first_line = f.readline().strip()
    assert first_line == "#!/usr/bin/env python3", f"Script does not have correct shebang, found: {first_line}"

def test_health_json_exists_and_valid():
    log_path = "/home/user/logs/health.json"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"

    with open(log_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {log_path} is not valid JSON"

    assert "data_size_bytes" in data, "Missing 'data_size_bytes' in JSON"
    assert "worker_count" in data, "Missing 'worker_count' in JSON"
    assert "deploy_user_exists" in data, "Missing 'deploy_user_exists' in JSON"

def test_health_json_values():
    log_path = "/home/user/logs/health.json"
    with open(log_path, "r") as f:
        data = json.load(f)

    # Recompute data_size_bytes
    total_size = 0
    app_data_dir = "/home/user/app_data"
    for root, dirs, files in os.walk(app_data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)

    assert data["data_size_bytes"] == total_size, f"Expected data_size_bytes to be {total_size}, but got {data['data_size_bytes']}"

    # Recompute worker_count
    try:
        ps_output = subprocess.check_output(["ps", "aux"], text=True)
        worker_count = sum(1 for line in ps_output.strip().split('\n') if "background_worker.sh" in line and "grep" not in line)
    except subprocess.CalledProcessError:
        worker_count = 0

    assert data["worker_count"] == worker_count, f"Expected worker_count to be {worker_count}, but got {data['worker_count']}"

    # Recompute deploy_user_exists
    try:
        pwd.getpwnam("deploy_user")
        user_exists = True
    except KeyError:
        user_exists = False

    assert data["deploy_user_exists"] == user_exists, f"Expected deploy_user_exists to be {user_exists}, but got {data['deploy_user_exists']}"