# test_final_state.py

import os
import subprocess
import time
import pytest

def test_active_routes():
    active_routes_path = "/home/user/config/active_routes.txt"
    assert os.path.isfile(active_routes_path), f"File {active_routes_path} does not exist."

    with open(active_routes_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_routes = [
        "10.0.0.0 192.168.1.1 eth0",
        "192.168.2.0 0.0.0.0 tun1",
        "10.10.10.0 10.10.10.1 tun0"
    ]

    assert lines == expected_routes, f"Parsed routes in {active_routes_path} do not match the expected valid routes."

def test_log_rotator_behavior():
    rotator_script = "/home/user/scripts/log-rotator.sh"
    log_file = "/home/user/monitor/network.log"

    assert os.path.isfile(rotator_script), f"Script {rotator_script} does not exist."
    assert os.access(rotator_script, os.X_OK), f"Script {rotator_script} is not executable."

    # Helper to write lines
    def write_lines(n):
        with open(log_file, "w") as f:
            for i in range(n):
                f.write(f"Line {i}\n")

    # Clean up existing logs for a clean test
    for ext in ["", ".1", ".2", ".3", ".4"]:
        path = log_file + ext
        if os.path.exists(path):
            os.remove(path)

    # Test 1: 55 lines, should rotate
    write_lines(55)
    subprocess.run([rotator_script], check=True)

    assert os.path.getsize(log_file) == 0, "Original network.log was not truncated to 0 bytes."
    assert os.path.isfile(log_file + ".1"), "network.log.1 was not created."
    with open(log_file + ".1", "r") as f:
        assert len(f.readlines()) == 55, "network.log.1 does not contain the expected 55 lines."

    # Test 2: 52 lines, should rotate and shift
    write_lines(52)
    subprocess.run([rotator_script], check=True)

    assert os.path.getsize(log_file) == 0, "Original network.log was not truncated to 0 bytes."
    with open(log_file + ".1", "r") as f:
        assert len(f.readlines()) == 52, "network.log.1 does not contain the expected 52 lines."
    with open(log_file + ".2", "r") as f:
        assert len(f.readlines()) == 55, "network.log.2 does not contain the expected 55 lines."

    # Test 3: 51 lines, should rotate and shift
    write_lines(51)
    subprocess.run([rotator_script], check=True)

    assert os.path.getsize(log_file) == 0, "Original network.log was not truncated to 0 bytes."
    with open(log_file + ".1", "r") as f:
        assert len(f.readlines()) == 51, "network.log.1 does not contain the expected 51 lines."
    with open(log_file + ".3", "r") as f:
        assert len(f.readlines()) == 55, "network.log.3 does not contain the expected 55 lines."

    # Test 4: 53 lines, should rotate, shift, and drop .4
    write_lines(53)
    subprocess.run([rotator_script], check=True)

    assert os.path.getsize(log_file) == 0, "Original network.log was not truncated to 0 bytes."
    with open(log_file + ".1", "r") as f:
        assert len(f.readlines()) == 53, "network.log.1 does not contain the expected 53 lines."
    with open(log_file + ".3", "r") as f:
        assert len(f.readlines()) == 52, "network.log.3 does not contain the expected 52 lines."
    assert not os.path.exists(log_file + ".4"), "network.log.4 should not exist (only keep 3 old versions)."

def test_net_monitor_behavior():
    monitor_script = "/home/user/scripts/net-monitor.sh"

    assert os.path.isfile(monitor_script), f"Script {monitor_script} does not exist."
    assert os.access(monitor_script, os.X_OK), f"Script {monitor_script} is not executable."

    # Kill any existing dummy-service.sh and net-monitor.sh
    subprocess.run(["pkill", "-f", "dummy-service.sh"])
    subprocess.run(["pkill", "-f", "net-monitor.sh"])

    # Start net-monitor.sh in the background
    monitor_proc = subprocess.Popen([monitor_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for monitor to start the service
        time.sleep(2)

        # Check if dummy-service.sh is running
        pgrep = subprocess.run(["pgrep", "-f", "dummy-service.sh"], capture_output=True, text=True)
        assert pgrep.returncode == 0 and pgrep.stdout.strip() != "", "dummy-service.sh was not started by net-monitor.sh"

        # Kill it to see if it gets restarted
        subprocess.run(["pkill", "-f", "dummy-service.sh"])

        # Wait for monitor to restart the service
        time.sleep(2)

        pgrep = subprocess.run(["pgrep", "-f", "dummy-service.sh"], capture_output=True, text=True)
        assert pgrep.returncode == 0 and pgrep.stdout.strip() != "", "dummy-service.sh was not restarted by net-monitor.sh after being killed."

    finally:
        # Cleanup
        monitor_proc.terminate()
        monitor_proc.wait()
        subprocess.run(["pkill", "-f", "dummy-service.sh"])
        subprocess.run(["pkill", "-f", "net-monitor.sh"])