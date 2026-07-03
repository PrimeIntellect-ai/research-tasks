# test_final_state.py

import os
import subprocess
import time
import pytest

def test_worker_script_fixed():
    worker_path = "/home/user/worker.sh"
    assert os.path.exists(worker_path), f"{worker_path} not found."
    with open(worker_path, "r") as f:
        content = f.read()

    assert "/var/log/worker.log" not in content, "worker.sh still contains the invalid log path /var/log/worker.log."
    assert "/home/user/worker.log" in content, "worker.sh does not contain the correct log path /home/user/worker.log."
    assert "8000" not in content, "worker.sh still contains the incorrect port 8000."
    assert "8080" in content, "worker.sh does not contain the correct port 8080."

def test_health_script_executable():
    health_path = "/home/user/health.sh"
    assert os.path.exists(health_path), f"{health_path} not found."
    assert os.access(health_path, os.X_OK), f"{health_path} is not executable."

def test_health_script_logic():
    health_path = "/home/user/health.sh"
    log_path = "/home/user/health.log"
    worker_path = "/home/user/worker.sh"

    # Ensure worker.sh is not running
    subprocess.run(["pkill", "-f", "worker.sh"])
    time.sleep(0.5)

    # Run health.sh
    subprocess.run([health_path], check=False)

    assert os.path.exists(log_path), f"{log_path} was not created by health.sh."
    with open(log_path, "r") as f:
        lines = f.read().splitlines()
    assert len(lines) > 0, f"{log_path} is empty."
    assert lines[-1] == "FAIL", f"Expected the last line of {log_path} to be 'FAIL' when worker is not running, got '{lines[-1]}'."

    # Start worker.sh in the background
    worker_proc = subprocess.Popen([worker_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) # Give it a moment to start

    try:
        # Run health.sh again
        subprocess.run([health_path], check=False)
        with open(log_path, "r") as f:
            lines = f.read().splitlines()
        assert lines[-1] == "OK", f"Expected the last line of {log_path} to be 'OK' when worker is running, got '{lines[-1]}'."
    finally:
        # Cleanup
        worker_proc.terminate()
        worker_proc.wait(timeout=2)
        subprocess.run(["pkill", "-f", "worker.sh"])

def test_cron_job_installed():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab or crontab is empty."

    cron_lines = [line.strip() for line in result.stdout.splitlines() if line.strip() and not line.strip().startswith("#")]
    found = False
    for line in cron_lines:
        if "/home/user/health.sh" in line:
            parts = line.split()
            # Check if it runs every minute
            if len(parts) >= 6 and parts[:5] == ["*", "*", "*", "*", "*"]:
                found = True
                break

    assert found, "Cron job for /home/user/health.sh to run every minute (* * * * *) not found."