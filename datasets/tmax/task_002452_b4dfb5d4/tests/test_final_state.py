# test_final_state.py

import os
import subprocess
import time
import urllib.request
import json
import pytest

APP_DIR = "/home/user/app"
SANITIZER_BIN = os.path.join(APP_DIR, "sanitizer")
CLEAN_CORPUS_DIR = os.path.join(APP_DIR, "corpora", "clean")
EVIL_CORPUS_DIR = os.path.join(APP_DIR, "corpora", "evil")
WORKER_DIR = os.path.join(APP_DIR, "worker")
WORKER_BIN = os.path.join(WORKER_DIR, "worker_daemon")
START_SCRIPT = os.path.join(APP_DIR, "start_services.sh")
LOG_FILE = os.path.join(WORKER_DIR, "logs", "processed.log")

def test_makefile_repair():
    """Test that the Makefile successfully builds the worker_daemon."""
    # Clean first if possible, but just running make is fine
    subprocess.run(["make", "clean"], cwd=WORKER_DIR, capture_output=True)
    result = subprocess.run(["make"], cwd=WORKER_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Make failed:\n{result.stderr}"
    assert os.path.isfile(WORKER_BIN), f"Worker binary {WORKER_BIN} was not produced."
    assert os.access(WORKER_BIN, os.X_OK), f"Worker binary {WORKER_BIN} is not executable."

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_BIN), f"Sanitizer binary {SANITIZER_BIN} is missing."
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary {SANITIZER_BIN} is not executable."

def test_sanitizer_clean_corpus():
    """Test that sanitizer accepts all clean files."""
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.cpp') or f.endswith('.cc') or f.endswith('.c')]
    if not clean_files:
        # Fallback if no extensions or different
        clean_files = os.listdir(CLEAN_CORPUS_DIR)

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([SANITIZER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_files)}"

def test_sanitizer_evil_corpus():
    """Test that sanitizer rejects all evil files."""
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.cpp') or f.endswith('.cc') or f.endswith('.c')]
    if not evil_files:
        evil_files = os.listdir(EVIL_CORPUS_DIR)

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        result = subprocess.run([SANITIZER_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}"

def test_end_to_end_services():
    """Test the E2E flow by starting services, sending a request, and checking the log."""
    # Ensure log directory exists and clear previous log
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Start services
    proc = subprocess.Popen([START_SCRIPT], cwd=APP_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3) # Wait for services to initialize

    try:
        # Send request to Nginx API Gateway
        req = urllib.request.Request(
            "http://localhost:8080/api/submit",
            data=json.dumps({"code": "int main(){return 0;}"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"API returned status {response.status}"
        except Exception as e:
            pytest.fail(f"Failed to communicate with API Gateway: {e}")

        # Wait for worker to process
        time.sleep(2)

        # Check log
        assert os.path.exists(LOG_FILE), f"Worker log file {LOG_FILE} was not created. Worker did not process the job."
        with open(LOG_FILE, "r") as f:
            log_content = f.read()
        assert log_content.strip(), f"Worker log file {LOG_FILE} is empty."

    finally:
        # Cleanup processes
        subprocess.run(["pkill", "-f", "nginx"], capture_output=True)
        subprocess.run(["pkill", "-f", "flask"], capture_output=True)
        subprocess.run(["pkill", "-f", "app.py"], capture_output=True)
        subprocess.run(["pkill", "-f", "redis-server"], capture_output=True)
        subprocess.run(["pkill", "-f", "worker_daemon"], capture_output=True)