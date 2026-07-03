# test_final_state.py

import os
import signal
import pytest

def test_symlink_correct():
    symlink_path = "/home/user/netmon/config/active.json"
    expected_target = "/home/user/netmon/config/available/production.json"

    assert os.path.islink(symlink_path), f"'{symlink_path}' is not a symlink."

    actual_target = os.readlink(symlink_path)
    # The symlink could be absolute or relative, but the instructions say to point it to the existing file.
    # We resolve it to absolute path to be robust.
    actual_target_abs = os.path.abspath(os.path.join(os.path.dirname(symlink_path), actual_target))
    expected_target_abs = os.path.abspath(expected_target)

    assert actual_target_abs == expected_target_abs, (
        f"Symlink points to '{actual_target}', expected it to point to '{expected_target}'."
    )

def test_autorestart_policy():
    conf_path = "/home/user/netmon/supervisor/conf.d/netmon.conf"
    assert os.path.isfile(conf_path), f"Configuration file '{conf_path}' is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "autorestart=true" in content.replace(" ", ""), (
        f"'autorestart=true' not found in '{conf_path}'. The service will not restart automatically."
    )

def test_connectivity_log_success():
    log_path = "/home/user/netmon/logs/connectivity.log"
    assert os.path.isfile(log_path), f"Log file '{log_path}' has not been created."

    with open(log_path, "r") as f:
        content = f.read()

    assert "STATUS: PING_SUCCESS" in content, (
        f"'STATUS: PING_SUCCESS' not found in '{log_path}'. The monitor script may not be running or the config is wrong."
    )

def test_supervisord_running():
    pid_path = "/home/user/netmon/run/supervisord.pid"
    assert os.path.isfile(pid_path), f"Supervisord PID file '{pid_path}' not found. Is supervisord running?"

    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file '{pid_path}' does not contain a valid PID."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Supervisord process with PID {pid} is not running.")