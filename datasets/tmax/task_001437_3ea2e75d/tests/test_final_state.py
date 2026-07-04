# test_final_state.py
import os
import re
import json
import subprocess
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def test_nginx_conf_updated():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8080;" in content, "nginx.conf does not contain the updated proxy_pass directive pointing to 8080."
    assert "proxy_pass http://127.0.0.1:9090;" not in content, "nginx.conf still contains the old proxy_pass directive pointing to 9090."

def test_monitor_script_exists_and_executable():
    script_path = "/home/user/monitor.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def test_monitor_script_execution_and_output():
    script_path = "/home/user/monitor.py"
    json_path = "/home/user/status.json"

    # Remove existing status.json if any
    if os.path.exists(json_path):
        os.remove(json_path)

    # Start dummy HTTP server
    server = HTTPServer(('127.0.0.1', 8081), DummyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        # Run the monitor script
        result = subprocess.run([script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Execution of {script_path} failed with return code {result.returncode}. Stderr: {result.stderr}"

        # Check output JSON
        assert os.path.isfile(json_path), f"{json_path} was not created by the script."

        with open(json_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                assert False, f"{json_path} does not contain valid JSON."

        # Validate schema
        assert "timezone" in data, "Missing 'timezone' in JSON output."
        assert data["timezone"] == "Asia/Tokyo", f"Expected timezone 'Asia/Tokyo', got {data['timezone']}"

        assert "timestamp" in data, "Missing 'timestamp' in JSON output."
        timestamp_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+09:00$"
        assert re.match(timestamp_pattern, data["timestamp"]), f"Timestamp format is incorrect: {data['timestamp']}"

        assert "status_code" in data, "Missing 'status_code' in JSON output."
        assert data["status_code"] == 200, f"Expected status_code 200, got {data['status_code']}"

        assert "disk_usage_percent" in data, "Missing 'disk_usage_percent' in JSON output."
        assert isinstance(data["disk_usage_percent"], (int, float)), "disk_usage_percent must be a float or int."
        assert 0.0 <= float(data["disk_usage_percent"]) <= 100.0, "disk_usage_percent must be between 0 and 100."

    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()