# test_final_state.py

import os
import socket
import pytest

def test_directories_and_symlinks():
    """Check that the required directories and symlinks are created correctly."""
    dirs_to_check = [
        "/home/user/var/log/finops",
        "/home/user/var/data/finops",
        "/home/user/finops"
    ]
    for d in dirs_to_check:
        assert os.path.isdir(d), f"Directory {d} does not exist."

    symlinks_to_check = {
        "/home/user/finops/logs": "/home/user/var/log/finops",
        "/home/user/finops/data": "/home/user/var/data/finops"
    }
    for link, target in symlinks_to_check.items():
        assert os.path.islink(link), f"{link} is not a symlink."
        assert os.readlink(link) == target, f"Symlink {link} does not point to {target}."

def test_scripts_exist_and_executable():
    """Check that the orchestrator and expect scripts exist and are executable."""
    scripts = [
        "/home/user/run_cost_analysis.sh",
        "/home/user/fetch_metrics.exp"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_log_file_content():
    """Check that the cost log file exists and contains the expected output."""
    log_file = "/home/user/finops/logs/cost.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist. Did the script run successfully?"

    with open(log_file, "r") as f:
        content = f.read()

    expected_string = 'COST_OPTS: {"spot": 0.04, "on_demand": 0.12}'
    assert expected_string in content, f"Log file does not contain the expected cost metrics. Found: {content}"

def test_port_8080_is_closed():
    """Check that no process is listening on port 8080 (cleanup was successful)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        # If connect succeeds, the port is still open
        s.connect(("127.0.0.1", 8080))
        port_open = True
    except (socket.timeout, ConnectionRefusedError):
        port_open = False
    finally:
        s.close()

    assert not port_open, "Port 8080 is still open. The background emulator process was not properly terminated."