# test_final_state.py

import os
import socket
import tarfile
import re

def test_directories_exist():
    """Check that the required directories were created."""
    directories = [
        "/home/user/alerts",
        "/home/user/backups",
        "/home/user/src",
        "/home/user/bin",
        "/home/user/certs"
    ]
    for d in directories:
        assert os.path.isdir(d), f"Directory {d} is missing."

def test_bashrc_env_vars():
    """Check that .bashrc contains the required environment variables."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} is missing."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert re.search(r"ALERT_DIR\s*=\s*['\"]?/home/user/alerts['\"]?", content), "ALERT_DIR is not correctly set in .bashrc"
    assert re.search(r"ALERT_PORT\s*=\s*['\"]?8080['\"]?", content), "ALERT_PORT is not correctly set in .bashrc"

def test_daemon_files_exist():
    """Check that the C source and compiled binary exist."""
    src_path = "/home/user/src/alert_daemon.c"
    bin_path = "/home/user/bin/alert_daemon"

    assert os.path.isfile(src_path), f"C source file {src_path} is missing."
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

def test_daemon_behavior():
    """Check that the daemon is running, accepts TRIGGER, and replies OK."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 8080))
        s.sendall(b"TRIGGER\n")
        data = s.recv(1024)
        s.close()
    except Exception as e:
        assert False, f"Failed to connect to daemon on port 8080 or send data: {e}"

    assert b"OK" in data, f"Daemon did not reply with OK, got: {data}"

def test_alerts_log_content():
    """Check that alerts.log contains the expected alert string."""
    log_path = "/home/user/alerts/alerts.log"
    assert os.path.isfile(log_path), f"Alert log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "ALERT_FIRED" in content, "alerts.log does not contain 'ALERT_FIRED'."

def test_tls_certs():
    """Check that the generated certificates exist and are basic PEM files."""
    crt_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.isfile(crt_path), f"Certificate {crt_path} is missing."
    assert os.path.isfile(key_path), f"Private key {key_path} is missing."

    with open(crt_path, "r") as f:
        crt_content = f.read()
    assert "BEGIN CERTIFICATE" in crt_content, f"{crt_path} does not look like a valid PEM certificate."

    with open(key_path, "r") as f:
        key_content = f.read()
    assert "PRIVATE KEY" in key_content, f"{key_path} does not look like a valid PEM private key."

def test_scripts_exist():
    """Check that the required shell scripts exist and are executable."""
    serve_script = "/home/user/serve_logs.sh"
    backup_script = "/home/user/backup.sh"

    assert os.path.isfile(serve_script), f"Script {serve_script} is missing."
    assert os.access(serve_script, os.X_OK), f"Script {serve_script} is not executable."

    assert os.path.isfile(backup_script), f"Script {backup_script} is missing."
    assert os.access(backup_script, os.X_OK), f"Script {backup_script} is not executable."

def test_backup_archive():
    """Check that the backup archive exists and contains alerts.log."""
    backup_path = "/home/user/backups/alerts_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            assert any("alerts.log" in name for name in names), "alerts.log is not present in the backup archive."
    except tarfile.TarError as e:
        assert False, f"Failed to read tar.gz archive {backup_path}: {e}"