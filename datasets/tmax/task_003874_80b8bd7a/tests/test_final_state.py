# test_final_state.py
import os
import re
import socket

def test_server_executable_exists():
    """Check that /home/user/restore/server exists and is executable."""
    server_path = "/home/user/restore/server"
    assert os.path.isfile(server_path), f"Executable {server_path} does not exist."
    assert os.access(server_path, os.X_OK), f"File {server_path} is not executable."

def test_watchdog_script_exists():
    """Check that /home/user/watchdog.sh exists and is executable."""
    watchdog_path = "/home/user/watchdog.sh"
    assert os.path.isfile(watchdog_path), f"Watchdog script {watchdog_path} does not exist."
    assert os.access(watchdog_path, os.X_OK), f"Watchdog script {watchdog_path} is not executable."

def test_cron_txt_content():
    """Check that /home/user/cron.txt contains the correct 5-minute schedule."""
    cron_path = "/home/user/cron.txt"
    assert os.path.isfile(cron_path), f"Cron file {cron_path} does not exist."

    with open(cron_path, "r") as f:
        content = f.read()

    # Match patterns like "*/5 * * * * /home/user/watchdog.sh"
    # or "0,5,10... * * * * /home/user/watchdog.sh"
    pattern = r'^\s*(?:\*/5|0,5,10,15,20,25,30,35,40,45,50,55)\s+\*\s+\*\s+\*\s+\*\s+/home/user/watchdog\.sh'

    match = False
    for line in content.splitlines():
        if re.match(pattern, line):
            match = True
            break

    assert match, f"No valid 5-minute cron entry found for /home/user/watchdog.sh in {cron_path}"

def test_restore_status_log():
    """Check that the status log contains the exact success message."""
    log_path = "/home/user/restore_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "BACKUP_RESTORE_SUCCESSFUL" in content, f"Expected success message not found in {log_path}"

def test_server_listening():
    """Check that the server is actively listening on 127.0.0.1:8080 and responds correctly."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(("127.0.0.1", 8080))
        data = s.recv(1024)
        s.close()
        assert b"BACKUP_RESTORE_SUCCESSFUL" in data, "Server did not respond with the expected message."
    except ConnectionRefusedError:
        assert False, "Connection refused: Server is not listening on 127.0.0.1:8080."
    except socket.timeout:
        assert False, "Connection timed out: Server is not responding on 127.0.0.1:8080."
    except Exception as e:
        assert False, f"Failed to connect to server on 127.0.0.1:8080: {e}"