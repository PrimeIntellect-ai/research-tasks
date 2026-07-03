# test_final_state.py

import os
import subprocess
import time
import signal
import pytest

PROVISION_SCRIPT = "/home/user/provision.sh"
HEALTH_SCRIPT = "/home/user/check_health.sh"
ENV_FILE = "/home/user/service.env"
PID_FILE = "/home/user/app.pid"
LOG_FILE = "/home/user/app.log"

def test_scripts_exist_and_executable():
    assert os.path.isfile(PROVISION_SCRIPT), f"{PROVISION_SCRIPT} does not exist."
    assert os.access(PROVISION_SCRIPT, os.X_OK), f"{PROVISION_SCRIPT} is not executable."

    assert os.path.isfile(HEALTH_SCRIPT), f"{HEALTH_SCRIPT} does not exist."
    assert os.access(HEALTH_SCRIPT, os.X_OK), f"{HEALTH_SCRIPT} is not executable."

def test_provision_script_behavior():
    # Run provision.sh
    result = subprocess.run([PROVISION_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{PROVISION_SCRIPT} did not exit cleanly. stderr: {result.stderr}"

    # Check service.env
    assert os.path.isfile(ENV_FILE), f"{ENV_FILE} was not created."
    with open(ENV_FILE, "r") as f:
        env_contents = f.read().splitlines()

    assert "TZ=Pacific/Fiji" in env_contents, f"TZ not correctly set in {ENV_FILE}"
    assert "LC_ALL=en_NZ.UTF-8" in env_contents, f"LC_ALL not correctly set in {ENV_FILE}"

    # Check app.pid
    assert os.path.isfile(PID_FILE), f"{PID_FILE} was not created."
    with open(PID_FILE, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"{PID_FILE} does not contain a valid PID."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

    # Wait for the app to write to the log
    time.sleep(2)

    # Check app.log
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} was not created."

def test_check_health_script_healthy():
    # Run check_health.sh while app is healthy
    result = subprocess.run([HEALTH_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{HEALTH_SCRIPT} failed to run."
    output = result.stdout.strip()
    assert output == "HEALTHY", f"Expected 'HEALTHY' but got '{output}'"

def test_check_health_script_unhealthy():
    # Read PID and kill process
    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass # Process already dead

    time.sleep(1) # Wait for process to fully terminate

    # Run check_health.sh while app is dead
    result = subprocess.run([HEALTH_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{HEALTH_SCRIPT} failed to run."
    output = result.stdout.strip()
    assert output == "UNHEALTHY", f"Expected 'UNHEALTHY' but got '{output}'"

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    # Cleanup any lingering processes
    if os.path.isfile(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGKILL)
        except Exception:
            pass