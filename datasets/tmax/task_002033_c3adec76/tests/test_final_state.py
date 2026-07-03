# test_final_state.py

import os
import time
import signal
import subprocess

def test_alerter_compiled():
    """Verify that the alerter binary has been compiled and is executable."""
    path = "/home/user/alerter"
    assert os.path.isfile(path), f"{path} binary is missing. Did you compile alerter.rs?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_directory_and_symlink():
    """Verify the required directory structure and symlink."""
    release_dir = "/home/user/data/releases/v1"
    symlink_path = "/home/user/data/active"

    assert os.path.isdir(release_dir), f"Directory {release_dir} is missing."
    assert os.path.islink(symlink_path), f"{symlink_path} is missing or is not a symlink."

    target = os.readlink(symlink_path)
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), target))

    assert target == release_dir, f"Symlink points to {target}, expected {release_dir}."

def test_supervisor_script():
    """Verify that the supervisor script exists and is executable."""
    path = "/home/user/supervisor.sh"
    assert os.path.isfile(path), f"{path} is missing."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_supervisor_running():
    """Verify that the supervisor PID file exists and the process is running."""
    pid_file = "/home/user/supervisor.pid"
    assert os.path.isfile(pid_file), f"{pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'"
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Supervisor process {pid} is not running."

def get_alerter_pids():
    """Helper to get list of PIDs for 'alerter'."""
    try:
        output = subprocess.check_output(["pgrep", "-x", "alerter"]).decode().strip()
        return [int(x) for x in output.split() if x.isdigit()]
    except subprocess.CalledProcessError:
        return []

def test_alerter_restart_policy():
    """Verify that alerter is running and restarts automatically when killed."""
    pids = get_alerter_pids()
    assert len(pids) > 0, "alerter process is not running."

    target_pid = pids[0]

    # Kill the alerter process
    try:
        os.kill(target_pid, signal.SIGKILL)
    except OSError:
        pass

    # Give the supervisor time to detect and restart
    time.sleep(2.5)

    new_pids = get_alerter_pids()
    assert len(new_pids) > 0, "Alerter was not restarted by the supervisor after being killed!"
    assert target_pid not in new_pids, "Alerter PID didn't change; kill failed or it wasn't actually restarted."