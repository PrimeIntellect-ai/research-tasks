# test_final_state.py
import os
import glob
import socket
import subprocess
import pytest

def test_files_renamed():
    """Check that .zlog files were renamed to .legacy.z."""
    logs_dir = "/home/user/logs"
    zlog_files = glob.glob(os.path.join(logs_dir, "*.zlog"))
    assert len(zlog_files) == 0, f"Found .zlog files still remaining in {logs_dir}."

    legacy_files = glob.glob(os.path.join(logs_dir, "*.legacy.z"))
    assert len(legacy_files) > 0, f"No .legacy.z files found in {logs_dir}."

    syslog_path = os.path.join(logs_dir, "syslog.legacy.z")
    assert os.path.isfile(syslog_path), f"Expected file {syslog_path} does not exist."

def test_c_program_exists():
    """Check that the C source and compiled binary exist."""
    assert os.path.isfile("/home/user/log_server.c"), "Source file /home/user/log_server.c is missing."
    assert os.path.isfile("/home/user/log_server"), "Compiled binary /home/user/log_server is missing."
    assert os.access("/home/user/log_server", os.X_OK), "Compiled binary /home/user/log_server is not executable."

def test_server_response():
    """Connect to the server and verify it returns correctly converted UTF-8 content."""
    syslog_path = "/home/user/logs/syslog.legacy.z"
    assert os.path.exists(syslog_path), f"Cannot test server, {syslog_path} missing."

    # Generate expected output using the provided binary
    try:
        raw_output = subprocess.check_output(["/app/bin/zdecoder", syslog_path])
        expected_utf8 = raw_output.decode("utf-16le").encode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to generate expected output using zdecoder: {e}")

    host = "127.0.0.1"
    port = 9090

    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        pytest.fail(f"Could not connect to server at {host}:{port}: {e}")

    try:
        s.sendall(f"{syslog_path}\n".encode("utf-8"))

        received_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            received_data += chunk

    except Exception as e:
        pytest.fail(f"Error communicating with server: {e}")
    finally:
        s.close()

    assert received_data == expected_utf8, "Server response does not match the expected UTF-8 output."