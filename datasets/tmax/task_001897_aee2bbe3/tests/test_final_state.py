# test_final_state.py

import os
import stat
import subprocess
import re

def test_socket_exists_and_is_socket():
    """Verify that /home/user/migration/run/app.sock exists and is a socket."""
    sock_path = "/home/user/migration/run/app.sock"
    assert os.path.exists(sock_path), f"Verification failed: {sock_path} is missing."

    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"Verification failed: {sock_path} is not a socket."

def test_backend_server_running():
    """Verify that backend_server process is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "/home/user/migration/backend_server"], text=True)
        assert output.strip(), "Verification failed: backend_server process is not running."
    except subprocess.CalledProcessError:
        assert False, "Verification failed: backend_server process is not running."

def test_crontab_conf_correct():
    """Verify the cron config."""
    conf_path = "/home/user/migration/crontab.conf"
    assert os.path.isfile(conf_path), f"Verification failed: {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for * * * * * /home/user/migration/watchdog.sh
    # Allowing spaces/tabs and optional commands before the script
    pattern = r"^\s*\*\s+\*\s+\*\s+\*\s+\*.*\/home\/user\/migration\/watchdog\.sh"
    match = re.search(pattern, content, re.MULTILINE)
    assert match is not None, "Verification failed: crontab.conf does not contain the correct cron expression."

def test_watchdog_script_executable():
    """Verify watchdog script exists and is executable."""
    script_path = "/home/user/migration/watchdog.sh"
    assert os.path.isfile(script_path), f"Verification failed: {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Verification failed: {script_path} is not executable."

def test_backend_server_executable():
    """Verify backend_server executable exists."""
    exe_path = "/home/user/migration/backend_server"
    assert os.path.isfile(exe_path), f"Verification failed: {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"Verification failed: {exe_path} is not executable."