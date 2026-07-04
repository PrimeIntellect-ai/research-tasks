# test_final_state.py

import os
import subprocess
import threading
import socket
import pytest
import time

BINARY_PATH = "/home/user/infra_agent"
LOG_PATH = "/home/user/health.log"
UNIT_FILE_PATH = "/home/user/.config/systemd/user/infra_agent.service"

def dummy_listener():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 8888))
        s.listen(1)
        s.settimeout(2.0)
        conn, addr = s.accept()
        conn.close()
        s.close()
    except Exception:
        pass

def test_binary_exists_and_executable():
    assert os.path.exists(BINARY_PATH), f"Binary {BINARY_PATH} does not exist."
    assert os.access(BINARY_PATH, os.X_OK), f"Binary {BINARY_PATH} is not executable."

def test_binary_behavior():
    # Ensure the app_storage exists
    os.makedirs("/home/user/app_storage", exist_ok=True)

    # Start a dummy listener in case the original one was consumed
    t = threading.Thread(target=dummy_listener)
    t.start()
    time.sleep(0.1)

    # Clear log file if exists
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    env = os.environ.copy()
    env["USER"] = "user"

    try:
        subprocess.run([BINARY_PATH], env=env, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to execute binary: {e}")

    t.join(timeout=2)

    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} was not created by the binary."

    with open(LOG_PATH, "r") as f:
        content = f.read()

    assert "SYSTEM_READY" in content, f"Expected 'SYSTEM_READY' in {LOG_PATH}, but got '{content}'"

def test_systemd_unit_file():
    assert os.path.exists(UNIT_FILE_PATH), f"systemd unit file {UNIT_FILE_PATH} not found."

    with open(UNIT_FILE_PATH, "r") as f:
        content = f.read()

    assert "[Service]" in content, f"Unit file missing [Service] section."

    exec_start_found = False
    restart_always_found = False

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("ExecStart="):
            parts = line.split("=", 1)
            if parts[1].strip() == BINARY_PATH:
                exec_start_found = True
        if line.lower().startswith("restart="):
            parts = line.split("=", 1)
            if parts[1].strip().lower() == "always":
                restart_always_found = True

    assert exec_start_found, f"Unit file missing correct ExecStart={BINARY_PATH}"
    assert restart_always_found, f"Unit file missing Restart=always"