# test_final_state.py

import os
import pytest

def test_check_ports_executable():
    filepath = "/home/user/netmon/check_ports"
    assert os.path.isfile(filepath), f"{filepath} does not exist. Did you compile the C program?"
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable."

def test_trigger_alert_executable():
    filepath = "/home/user/netmon/trigger_alert.sh"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable."

def test_netmon_init_executable():
    filepath = "/home/user/netmon/netmon-init.sh"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable."

def test_alerts_log_contents():
    filepath = "/home/user/netmon/alerts.log"
    assert os.path.isfile(filepath), f"{filepath} does not exist. Did the service run?"

    with open(filepath, "r") as f:
        content = f.read()

    assert "ALERT: Service for [bob] on port [8082] is unreachable!" in content, \
        "Expected alert for bob on port 8082 not found in alerts.log."

    assert "ALERT: Service for [alice] on port [8084] is unreachable!" in content, \
        "Expected alert for alice on port 8084 not found in alerts.log."

    assert "charlie" not in content, \
        "Alert for charlie found in alerts.log, but charlie is not in valid_users.txt."

    assert "8081" not in content, \
        "Alert for port 8081 found in alerts.log, but port 8081 should be up."

def test_pid_file_removed():
    # The task says to stop the service, which should remove the pid file.
    pid_file = "/home/user/netmon/netmon.pid"
    assert not os.path.exists(pid_file), f"PID file {pid_file} still exists. Did you properly stop the service?"