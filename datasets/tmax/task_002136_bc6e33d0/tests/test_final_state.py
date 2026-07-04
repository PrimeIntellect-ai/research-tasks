# test_final_state.py

import os
import time
import socket
import random
import subprocess
import pytest

def test_systemd_service_file():
    """Verify the systemd service file is created correctly."""
    service_path = "/home/user/.config/systemd/user/port-monitor.service"
    assert os.path.isfile(service_path), f"Service file {service_path} does not exist."

    with open(service_path, "r") as f:
        content = f.read()

    expected_exec = "ExecStart=/home/user/bin/port-monitor.sh /home/user/ports.txt /home/user/alerts.log"
    assert expected_exec in content, f"Service file missing expected ExecStart line. Found:\n{content}"

def test_script_installed_and_executable():
    """Verify the script was installed to the correct user bin directory and is executable."""
    script_path = "/home/user/bin/port-monitor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist. Did you modify the Makefile and run make install?"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_time_and_correctness():
    """Verify the optimized script detects correct ports and runs within the 1.5s threshold."""
    script_path = "/home/user/bin/port-monitor.sh"
    ports_file = "/home/user/test_ports.txt"
    log_file = "/home/user/test_alerts.log"

    open_ports = []
    sockets = []

    # Start 10 dummy listening sockets
    try:
        for _ in range(10):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', 0))
            s.listen(1)
            open_ports.append(s.getsockname()[1])
            sockets.append(s)

        # Generate 190 closed ports
        closed_ports = []
        while len(closed_ports) < 190:
            p = random.randint(20000, 60000)
            if p not in open_ports and p not in closed_ports:
                # Double check it is actually closed
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as check_sock:
                    if check_sock.connect_ex(('127.0.0.1', p)) != 0:
                        closed_ports.append(p)

        all_ports = open_ports + closed_ports
        random.shuffle(all_ports)

        with open(ports_file, "w") as f:
            for p in all_ports:
                f.write(f"{p}\n")

        # Remove old log if exists
        if os.path.exists(log_file):
            os.remove(log_file)

        start_time = time.time()
        proc = subprocess.run([script_path, ports_file, log_file], capture_output=True, text=True)
        duration = time.time() - start_time

        assert proc.returncode == 0, f"Script failed with return code {proc.returncode}. Stderr: {proc.stderr}"

        # Check output log
        assert os.path.isfile(log_file), f"Log file {log_file} was not created by the script."
        with open(log_file, "r") as f:
            lines = f.read().splitlines()

        reported_down = []
        for line in lines:
            if line.startswith("Port ") and line.endswith(" is DOWN"):
                try:
                    port_num = int(line.split()[1])
                    reported_down.append(port_num)
                except ValueError:
                    pass

        reported_down_set = set(reported_down)
        expected_down_set = set(closed_ports)

        missing = expected_down_set - reported_down_set
        extra = reported_down_set - expected_down_set

        assert not missing, f"Script failed to report these closed ports as DOWN: {missing}"
        assert not extra, f"Script incorrectly reported these open ports as DOWN: {extra}"

        assert duration <= 1.5, f"Execution time metric failed: duration was {duration:.2f}s, which is > 1.5s threshold."

    finally:
        for s in sockets:
            s.close()
        if os.path.exists(ports_file):
            os.remove(ports_file)
        if os.path.exists(log_file):
            os.remove(log_file)