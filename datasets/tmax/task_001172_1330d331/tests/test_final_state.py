# test_final_state.py
import os
import subprocess
import time
import urllib.request
import urllib.error
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import pytest

def test_audio_processor_service_running():
    # Check if the service is active
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "audio-processor.service"],
            capture_output=True, text=True, check=False
        )
        assert result.stdout.strip() == "active", "Service audio-processor.service is not active."
    except Exception as e:
        pytest.fail(f"Failed to check service status: {e}")

def test_audio_duration_file():
    duration_file = Path("/home/user/audio_duration.txt")
    assert duration_file.exists(), f"Duration file missing at {duration_file}"
    content = duration_file.read_text().strip()
    assert content == "12.45", f"Expected duration '12.45', got '{content}'"

def test_cron_job_exists():
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True, check=False
        )
        crontab_content = result.stdout
        # Check for */5 * * * * or something running every 5 minutes
        # Also check for monitor_storage.sh
        assert "/home/user/monitor_storage.sh" in crontab_content, "monitor_storage.sh not found in crontab"

        # Simple check for 5 minutes
        lines = [line for line in crontab_content.splitlines() if "/home/user/monitor_storage.sh" in line and not line.strip().startswith("#")]
        assert len(lines) > 0, "No active cron job found for monitor_storage.sh"
        line = lines[0].strip()
        parts = line.split()
        assert parts[0] == "*/5", f"Expected '*/5' for minute field, got '{parts[0]}'"
    except Exception as e:
        pytest.fail(f"Failed to check crontab: {e}")

def test_monitor_storage_script_exists():
    script_path = Path("/home/user/monitor_storage.sh")
    assert script_path.exists(), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_sanitize_config_adversarial_corpus():
    script_path = Path("/home/user/sanitize_config.py")
    assert script_path.exists(), f"Sanitize script missing at {script_path}"

    clean_dir = Path("/app/corpus/clean")
    evil_dir = Path("/app/corpus/evil")

    clean_failed = []
    evil_failed = []

    if clean_dir.exists():
        for f in clean_dir.iterdir():
            if f.is_file():
                res = subprocess.run(["python3", str(script_path), str(f)])
                if res.returncode != 0:
                    clean_failed.append(f.name)

    if evil_dir.exists():
        for f in evil_dir.iterdir():
            if f.is_file():
                res = subprocess.run(["python3", str(script_path), str(f)])
                if res.returncode != 1:
                    evil_failed.append(f.name)

    total_clean = len(list(clean_dir.iterdir())) if clean_dir.exists() else 0
    total_evil = len(list(evil_dir.iterdir())) if evil_dir.exists() else 0

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {total_clean} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {total_evil} evil bypassed: {', '.join(evil_failed)}")

    if error_msgs:
        pytest.fail("Adversarial corpus test failed: " + " | ".join(error_msgs))

class DummyBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"BACKEND_SUCCESS")

    def log_message(self, format, *args):
        pass

def test_reverse_proxy():
    # Spin up dummy backend on 9090
    server = HTTPServer(('127.0.0.1', 9090), DummyBackendHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    try:
        # Wait a moment for the proxy to be ready if it was just started
        time.sleep(1)
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8')
            assert body == "BACKEND_SUCCESS", "Proxy did not return expected response from backend"
    except Exception as e:
        pytest.fail(f"Failed to connect to proxy on port 8080 or it did not proxy correctly: {e}")
    finally:
        server.shutdown()
        server.server_close()
        t.join(timeout=1)