# test_final_state.py
import os
import time
import json
import signal
import subprocess
import pytest

def test_deployment_report():
    report_path = "/home/user/deployment_report.txt"
    assert os.path.exists(report_path), f"{report_path} does not exist"

    with open(report_path, "r") as f:
        content = f.read().strip().split('\n')

    expected_lines = [
        "BINARY_PATH=/home/user/iot_aggregator/target/release/iot_aggregator",
        "SUPERVISOR_PATH=/home/user/supervisor.sh",
        "PID_FILE=/home/user/run/aggregator.pid"
    ]

    for expected in expected_lines:
        assert expected in content, f"Expected '{expected}' in deployment_report.txt"

def test_supervisor_executable():
    supervisor_path = "/home/user/supervisor.sh"
    assert os.path.exists(supervisor_path), f"{supervisor_path} does not exist"
    assert os.access(supervisor_path, os.X_OK), f"{supervisor_path} is not executable"

def test_aggregator_lifecycle():
    supervisor_path = "/home/user/supervisor.sh"
    pid_file = "/home/user/run/aggregator.pid"
    sensor_dir = "/home/user/sensor_data"
    metrics_dir = "/home/user/metrics"
    log_file = os.path.join(sensor_dir, "log1.log")
    symlink_file = os.path.join(sensor_dir, "latest.log")
    current_json = os.path.join(metrics_dir, "current.json")
    state_json = os.path.join(metrics_dir, "state.json")

    # Start supervisor
    supervisor_proc = subprocess.Popen([supervisor_path], preexec_fn=os.setsid)

    try:
        # Wait for PID file to be created
        pid = None
        for _ in range(10):
            if os.path.exists(pid_file):
                with open(pid_file, "r") as f:
                    pid_str = f.read().strip()
                    if pid_str.isdigit():
                        pid = int(pid_str)
                        break
            time.sleep(0.5)

        assert pid is not None, "PID file was not created or does not contain a valid PID"

        # Create log file and symlink
        os.makedirs(sensor_dir, exist_ok=True)
        with open(log_file, "w") as f:
            pass

        if os.path.exists(symlink_file):
            os.remove(symlink_file)
        os.symlink(log_file, symlink_file)

        # Append logs
        logs = [
            "[2023-10-25T10:00:00Z] sensor=A1 temp=20.5C humidity=40% status=OK\n",
            "[2023-10-25T10:00:01Z] sensor=A1 temp=99.9C humidity=99% status=ERROR\n",
            "[2023-10-25T10:00:02Z] sensor=A1 temp=21.0C humidity=42% status=OK\n"
        ]

        with open(log_file, "a") as f:
            for line in logs:
                f.write(line)
                f.flush()
                time.sleep(0.5)

        # Give it a moment to process
        time.sleep(1)

        # Check current.json
        assert os.path.exists(current_json), f"{current_json} does not exist"
        with open(current_json, "r") as f:
            data = json.load(f)

        assert data.get("latest_temp") == 21.0, f"Expected latest_temp=21.0, got {data.get('latest_temp')}"
        assert data.get("latest_humidity") == 42.0, f"Expected latest_humidity=42.0, got {data.get('latest_humidity')}"
        assert data.get("valid_readings_count") == 2, f"Expected valid_readings_count=2, got {data.get('valid_readings_count')}"

        # Send SIGTERM to aggregator
        os.kill(pid, signal.SIGTERM)
        time.sleep(2)

        # Check state.json
        assert os.path.exists(state_json), f"{state_json} does not exist"
        with open(state_json, "r") as f:
            state_data = json.load(f)

        assert state_data.get("status") == "shutting_down", f"Expected status='shutting_down', got {state_data.get('status')}"

        # Check process exited
        try:
            os.kill(pid, 0)
            pytest.fail(f"Process {pid} did not exit after SIGTERM")
        except OSError:
            pass # Process is gone, which is expected

    finally:
        # Clean up supervisor
        try:
            os.killpg(os.getpgid(supervisor_proc.pid), signal.SIGKILL)
        except OSError:
            pass