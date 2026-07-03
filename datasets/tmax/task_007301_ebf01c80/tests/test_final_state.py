# test_final_state.py

import os
import subprocess
import socket
import time
import threading

def test_backup_exists():
    """Verify that the backup of .bashrc exists."""
    backup_path = "/home/user/backups/bashrc.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

def test_bashrc_contains_env_var():
    """Verify that .bashrc contains the correct environment variable."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "SRE_MONITOR_PORT=5922" in content, f"{bashrc_path} does not set SRE_MONITOR_PORT=5922."

def test_executable_exists_and_executable():
    """Verify that the compiled executable exists and is executable."""
    exe_path = "/home/user/check_uptime"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_vnc_down_scenario():
    """Verify the executable correctly logs VNC_DOWN when the port is closed."""
    exe_path = "/home/user/check_uptime"
    log_path = "/home/user/sre_uptime.log"

    # Ensure port 5922 is closed (or at least attempt to)
    env = os.environ.copy()
    env["SRE_MONITOR_PORT"] = "5922"

    result = subprocess.run([exe_path], env=env, capture_output=True)
    assert result.returncode == 0, "check_uptime executable failed to run."

    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Log file is empty."
    assert "STATUS: VNC_DOWN" in lines[-1], "The last log entry should be 'STATUS: VNC_DOWN'."

def start_dummy_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(1)

    def accept_conn():
        try:
            conn, addr = server_socket.accept()
            conn.close()
        except:
            pass
        finally:
            server_socket.close()

    t = threading.Thread(target=accept_conn)
    t.daemon = True
    t.start()
    return server_socket

def test_vnc_up_scenario():
    """Verify the executable correctly logs VNC_UP when the port is open."""
    exe_path = "/home/user/check_uptime"
    log_path = "/home/user/sre_uptime.log"
    port = 5922

    server_socket = start_dummy_server(port)
    time.sleep(0.1) # Wait for server to start listening

    try:
        env = os.environ.copy()
        env["SRE_MONITOR_PORT"] = str(port)

        result = subprocess.run([exe_path], env=env, capture_output=True)
        assert result.returncode == 0, "check_uptime executable failed to run."

        assert os.path.isfile(log_path), f"Log file {log_path} was not created."

        with open(log_path, "r") as f:
            lines = f.readlines()

        assert len(lines) > 0, "Log file is empty."
        assert "STATUS: VNC_UP" in lines[-1], "The last log entry should be 'STATUS: VNC_UP'."
    finally:
        server_socket.close()