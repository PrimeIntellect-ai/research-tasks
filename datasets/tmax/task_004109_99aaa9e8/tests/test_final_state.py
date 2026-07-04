# test_final_state.py
import os
import subprocess
import time
import threading
import http.server
import socketserver
import pytest

APP_DIR = "/home/user/app"
BACKUP_FILE = os.path.join(APP_DIR, "backups", "start_services.sh.bak")
START_SCRIPT = os.path.join(APP_DIR, "start_services.sh")
HEALTH_CHECK_SCRIPT = os.path.join(APP_DIR, "health_check.py")
LOG_DIR = os.path.join(APP_DIR, "logs")
HEALTH_LOG = os.path.join(LOG_DIR, "health.log")

def test_backup_exists():
    assert os.path.isfile(BACKUP_FILE), f"Backup file not found at {BACKUP_FILE}"
    with open(BACKUP_FILE, "r") as f:
        content = f.read()
    assert "data_initializer.py" in content, "Backup file does not look like the original script."

def test_start_services_fixed():
    assert os.path.isfile(START_SCRIPT), f"Script not found at {START_SCRIPT}"
    assert os.access(START_SCRIPT, os.X_OK), f"Script {START_SCRIPT} is not executable"

    with open(START_SCRIPT, "r") as f:
        content = f.read()

    # It should check for shared_data.json before starting backend_api.py
    assert "shared_data.json" in content, "start_services.sh does not seem to check for shared_data.json"
    # It should have some form of loop/sleep to wait
    assert "sleep" in content or "inotifywait" in content, "start_services.sh does not seem to wait/sleep for the file"

def test_health_check_script_functionality():
    assert os.path.isfile(HEALTH_CHECK_SCRIPT), f"Health check script not found at {HEALTH_CHECK_SCRIPT}"

    # Ensure log dir exists or the script creates it
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if os.path.exists(HEALTH_LOG):
        os.remove(HEALTH_LOG)

    # Run health check when service is DOWN
    subprocess.run(["python3", HEALTH_CHECK_SCRIPT], capture_output=True)

    assert os.path.isfile(HEALTH_LOG), f"Log file not created at {HEALTH_LOG}"
    with open(HEALTH_LOG, "r") as f:
        logs = f.readlines()

    assert len(logs) >= 1, "No logs written when service is down"
    assert "[ERROR] Service unreachable or failing" in logs[-1], "Incorrect error log message"

    # Run health check when service is UP
    class DummyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/status':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            else:
                self.send_response(404)
                self.end_headers()
        def log_message(self, format, *args):
            pass

    httpd = socketserver.TCPServer(("127.0.0.1", 8080), DummyHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        time.sleep(0.5)
        subprocess.run(["python3", HEALTH_CHECK_SCRIPT], capture_output=True)

        with open(HEALTH_LOG, "r") as f:
            logs = f.readlines()

        assert len(logs) >= 2, "No new logs written when service is up"
        assert "[OK] Service healthy" in logs[-1], "Incorrect success log message"
    finally:
        httpd.shutdown()
        httpd.server_close()
        server_thread.join(timeout=1)

def test_crontab_entry():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab"
    cron_jobs = result.stdout
    assert "health_check.py" in cron_jobs, "No crontab entry found for health_check.py"
    assert "* * * * *" in cron_jobs, "Crontab entry is not set to run every minute (* * * * *)"
    assert "/usr/bin/python3" in cron_jobs, "Crontab entry does not use /usr/bin/python3"