# test_final_state.py

import os
import subprocess
import time
import pytest
import signal

def test_frontend_c_fixed():
    frontend_file = "/home/user/src/frontend.c"
    assert os.path.isfile(frontend_file), f"File {frontend_file} is missing."
    with open(frontend_file, "r") as f:
        content = f.read()

    assert "192.168.99.99" not in content, "frontend.c still contains the hardcoded IP '192.168.99.99'."
    assert "getenv(\"BACKEND_IP\")" in content, "frontend.c does not dynamically read BACKEND_IP using getenv."
    assert "getenv(\"BACKEND_PORT\")" in content, "frontend.c does not dynamically read BACKEND_PORT using getenv."

def test_binaries_compiled():
    backend_bin = "/home/user/bin/backend"
    frontend_bin = "/home/user/bin/frontend"
    assert os.path.isfile(backend_bin), f"Backend binary {backend_bin} is missing."
    assert os.access(backend_bin, os.X_OK), f"Backend binary {backend_bin} is not executable."
    assert os.path.isfile(frontend_bin), f"Frontend binary {frontend_bin} is missing."
    assert os.access(frontend_bin, os.X_OK), f"Frontend binary {frontend_bin} is not executable."

@pytest.fixture(scope="module")
def running_services():
    start_script = "/home/user/start_services.sh"
    assert os.path.isfile(start_script), f"Script {start_script} is missing."
    assert os.access(start_script, os.X_OK), f"Script {start_script} is not executable."

    # Run the start script
    subprocess.run(["bash", start_script], check=True)
    time.sleep(1) # Give services a moment to start

    backend_pid_file = "/home/user/run/backend.pid"
    frontend_pid_file = "/home/user/run/frontend.pid"

    assert os.path.isfile(backend_pid_file), f"PID file {backend_pid_file} is missing."
    assert os.path.isfile(frontend_pid_file), f"PID file {frontend_pid_file} is missing."

    with open(backend_pid_file, "r") as f:
        backend_pid = int(f.read().strip())
    with open(frontend_pid_file, "r") as f:
        frontend_pid = int(f.read().strip())

    yield

    # Cleanup
    for pid in [backend_pid, frontend_pid]:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass

def test_start_services(running_services):
    # This test just relies on the fixture successfully starting the services and finding the PID files
    pass

def test_monitor_script(running_services):
    monitor_script = "/home/user/monitor.sh"
    assert os.path.isfile(monitor_script), f"Script {monitor_script} is missing."
    assert os.access(monitor_script, os.X_OK), f"Script {monitor_script} is not executable."

    health_log = "/home/user/logs/health.log"
    if os.path.exists(health_log):
        os.remove(health_log)

    subprocess.run(["bash", monitor_script], check=True)

    assert os.path.isfile(health_log), f"Log file {health_log} was not created by monitor.sh."
    with open(health_log, "r") as f:
        content = f.read()

    assert "STATUS: HEALTHY" in content, f"Expected 'STATUS: HEALTHY' in {health_log}, but got:\n{content}"

def test_rotate_script():
    rotate_script = "/home/user/rotate.sh"
    assert os.path.isfile(rotate_script), f"Script {rotate_script} is missing."
    assert os.access(rotate_script, os.X_OK), f"Script {rotate_script} is not executable."

    health_log = "/home/user/logs/health.log"

    # Create a dummy health.log with 6 lines
    with open(health_log, "w") as f:
        for i in range(6):
            f.write(f"Dummy line {i}\n")

    subprocess.run(["bash", rotate_script], check=True)

    rotated_log = "/home/user/logs/health.log.1"
    assert os.path.isfile(rotated_log), f"Rotated log file {rotated_log} is missing."

    with open(rotated_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 6, f"Expected 6 lines in {rotated_log}, got {len(lines)}."

    assert os.path.isfile(health_log), f"New empty log file {health_log} is missing."
    with open(health_log, "r") as f:
        content = f.read()
    assert content == "", f"New {health_log} is not empty."