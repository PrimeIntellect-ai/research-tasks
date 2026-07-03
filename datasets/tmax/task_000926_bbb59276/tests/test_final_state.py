# test_final_state.py

import os
import time
import socket
import subprocess
import pytest

def test_files_exist():
    """Verify that the required Python scripts are created."""
    required_files = [
        "/home/user/watchdog.py",
        "/home/user/net_route.py",
        "/home/user/metric_exporter.py",
    ]
    for filepath in required_files:
        assert os.path.exists(filepath), f"Missing required file: {filepath}"
        assert os.path.isfile(filepath), f"Path is not a file: {filepath}"

def test_system_integration():
    """
    Run the user scripts, simulate time, trigger a crash, 
    and verify the resulting logs.
    """
    watchdog_proc = None
    net_route_proc = None
    metric_exporter_proc = None

    try:
        # Start watchdog
        watchdog_proc = subprocess.Popen(
            ["python3", "/home/user/watchdog.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait a moment for watchdog to start the daemon
        time.sleep(1)

        # Start net_route
        net_route_proc = subprocess.Popen(
            ["python3", "/home/user/net_route.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait a moment for net_route to bind
        time.sleep(1)

        # Start metric_exporter
        metric_exporter_proc = subprocess.Popen(
            ["python3", "/home/user/metric_exporter.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait 3 seconds to let observability.log populate
        time.sleep(3)

        # Send CRASH command through proxy
        try:
            with socket.create_connection(("127.0.0.1", 9025), timeout=2) as s:
                # Read banner
                s.recv(1024)
                # Send crash
                s.sendall(b"CRASH\r\n")
        except Exception as e:
            pytest.fail(f"Failed to connect to proxy or send CRASH command: {e}")

        # Wait 3 seconds to allow watchdog to restart daemon and metric exporter to log more
        time.sleep(3)

        # Verify watchdog.log
        watchdog_log_path = "/home/user/watchdog.log"
        assert os.path.exists(watchdog_log_path), "watchdog.log was not created."
        with open(watchdog_log_path, "r") as f:
            watchdog_content = f.read()

        assert "[SUPERVISOR] daemon restarted" in watchdog_content, \
            "watchdog.log does not contain the expected restart message."

        # Verify observability.log
        observability_log_path = "/home/user/observability.log"
        assert os.path.exists(observability_log_path), "observability.log was not created."
        with open(observability_log_path, "r") as f:
            observability_content = f.read()

        up_count = observability_content.count("email_service_up 1")
        assert up_count >= 3, \
            f"Expected at least 3 'email_service_up 1' in observability.log, found {up_count}."

    finally:
        # Cleanup processes
        for proc in [metric_exporter_proc, net_route_proc, watchdog_proc]:
            if proc is not None:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()

        # Also ensure mock_email_daemon is killed if watchdog orphaned it
        subprocess.run(["pkill", "-f", "mock_email_daemon.py"], capture_output=True)