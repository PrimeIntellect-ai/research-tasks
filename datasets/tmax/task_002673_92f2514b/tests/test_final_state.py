# test_final_state.py

import os
import stat
import subprocess
import socket
import time
import tarfile
import threading

def test_watchdog_files_exist():
    cpp_path = "/home/user/watchdog.cpp"
    exe_path = "/home/user/watchdog"

    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."
    assert os.path.isfile(exe_path), f"Executable file {exe_path} does not exist."

    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_path} is not executable."

def test_watchdog_service_down():
    exe_path = "/home/user/watchdog"
    alert_log = "/home/user/alert.log"
    backup_file = "/home/user/data_backup.tar.gz"

    # Ensure port 9090 is not listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    assert sock.connect_ex(('127.0.0.1', 9090)) != 0, "Port 9090 is unexpectedly open before the test."
    sock.close()

    # Clean up files if they exist from previous runs
    if os.path.exists(alert_log):
        os.remove(alert_log)
    if os.path.exists(backup_file):
        os.remove(backup_file)

    # Run the watchdog
    result = subprocess.run([exe_path], capture_output=True)

    assert result.returncode == 1, f"Expected exit code 1 when service is down, got {result.returncode}."

    assert os.path.isfile(alert_log), f"{alert_log} was not created."
    with open(alert_log, "r") as f:
        lines = f.readlines()
    assert len(lines) > 0, f"{alert_log} is empty."
    assert lines[-1] == "[ALERT] Port 9090 is unreachable\n", f"Incorrect log message in {alert_log}."

    assert os.path.isfile(backup_file), f"{backup_file} was not created."

    # Check if tar file is valid and contains metrics.txt
    try:
        with tarfile.open(backup_file, "r:gz") as tar:
            names = tar.getnames()
            # The archive should contain app_data/metrics.txt or similar path ending in metrics.txt
            found = any("app_data/metrics.txt" in name for name in names) or any("metrics.txt" in name for name in names)
            assert found, "Backup archive does not contain the expected metrics.txt file."
    except tarfile.TarError:
        assert False, f"{backup_file} is not a valid gzip-compressed tar archive."

def test_watchdog_service_up():
    exe_path = "/home/user/watchdog"
    alert_log = "/home/user/alert.log"
    backup_file = "/home/user/data_backup.tar.gz"

    # Clean up files
    if os.path.exists(alert_log):
        os.remove(alert_log)
    if os.path.exists(backup_file):
        os.remove(backup_file)

    # Start a dummy listener
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('127.0.0.1', 9090))
    server_sock.listen(1)

    stop_event = threading.Event()

    def accept_connections():
        server_sock.settimeout(0.5)
        while not stop_event.is_set():
            try:
                conn, addr = server_sock.accept()
                conn.close()
            except socket.timeout:
                continue
            except Exception:
                break

    t = threading.Thread(target=accept_connections)
    t.start()

    try:
        # Run the watchdog
        result = subprocess.run([exe_path], capture_output=True)

        assert result.returncode == 0, f"Expected exit code 0 when service is up, got {result.returncode}."
        assert not os.path.exists(alert_log), f"{alert_log} should not be created when service is up."
        assert not os.path.exists(backup_file), f"{backup_file} should not be created when service is up."
    finally:
        stop_event.set()
        t.join()
        server_sock.close()