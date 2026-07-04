# test_final_state.py

import os
import time
import subprocess
import pytest

def get_pids(process_name):
    try:
        output = subprocess.check_output(["pgrep", "-f", process_name]).decode("utf-8")
        return [int(pid) for pid in output.strip().split("\n") if pid]
    except subprocess.CalledProcessError:
        return []

def test_processes_running():
    socat_pids = get_pids("socat")
    assert len(socat_pids) > 0, "socat is not running. Did start_all.sh start it?"

    mock_smtp_pids = get_pids("mock_smtp.py")
    assert len(mock_smtp_pids) > 0, "mock_smtp.py is not running."

    supervisor_pids = get_pids("supervisor.sh")
    assert len(supervisor_pids) > 0, "supervisor.sh is not running."

    finops_pids = get_pids("finops_alert")
    assert len(finops_pids) > 0, "finops_alert is not running."

def test_alert_email_generation():
    usage_file = "/home/user/usage.csv"
    log_file = "/home/user/alert_emails.log"

    # Clear log file if it exists
    if os.path.exists(log_file):
        os.remove(log_file)

    # Write cost > 1000
    with open(usage_file, "w") as f:
        f.write("i-123,10,50.0\n")
        f.write("i-456,10,51.0\n")

    # Wait for the monitor to process (it reads every 2 seconds)
    time.sleep(3)

    assert os.path.exists(log_file), f"{log_file} was not created. The email was not sent or mock_smtp didn't receive it."

    with open(log_file, "r") as f:
        content = f.read()

    assert "Subject: Cost Alert" in content, "Email subject is incorrect or missing."
    assert "Total cost is $1010.00" in content, "Total cost calculation or formatting is incorrect."

def test_crash_and_restart():
    usage_file = "/home/user/usage.csv"

    initial_pids = get_pids("finops_alert")
    assert len(initial_pids) > 0, "finops_alert is not running before crash test."
    initial_pid = initial_pids[0]

    # Trigger crash
    with open(usage_file, "w") as f:
        f.write("CRASH_TEST,0,0\n")

    # Wait for crash and restart
    time.sleep(3)

    new_pids = get_pids("finops_alert")
    assert len(new_pids) > 0, "finops_alert did not restart after crashing."

    new_pid = new_pids[0]
    assert new_pid != initial_pid, "finops_alert PID did not change. It either didn't crash, or the supervisor didn't restart it properly."