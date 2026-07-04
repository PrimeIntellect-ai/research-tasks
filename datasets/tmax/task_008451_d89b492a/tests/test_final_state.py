# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import glob
import tarfile
import re

MIGRATION_DIR = "/home/user/migration"

def test_directory_structure():
    """Check if the directory structure and symlinks are created correctly."""
    app_data_dir = os.path.join(MIGRATION_DIR, "app_data")
    active_apps_dir = os.path.join(MIGRATION_DIR, "active_apps")

    for i in range(1, 4):
        server_dir = os.path.join(app_data_dir, f"server{i}")
        assert os.path.isdir(server_dir), f"Directory {server_dir} does not exist."

        symlink_path = os.path.join(active_apps_dir, f"app{i}")
        assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

        target = os.readlink(symlink_path)
        # Handle both absolute and relative symlinks
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(active_apps_dir, target))
        assert target == server_dir, f"Symlink {symlink_path} does not point to {server_dir}."

def test_nginx_configuration():
    """Check if the Nginx configuration is valid and correctly set up for user space."""
    nginx_conf = os.path.join(MIGRATION_DIR, "nginx.conf")
    nginx_run = os.path.join(MIGRATION_DIR, "nginx_run")

    assert os.path.isfile(nginx_conf), f"Nginx configuration {nginx_conf} does not exist."
    assert os.path.isdir(nginx_run), f"Nginx run directory {nginx_run} does not exist."

    # Test Nginx syntax
    result = subprocess.run(["nginx", "-t", "-c", nginx_conf], capture_output=True, text=True)
    assert result.returncode == 0, f"Nginx configuration syntax check failed:\n{result.stderr}"

    # Dump configuration to verify directives
    result = subprocess.run(["nginx", "-T", "-c", nginx_conf], capture_output=True, text=True)
    config_output = result.stdout

    # Check for user space paths
    for directive in ["pid", "client_body_temp_path", "proxy_temp_path", 
                      "fastcgi_temp_path", "uwsgi_temp_path", "scgi_temp_path", 
                      "access_log", "error_log"]:
        assert f"{nginx_run}" in config_output, f"Directive {directive} does not seem to use {nginx_run}."

    # Check upstream block
    assert "upstream backend_cluster" in config_output, "Upstream block 'backend_cluster' not found."
    for port in [8081, 8082, 8083]:
        assert f"127.0.0.1:{port}" in config_output, f"Upstream server 127.0.0.1:{port} not found in config."

    # Check listen
    assert "listen 127.0.0.1:8080" in config_output or "listen 8080" in config_output, "Nginx is not configured to listen on 127.0.0.1:8080."

def start_dummy_server(port, stop_event):
    """Start a dummy socket server on the given port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        s.listen(1)
        s.settimeout(1.0)
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()
                conn.close()
            except socket.timeout:
                continue

def test_monitor_script_logic():
    """Test monitor.py logic by mocking listening ports."""
    monitor_script = os.path.join(MIGRATION_DIR, "monitor.py")
    log_file = os.path.join(MIGRATION_DIR, "logs", "monitor.log")
    backups_dir = os.path.join(MIGRATION_DIR, "backups")

    assert os.path.isfile(monitor_script), f"Monitor script {monitor_script} does not exist."

    stop_event = threading.Event()
    threads = []

    # Start listeners on 8081 and 8082, leave 8083 closed
    for port in [8081, 8082]:
        t = threading.Thread(target=start_dummy_server, args=(port, stop_event))
        t.start()
        threads.append(t)

    time.sleep(1) # wait for servers to start

    try:
        # Run monitor.py
        result = subprocess.run(["python3", monitor_script, "--check"], capture_output=True, text=True)
        assert result.returncode == 0 or result.returncode == 1, f"monitor.py failed to execute:\n{result.stderr}"

        # Check logs
        assert os.path.isfile(log_file), f"Log file {log_file} was not created."
        with open(log_file, "r") as f:
            logs = f.read()

        assert "ERROR - Backend port 8083 is down. Initiating backup." in logs, "Log did not contain the expected error message for port 8083."

        # Check backups
        assert os.path.isdir(backups_dir), f"Backups directory {backups_dir} was not created."
        backup_files = glob.glob(os.path.join(backups_dir, "apps_backup_*.tar.gz"))
        assert len(backup_files) >= 1, "No backup file found in backups directory."

        latest_backup = max(backup_files, key=os.path.getctime)

        # Verify tarball contents
        with tarfile.open(latest_backup, "r:gz") as tar:
            names = tar.getnames()
            # Ensure app1, app2, app3 are in the tarball
            found_apps = [name for name in names if "app1" in name or "app2" in name or "app3" in name]
            assert len(found_apps) >= 3, "Backup tarball does not contain the active_apps symlinks."

    finally:
        stop_event.set()
        for t in threads:
            t.join()