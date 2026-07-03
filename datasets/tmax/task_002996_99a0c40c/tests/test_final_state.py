# test_final_state.py

import os
import stat
import subprocess
import socket
import threading
import json
import time
import shutil

SUPERVISOR_PATH = "/home/user/supervisor.sh"
EXPORTER_PATH = "/home/user/exporter.py"
SUPERVISOR_LOG = "/home/user/supervisor.log"
METRICS_LOG = "/home/user/metrics.log"
TEST_MNT = "/home/user/test_mnt"

def setup_module(module):
    # Ensure a clean state before tests
    for f in [SUPERVISOR_LOG, METRICS_LOG]:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(TEST_MNT):
        os.rmdir(TEST_MNT)

def teardown_module(module):
    # Clean up after tests
    for f in [SUPERVISOR_LOG, METRICS_LOG]:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(TEST_MNT):
        os.rmdir(TEST_MNT)

def test_supervisor_executable():
    assert os.path.isfile(SUPERVISOR_PATH), f"Supervisor script missing at {SUPERVISOR_PATH}"
    st = os.stat(SUPERVISOR_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Supervisor script {SUPERVISOR_PATH} is not executable."

def test_connectivity_failure():
    # Ensure port 8888 is closed and test_mnt is missing
    if os.path.exists(SUPERVISOR_LOG):
        os.remove(SUPERVISOR_LOG)

    result = subprocess.run([SUPERVISOR_PATH], capture_output=True, text=True)

    assert result.returncode == 1, f"Expected supervisor to exit with 1 on connectivity failure, got {result.returncode}"

    assert os.path.isfile(SUPERVISOR_LOG), f"{SUPERVISOR_LOG} was not created."
    with open(SUPERVISOR_LOG, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_line = "Restarting exporter, previous exit code: 2"
    count = lines.count(expected_line)
    assert count == 3, f"Expected 3 occurrences of '{expected_line}' in {SUPERVISOR_LOG}, found {count}. Lines: {lines}"

def listener_thread(port, stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        s.listen(5)
        s.settimeout(0.5)
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()
                conn.close()
            except socket.timeout:
                continue
            except Exception:
                break

def test_mount_failure():
    if os.path.exists(SUPERVISOR_LOG):
        os.remove(SUPERVISOR_LOG)
    if os.path.exists(TEST_MNT):
        os.rmdir(TEST_MNT)

    stop_event = threading.Event()
    t = threading.Thread(target=listener_thread, args=(8888, stop_event))
    t.start()

    try:
        # Give the listener a moment to start
        time.sleep(0.2)
        result = subprocess.run([SUPERVISOR_PATH], capture_output=True, text=True)

        assert result.returncode == 1, f"Expected supervisor to exit with 1 on mount failure, got {result.returncode}"

        assert os.path.isfile(SUPERVISOR_LOG), f"{SUPERVISOR_LOG} was not created."
        with open(SUPERVISOR_LOG, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        expected_line = "Restarting exporter, previous exit code: 3"
        count = lines.count(expected_line)
        assert count == 3, f"Expected 3 occurrences of '{expected_line}' in {SUPERVISOR_LOG}, found {count}. Lines: {lines}"
    finally:
        stop_event.set()
        t.join()

def test_success():
    if os.path.exists(SUPERVISOR_LOG):
        os.remove(SUPERVISOR_LOG)
    if os.path.exists(METRICS_LOG):
        os.remove(METRICS_LOG)

    os.makedirs(TEST_MNT, exist_ok=True)

    stop_event = threading.Event()
    t = threading.Thread(target=listener_thread, args=(8888, stop_event))
    t.start()

    try:
        time.sleep(0.2)
        result = subprocess.run([SUPERVISOR_PATH], capture_output=True, text=True)

        assert result.returncode == 0, f"Expected supervisor to exit with 0 on success, got {result.returncode}"

        assert os.path.isfile(METRICS_LOG), f"{METRICS_LOG} was not created."
        with open(METRICS_LOG, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        assert len(lines) >= 1, f"Expected at least one line in {METRICS_LOG}"
        last_line = lines[-1]

        try:
            data = json.loads(last_line)
        except json.JSONDecodeError:
            assert False, f"Failed to parse JSON from {METRICS_LOG}: {last_line}"

        assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
        assert data.get("port") == 8888, f"Expected port 8888, got {data.get('port')}"
        assert data.get("mount_dir") == TEST_MNT, f"Expected mount_dir '{TEST_MNT}', got {data.get('mount_dir')}"
    finally:
        stop_event.set()
        t.join()