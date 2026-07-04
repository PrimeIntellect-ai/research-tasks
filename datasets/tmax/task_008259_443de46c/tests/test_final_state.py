# test_final_state.py

import os
import stat
import subprocess
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def test_script_permissions():
    script_path = "/home/user/uptime_monitor.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o700, f"Expected {script_path} to have permissions 0700, but got {oct(permissions)}"

def test_log_permissions():
    log_path = "/home/user/service_status.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    st = os.stat(log_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Expected {log_path} to have permissions 0600, but got {oct(permissions)}"

def test_cron_job():
    try:
        crontab_output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError:
        crontab_output = ""

    # Check if the script is scheduled to run every minute
    lines = crontab_output.strip().split('\n')
    found = False
    for line in lines:
        if line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) >= 6:
            schedule = parts[:5]
            command = " ".join(parts[5:])
            if schedule == ['*', '*', '*', '*', '*'] and "/home/user/uptime_monitor.py" in command:
                found = True
                break

    assert found, "Cron job for /home/user/uptime_monitor.py running every minute was not found."

def test_script_functionality_down():
    script_path = "/home/user/uptime_monitor.py"
    log_path = "/home/user/service_status.log"

    # Ensure port 8080 is not in use (or script handles it as DOWN)
    subprocess.run([script_path], check=False)

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Log file is empty after running the script."
    last_line = lines[-1].strip()
    assert last_line == "STATUS: DOWN", f"Expected 'STATUS: DOWN' when service is unreachable, got '{last_line}'"

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        pass

def test_script_functionality_up():
    script_path = "/home/user/uptime_monitor.py"
    log_path = "/home/user/service_status.log"

    server = HTTPServer(('localhost', 8080), HealthHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        # Give the server a moment to start
        time.sleep(1)

        subprocess.run([script_path], check=False)

        with open(log_path, "r") as f:
            lines = f.readlines()

        assert len(lines) > 0, "Log file is empty after running the script."
        last_line = lines[-1].strip()
        assert last_line == "STATUS: UP", f"Expected 'STATUS: UP' when service is reachable, got '{last_line}'"
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()