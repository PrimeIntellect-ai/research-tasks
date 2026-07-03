# test_final_state.py

import os
import subprocess
import pytest

SERVICES_DIR = '/home/user/services'

def test_health_check_script_exists():
    """Check that health_check.py exists."""
    path = os.path.join(SERVICES_DIR, 'health_check.py')
    assert os.path.isfile(path), f"{path} is missing."

def test_log_monitor_script_exists():
    """Check that log_monitor.sh exists."""
    path = os.path.join(SERVICES_DIR, 'log_monitor.sh')
    assert os.path.isfile(path), f"{path} is missing."

def test_run_pid_file():
    """Check that run.pid exists and contains exactly two lines (PIDs)."""
    pid_file = os.path.join(SERVICES_DIR, 'run.pid')
    assert os.path.isfile(pid_file), f"{pid_file} is missing."

    with open(pid_file, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"{pid_file} should contain exactly two lines (PIDs), found {len(lines)}."
    for line in lines:
        assert line.strip().isdigit(), f"Expected PID to be numeric, got '{line}' in {pid_file}."

def test_processes_running():
    """Check that both producer.py and consumer.py are running."""
    try:
        output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute 'ps aux'")

    producer_running = 'producer.py' in output
    consumer_running = 'consumer.py' in output

    assert producer_running, "producer.py is not running."
    assert consumer_running, "consumer.py is not running. It may have crashed due to dependency failure."

def test_consumer_success_flag():
    """Check that consumer_success.flag exists and contains 'OK'."""
    flag_file = os.path.join(SERVICES_DIR, 'consumer_success.flag')
    assert os.path.isfile(flag_file), f"{flag_file} is missing. Consumer did not successfully connect to producer."

    with open(flag_file, 'r') as f:
        content = f.read().strip()

    assert content == "OK", f"Expected 'OK' in {flag_file}, found '{content}'."

def test_critical_codes_file():
    """Check that critical_codes.txt exists and contains the correct critical codes."""
    codes_file = os.path.join(SERVICES_DIR, 'critical_codes.txt')
    assert os.path.isfile(codes_file), f"{codes_file} is missing."

    with open(codes_file, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_codes = ["CRIT_992", "CRIT_105"]
    assert lines == expected_codes, f"Expected critical codes {expected_codes}, found {lines}."