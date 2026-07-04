# test_final_state.py

import os
import subprocess
import socket
import time
import urllib.request
import urllib.error
import pytest

def test_deliverables_exist():
    """Verify that all required deliverables exist and have correct permissions."""
    assert os.path.isfile("/home/user/sanitizer.c"), "/home/user/sanitizer.c is missing."
    assert os.path.isfile("/home/user/sanitizer"), "/home/user/sanitizer binary is missing."
    assert os.access("/home/user/sanitizer", os.X_OK), "/home/user/sanitizer is not executable."

    assert os.path.isfile("/home/user/pipeline.sh"), "/home/user/pipeline.sh is missing."
    assert os.access("/home/user/pipeline.sh", os.X_OK), "/home/user/pipeline.sh is not executable."

    assert os.path.isfile("/home/user/proxy.sh"), "/home/user/proxy.sh is missing."
    assert os.access("/home/user/proxy.sh", os.X_OK), "/home/user/proxy.sh is not executable."

def test_adversarial_corpus():
    """
    Test the sanitizer binary against the clean and evil corpora.
    Must reject 100% of evil files (exit 1) and accept 100% of clean files (exit 0).
    """
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus
    for filename in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "rb") as f:
            proc = subprocess.run([sanitizer_path], stdin=f, capture_output=True)
            if proc.returncode != 1:
                bypassed_evil.append(filename)

    # Test clean corpus
    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "rb") as f:
            proc = subprocess.run([sanitizer_path], stdin=f, capture_output=True)
            if proc.returncode != 0:
                modified_clean.append(filename)

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(os.listdir(evil_dir))} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(os.listdir(clean_dir))} clean modified: {', '.join(modified_clean)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_pipeline_script():
    """Verify that the pipeline script runs successfully."""
    proc = subprocess.run(["/home/user/pipeline.sh"], capture_output=True, text=True)
    assert proc.returncode == 0, f"pipeline.sh failed with exit code {proc.returncode}. Output: {proc.stdout} {proc.stderr}"
    assert "PIPELINE SUCCESS" in proc.stdout, "pipeline.sh did not print 'PIPELINE SUCCESS'."

def send_tcp_request(port, payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", port))
        s.sendall(payload)
        response = s.recv(4096)
        s.close()
        return response
    except Exception as e:
        return b""

def test_end_to_end_clean_flow():
    """Verify that a clean request to 8080 is forwarded to 8081."""
    payload = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n{\"user\": \"test\"}"
    response = send_tcp_request(8080, payload)
    assert response, "No response received from proxy on port 8080 for clean request."
    assert b"403 Forbidden" not in response, "Clean request was incorrectly blocked."

def test_end_to_end_evil_flow():
    """Verify that an evil request to 8080 returns 403 Forbidden."""
    payload = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n{\"data\": \"admin' OR 1=1 --\"}"
    response = send_tcp_request(8080, payload)
    assert response, "No response received from proxy on port 8080 for evil request."
    assert b"403 Forbidden" in response, "Evil request was not blocked with 403 Forbidden."