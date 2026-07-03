# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import pytest

def test_symlink_and_frames():
    """Verify symlink and ffmpeg frame extraction."""
    symlink_path = "/home/user/active_feed.mp4"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    assert os.readlink(symlink_path) == "/app/camera1.mp4", f"{symlink_path} does not point to /app/camera1.mp4"

    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist"

    # Verify exactly 15 frames are generated (15s video at 1 fps)
    frames = [f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".jpg")]
    assert len(frames) == 15, f"Expected 15 frames, found {len(frames)}"
    for i in range(1, 16):
        expected_frame = f"frame_{i:04d}.jpg"
        assert expected_frame in frames, f"Missing {expected_frame}"

def test_port_forwarding():
    """Verify socat port forwarding from 8080 to 9090."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('127.0.0.1', 9090))
        server.listen(1)
    except Exception as e:
        pytest.fail(f"Could not bind to 9090 for testing: {e}")

    success = False
    def handle_client():
        nonlocal success
        try:
            server.settimeout(2.0)
            conn, addr = server.accept()
            data = conn.recv(1024)
            if data == b"ping":
                conn.sendall(b"pong")
                success = True
            conn.close()
        except Exception:
            pass

    t = threading.Thread(target=handle_client)
    t.start()
    time.sleep(0.5)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect(('127.0.0.1', 8080))
        client.sendall(b"ping")
        resp = client.recv(1024)
        assert resp == b"pong", "Did not receive correct response through port forward"
        client.close()
    except Exception as e:
        pytest.fail(f"Port forwarding test failed: {e}")
    finally:
        server.close()
        t.join(timeout=2)
        assert success, "Dummy server on 9090 did not receive the forwarded request"

def test_validator_script_adversarial():
    """Verify validator script against clean and evil corpora."""
    script = "/home/user/validator.py"
    assert os.path.isfile(script), f"Missing validator script at {script}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = os.listdir(clean_dir)
    evil_files = os.listdir(evil_dir)

    clean_failed = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, 'rb') as fp:
            res = subprocess.run(["python3", script], stdin=fp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode != 0:
                clean_failed.append(f)

    evil_failed = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, 'rb') as fp:
            res = subprocess.run(["python3", script], stdin=fp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                evil_failed.append(f)

    if clean_failed or evil_failed:
        msg = []
        if clean_failed:
            msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
        if evil_failed:
            msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
        pytest.fail(" | ".join(msg))

def test_logrotate_config():
    """Verify the logrotate configuration."""
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"Missing logrotate.conf at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "daily" in content, "Missing 'daily' rotation in logrotate.conf"
    assert "rotate 7" in content, "Missing 'rotate 7' in logrotate.conf"
    assert "compress" in content, "Missing 'compress' in logrotate.conf"
    assert "create 0644" in content or "create 644" in content, "Missing 'create 0644' in logrotate.conf"
    assert "/home/user/logs" in content, "Log path /home/user/logs is not properly specified in logrotate.conf"