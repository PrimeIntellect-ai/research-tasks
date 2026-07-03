# test_final_state.py
import os
import socket
import tarfile
import time
import pytest

def test_metadata_search():
    output_file = "/home/user/compromised_files.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_files = set()
    for root, _, files in os.walk("/app/storage_metadata/"):
        for file in files:
            if not file.endswith(".json"):
                continue
            path = os.path.join(root, file)
            if os.path.getsize(path) > 10240:
                with open(path, "r") as f:
                    content = f.read()
                    # A simplistic check for the exact key-value pair, removing spaces
                    if '"status":"compromised"' in content.replace(" ", ""):
                        expected_files.add(path)

    assert set(lines) == expected_files, f"Expected {expected_files}, but got {set(lines)} in {output_file}"

def test_daemon_unauthenticated_drop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", 5050))
        s.sendall(b"VIDEO_COUNT\n")
        response = s.recv(1024)
        assert response == b"", "Expected connection to be dropped without AUTH, but got response."
    except ConnectionRefusedError:
        pytest.fail("Daemon is not listening on 127.0.0.1:5050")
    finally:
        s.close()

def test_daemon_bad_auth_drop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", 5050))
        s.sendall(b"AUTH bad_token\n")
        response = s.recv(1024)
        assert response == b"", "Expected connection to be dropped with bad AUTH, but got response."
    finally:
        s.close()

def test_daemon_protocol():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", 5050))

        # 1. Auth
        s.sendall(b"AUTH storage_sec_token_v1\n")
        response = s.recv(1024).decode()
        assert response == "OK\n", f"Expected 'OK\\n', got {repr(response)}"

        # 2. Video Count
        s.sendall(b"VIDEO_COUNT\n")
        response = s.recv(1024).decode()
        assert response == "COUNT: 14\n", f"Expected 'COUNT: 14\\n', got {repr(response)}"

        # 3. Inspect safe
        s.sendall(b"INSPECT /app/test_safe.tar\n")
        response = s.recv(1024).decode()
        assert response == "SAFE\n", f"Expected 'SAFE\\n', got {repr(response)}"

        # 4. Inspect malicious
        s.sendall(b"INSPECT /app/test_malicious.tar\n")
        response = s.recv(1024).decode()
        assert response == "MALICIOUS\n", f"Expected 'MALICIOUS\\n', got {repr(response)}"

        # 5. Watch
        s.sendall(b"WATCH /home/user/dropzone\n")
        response = s.recv(1024).decode()
        assert response == "WATCHING\n", f"Expected 'WATCHING\\n', got {repr(response)}"

    finally:
        s.close()

def test_daemon_watch_behavior():
    # Wait a moment to ensure WATCH is fully registered
    time.sleep(0.5)

    # Create a malicious tarball in the dropzone
    payload_path = "/home/user/dropzone/payload.tar"
    with tarfile.open(payload_path, "w") as tar:
        ti = tarfile.TarInfo(name="../etc/shadow")
        ti.size = 0
        tar.addfile(ti)

    # Give the daemon time to process the inotify event and write to the log
    time.sleep(1)

    log_path = "/home/user/archive_watch.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_log = "[NEW_FILE] payload.tar: MALICIOUS\n"
    assert expected_log in log_content, f"Expected {repr(expected_log)} in log file, got {repr(log_content)}"