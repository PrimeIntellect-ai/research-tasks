# test_final_state.py
import os
import re
import socket
import pytest

def test_port_forwarding():
    """Verify that port 8080 is listening and forwards to the legacy daemon."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('127.0.0.1', 8080))
        data = s.recv(1024)
        assert b"Username: " in data, "Port 8080 is open but did not return the expected legacy daemon prompt."
    except ConnectionRefusedError:
        pytest.fail("Port 8080 is not listening. Port forwarding is not set up.")
    except socket.timeout:
        pytest.fail("Connection to port 8080 timed out.")
    finally:
        s.close()

def test_expect_script_exists():
    """Verify the expect script exists."""
    path = "/home/user/fetch_stats.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."

def test_collect_metrics_script_exists_and_executable():
    """Verify the collect metrics script exists and is executable."""
    path = "/home/user/collect_metrics.sh"
    assert os.path.isfile(path), f"Bash script {path} does not exist."
    assert os.access(path, os.X_OK), f"Bash script {path} is not executable."

def test_metrics_csv_content():
    """Verify metrics.csv exists, has exactly one line, and matches the expected format."""
    path = "/home/user/metrics.csv"
    assert os.path.isfile(path), f"Metrics file {path} does not exist."

    with open(path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 1, f"Expected exactly 1 line in {path}, found {len(lines)}."

    line = lines[0]
    parts = line.split(",")
    assert len(parts) == 5, f"Expected 5 comma-separated values, found {len(parts)} in line: {line}"

    timestamp, connections, bandwidth, cpu, mem = parts

    # Validate timestamp
    assert timestamp.isdigit(), f"Timestamp '{timestamp}' is not a valid integer."

    # Validate connections and bandwidth (based on the setup script's hardcoded values)
    assert connections == "404", f"Expected connections to be '404', got '{connections}'."
    assert bandwidth == "120", f"Expected bandwidth to be '120', got '{bandwidth}'."

    # Validate CPU and MEM are numeric (floats or ints)
    def is_numeric(val):
        try:
            float(val)
            return True
        except ValueError:
            return False

    assert is_numeric(cpu), f"CPU percent '{cpu}' is not a valid number."
    assert is_numeric(mem), f"Memory percent '{mem}' is not a valid number."