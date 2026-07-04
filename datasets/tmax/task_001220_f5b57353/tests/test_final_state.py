# test_final_state.py
import os
import socket
import stat
import time
import pytest

def test_daemon_listening_and_restore():
    """Test if the daemon is listening on 9090, handles the RESTORE command, and returns SUCCESS."""
    host = '127.0.0.1'
    port = 9090

    # Try to connect and send the command
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect((host, port))
        except (ConnectionRefusedError, socket.timeout):
            pytest.fail("Daemon is not listening on 127.0.0.1:9090")

        s.sendall(b"RESTORE v1.0\n")

        try:
            response = s.recv(1024).decode('utf-8')
        except socket.timeout:
            pytest.fail("Timeout waiting for response from daemon")

        assert "SUCCESS" in response, f"Expected 'SUCCESS' in response, got: {response}"

def test_extracted_files_and_permissions():
    """Test if the files were extracted and permissions set correctly."""
    app_bin_path = '/home/user/restore_deploy/app.bin'
    config_json_path = '/home/user/restore_deploy/config.json'

    # Allow some time for the daemon to finish extraction if async
    time.sleep(1)

    assert os.path.exists(app_bin_path), f"{app_bin_path} does not exist"
    assert os.path.exists(config_json_path), f"{config_json_path} does not exist"

    app_bin_stat = os.stat(app_bin_path)
    config_json_stat = os.stat(config_json_path)

    # Check permissions 0750 for app.bin
    assert stat.S_IMODE(app_bin_stat.st_mode) == 0o750, f"Permissions for {app_bin_path} are not 0750"

    # Check permissions 0600 for config.json
    assert stat.S_IMODE(config_json_stat.st_mode) == 0o600, f"Permissions for {config_json_path} are not 0600"

def test_smtp_notification():
    """Test if the SMTP notification was sent."""
    mail_log_path = '/home/user/mail.log'

    # Allow some time for the mail log to be written
    time.sleep(1)

    assert os.path.exists(mail_log_path), f"{mail_log_path} does not exist"

    with open(mail_log_path, 'r') as f:
        content = f.read()

    assert "Subject: Restore v1.0 complete" in content, "Subject not found in mail log"
    assert "operator@backup.local" in content, "Recipient not found in mail log"