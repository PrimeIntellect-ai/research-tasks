# test_final_state.py

import os
import subprocess
import time
import pytest

def test_proxy_running():
    """Verify that socat is running and its PID is stored correctly."""
    pid_file = "/home/user/proxy.pid"
    assert os.path.exists(pid_file), f"Proxy PID file missing at {pid_file}"

    with open(pid_file, "r") as f:
        pid = f.read().strip()

    assert pid.isdigit(), f"PID file does not contain a valid integer: '{pid}'"

    try:
        cmd = ["ps", "-p", pid, "-o", "comm="]
        output = subprocess.check_output(cmd, text=True).strip()
        assert "socat" in output, f"Process {pid} is not socat, it is '{output}'"
    except subprocess.CalledProcessError:
        pytest.fail(f"Process with PID {pid} is not running")

def test_logrotate_config():
    """Verify the logrotate configuration contains the required directives."""
    conf_file = "/home/user/logrotate.conf"
    assert os.path.exists(conf_file), f"logrotate config missing at {conf_file}"

    with open(conf_file, "r") as f:
        content = f.read()

    assert "rotate 5" in content, "logrotate.conf missing 'rotate 5'"
    assert "daily" in content, "logrotate.conf missing 'daily'"
    assert "compress" in content, "logrotate.conf missing 'compress'"
    assert "missingok" in content, "logrotate.conf missing 'missingok'"
    assert "/home/user/logs/telemetry.log" in content, "logrotate.conf does not reference the correct log file path"

def test_git_hook_and_log():
    """Verify the post-receive hook exists, is executable, and the log contains the expected output."""
    log_file = "/home/user/logs/telemetry.log"
    assert os.path.exists(log_file), f"Log file missing at {log_file}"

    with open(log_file, "r") as f:
        content = f.read()

    # The script should have outputted 45 to the log file via the hook
    assert "45" in content, f"telemetry.log does not contain the expected output '45'. Content: {content}"

    hook_file = "/home/user/telemetry.git/hooks/post-receive"
    assert os.path.exists(hook_file), f"post-receive hook missing at {hook_file}"
    assert os.access(hook_file, os.X_OK), "post-receive hook is not executable"

def test_analyze_script_metric():
    """Verify the correctness and performance of the analyze.py script."""
    script_path = "/home/user/deploy/analyze.py"
    assert os.path.exists(script_path), f"analyze.py missing at {script_path}"

    video_path = "/app/telemetry.mp4"
    assert os.path.exists(video_path), f"Video fixture missing at {video_path}"

    start_time = time.time()
    try:
        proc = subprocess.run(["python3", script_path, video_path], capture_output=True, text=True, timeout=5.0)
    except subprocess.TimeoutExpired:
        pytest.fail("analyze.py took longer than 5.0 seconds to execute, well above the 1.5s threshold")

    duration = time.time() - start_time

    try:
        count = int(proc.stdout.strip())
    except ValueError:
        pytest.fail(f"analyze.py did not output a valid integer. Output: '{proc.stdout.strip()}'")

    assert count == 45, f"FAILED: Expected 45 red frames, got {count}"
    assert duration <= 1.5, f"Execution time {duration:.3f}s exceeded the 1.5s threshold"