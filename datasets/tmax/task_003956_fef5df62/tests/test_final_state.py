# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_exporter_go_exists():
    assert os.path.isfile("/home/user/src/exporter.go"), "/home/user/src/exporter.go does not exist."

def test_deploy_script_idempotent():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

    # Run deploy.sh to check idempotency
    result = subprocess.run([deploy_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{deploy_script} failed on subsequent run (not idempotent). Error: {result.stderr}"

def test_exporter_binary_executable():
    binary_path = "/home/user/bin/exporter"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_metrics_directory_permissions():
    metrics_dir = "/home/user/metrics"
    assert os.path.isdir(metrics_dir), f"{metrics_dir} does not exist."

    mode = os.stat(metrics_dir).st_mode
    assert stat.S_IMODE(mode) == 0o700, f"Permissions for {metrics_dir} are not 700 (drwx------)."

def test_exporter_output_json():
    # Run the exporter manually to ensure output is generated properly based on current log
    binary_path = "/home/user/bin/exporter"
    result = subprocess.run([binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {binary_path} failed. Error: {result.stderr}"

    json_path = "/home/user/metrics/summary.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist after running exporter."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    # Calculate expected counts from requests.log
    log_path = "/home/user/data/requests.log"
    expected_counts = {}
    if os.path.isfile(log_path):
        with open(log_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    status = parts[1]
                    expected_counts[status] = expected_counts.get(status, 0) + 1

    # Convert keys to string for comparison, as JSON keys are always strings
    expected_counts_str = {str(k): int(v) for k, v in expected_counts.items()}
    data_str = {str(k): int(v) for k, v in data.items()}

    assert data_str == expected_counts_str, f"JSON output {data_str} does not match expected {expected_counts_str}."

def test_systemd_service_file():
    service_file = "/home/user/.config/systemd/user/exporter.service"
    assert os.path.isfile(service_file), f"{service_file} does not exist."

    with open(service_file, "r") as f:
        content = f.read()

    assert "Description=Custom Metrics Exporter" in content, f"Service file missing correct Description."
    assert "Type=oneshot" in content, f"Service file missing Type=oneshot."
    assert "ExecStart=/home/user/bin/exporter" in content, f"Service file missing correct ExecStart."

def test_systemd_timer_file():
    timer_file = "/home/user/.config/systemd/user/exporter.timer"
    assert os.path.isfile(timer_file), f"{timer_file} does not exist."

    with open(timer_file, "r") as f:
        content = f.read()

    assert "Description=Run Exporter Every Minute" in content, f"Timer file missing correct Description."
    assert "OnCalendar=*-*-* *:*:00" in content, f"Timer file missing correct OnCalendar."