# test_final_state.py

import os
import re
import subprocess
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

def test_directory_exists():
    assert os.path.isdir("/home/user/network_tools"), "Directory /home/user/network_tools does not exist."

def test_symlink_exists_and_correct():
    symlink_path = "/home/user/active_tool"
    target_path = "/home/user/network_tools/check_conn.py"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == target_path, f"Symlink does not point to {target_path}."

def test_script_is_executable():
    script_path = "/home/user/network_tools/check_conn.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_crontab_entry():
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        output = ""

    # Check for */5 * * * * /home/user/active_tool
    found = False
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Replace multiple spaces with single space for easier matching
        normalized_line = re.sub(r'\s+', ' ', line)
        if normalized_line == "*/5 * * * * /home/user/active_tool":
            found = True
            break

    assert found, "Crontab does not contain the correct entry: '*/5 * * * * /home/user/active_tool'."

def test_script_execution_fail_case():
    log_file = "/home/user/conn.log"
    script_path = "/home/user/active_tool"

    # Ensure server is down
    subprocess.run(["fuser", "-k", "8080/tcp"], capture_output=True)

    # Run script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"

    assert os.path.isfile(log_file), f"Log file {log_file} was not created."

    with open(log_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, "Log file is empty."
    last_line = lines[-1]

    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST\] FAIL$"
    assert re.match(pattern, last_line), f"Log line does not match expected format for FAIL case: {last_line}"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def test_script_execution_ok_case():
    log_file = "/home/user/conn.log"
    script_path = "/home/user/active_tool"

    # Start HTTP server
    server = HTTPServer(('127.0.0.1', 8080), SimpleHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        # Give server a moment to start
        time.sleep(0.5)

        # Run script
        result = subprocess.run([script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script execution failed: {result.stderr}"

        with open(log_file, "r") as f:
            lines = f.read().splitlines()

        assert len(lines) > 0, "Log file is empty."
        last_line = lines[-1]

        pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST\] OK$"
        assert re.match(pattern, last_line), f"Log line does not match expected format for OK case: {last_line}"
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()