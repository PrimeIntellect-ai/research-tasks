# test_final_state.py

import os
import glob
import socket
import threading
import time
import subprocess
import pytest

def test_timezone_file():
    path = "/home/user/timezone.txt"
    assert os.path.isfile(path), f"Missing timezone file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "Pacific/Auckland", f"Expected timezone 'Pacific/Auckland', got '{content}'"

def test_proxy_forwarding():
    received_data = []

    def dummy_backend():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', 9090))
            s.listen(1)
            s.settimeout(3)
            conn, _ = s.accept()
            data = conn.recv(1024)
            received_data.append(data)
            conn.close()
            s.close()
        except Exception:
            pass

    t = threading.Thread(target=dummy_backend)
    t.start()

    # Give the backend a moment to start listening
    time.sleep(0.5)

    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.settimeout(2)
        c.connect(('127.0.0.1', 8080))
        c.sendall(b"proxy_test_payload")
        c.close()
    except Exception as e:
        pytest.fail(f"Could not connect to proxy on port 8080: {e}")

    t.join(timeout=4)
    assert received_data, "No data received on internal backend port 9090. Proxy is not forwarding traffic correctly."
    assert received_data[0] == b"proxy_test_payload", "Data received on port 9090 did not match the payload sent to port 8080."

def test_bio_filter_adversarial():
    script_path = "/home/user/bio_filter.sh"
    assert os.path.isfile(script_path), f"Missing bio filter script: {script_path}"

    clean_files = glob.glob("/app/clean_bios/*")
    evil_files = glob.glob("/app/evil_bios/*")

    assert len(clean_files) > 0, "Clean corpus missing"
    assert len(evil_files) > 0, "Evil corpus missing"

    clean_failed = []
    for cf in clean_files:
        with open(cf, "rb") as f:
            data = f.read()
        res = subprocess.run(["/bin/bash", script_path], input=data, capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        with open(ef, "rb") as f:
            data = f.read()
        res = subprocess.run(["/bin/bash", script_path], input=data, capture_output=True)
        if res.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected (expected exit 0): {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (expected exit 1): {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_sync_users_script_fixed():
    path = "/home/user/sync_users.sh"
    assert os.path.isfile(path), f"Missing script file: {path}"
    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/sync.log" in content, f"Script {path} does not use the absolute path '/home/user/sync.log'."
    assert "PATH=" in content and "/usr/bin" in content, f"Script {path} does not set PATH to include /usr/bin."