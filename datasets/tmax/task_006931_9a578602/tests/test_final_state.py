# test_final_state.py

import os
import stat
import json
import socket
import threading
import subprocess
import time
import pytest

DEPLOY_SCRIPT = "/home/user/deploy.py"
CRON_FILE = "/home/user/schedule.cron"
STAGING_DIR = "/home/user/staging"
PRODUCTION_DIR = "/home/user/production"
BACKUP_DIR = "/home/user/backup"
LOG_FILE = "/home/user/deploy_log.json"

class DummySMTPServer(threading.Thread):
    def __init__(self, host='127.0.0.1', port=1025):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.received_data = ""
        self.running = True

    def run(self):
        self.server_socket.settimeout(1)
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with conn:
                conn.sendall(b"220 localhost ESMTP\r\n")
                while self.running:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.received_data += data.decode('utf-8', errors='ignore')
                        if b"QUIT" in data.upper():
                            conn.sendall(b"221 Bye\r\n")
                            break
                        elif b"DATA" in data.upper():
                            conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                        else:
                            conn.sendall(b"250 OK\r\n")
                    except Exception:
                        break

    def stop(self):
        self.running = False
        try:
            self.server_socket.close()
        except Exception:
            pass
        self.join()

def test_deploy_script_exists_and_executable():
    assert os.path.isfile(DEPLOY_SCRIPT), f"{DEPLOY_SCRIPT} does not exist."
    st = os.stat(DEPLOY_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{DEPLOY_SCRIPT} is not executable."

def test_cron_file_content():
    assert os.path.isfile(CRON_FILE), f"{CRON_FILE} does not exist."
    with open(CRON_FILE, "r") as f:
        content = f.read().strip()

    # Check for correct cron schedule
    assert "15 2 * * 0" in content, f"Cron expression '15 2 * * 0' not found in {CRON_FILE}."
    assert DEPLOY_SCRIPT in content, f"Script path {DEPLOY_SCRIPT} not found in {CRON_FILE}."

def test_deploy_script_execution_and_effects():
    # Setup SMTP server
    smtp_server = DummySMTPServer()
    smtp_server.start()

    try:
        # Give the server a moment to start
        time.sleep(0.5)

        # Execute the deployment script
        result = subprocess.run([DEPLOY_SCRIPT], capture_output=True, text=True)
        assert result.returncode == 0, f"Script exited with status {result.returncode}. Stderr: {result.stderr}"

        # 1. Check backup directory
        assert os.path.isdir(BACKUP_DIR), f"{BACKUP_DIR} was not created."
        assert os.path.isfile(os.path.join(BACKUP_DIR, "app_v1.py")), "app_v1.py was not moved to backup."
        assert not os.path.exists(os.path.join(PRODUCTION_DIR, "app_v1.py")), "app_v1.py was not removed from production."

        # 2. Check production directory
        assert os.path.isfile(os.path.join(PRODUCTION_DIR, "app_v2.py")), "app_v2.py was not copied to production."
        assert os.path.isfile(os.path.join(PRODUCTION_DIR, "config.yml")), "config.yml was not copied to production."

        # 3. Check deploy_log.json
        assert os.path.isfile(LOG_FILE), f"{LOG_FILE} was not created."
        with open(LOG_FILE, "r") as f:
            lines = f.read().strip().splitlines()
        assert len(lines) > 0, f"{LOG_FILE} is empty."

        last_line = lines[-1]
        try:
            log_data = json.loads(last_line)
        except json.JSONDecodeError:
            pytest.fail(f"Last line of {LOG_FILE} is not valid JSON.")

        assert log_data.get("status") == "success", "Log JSON 'status' is not 'success'."
        assert "files" in log_data, "Log JSON missing 'files' key."
        assert "app_v2.py" in log_data["files"], "app_v2.py not found in log 'files' list."
        assert "timestamp" in log_data, "Log JSON missing 'timestamp' key."
        assert isinstance(log_data["timestamp"], float), "Log JSON 'timestamp' is not a float."

        # 4. Check SMTP email
        email_data = smtp_server.received_data
        assert "deploy@company.local" in email_data, "Envelope sender 'deploy@company.local' not found in SMTP traffic."
        assert "eng-mailing-list@company.local" in email_data, "Recipient 'eng-mailing-list@company.local' not found in SMTP traffic."
        assert "Subject: Deployment Update" in email_data, "Email subject 'Deployment Update' not found."
        assert "New release deployed successfully." in email_data, "Email body not found in SMTP traffic."

    finally:
        smtp_server.stop()