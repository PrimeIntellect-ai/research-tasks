# test_final_state.py

import os
import socket
import threading
import subprocess
import re
import time
import pytest

def test_data_dir_exists():
    """Ensure the data_dir directory exists."""
    path = "/home/user/data_dir"
    assert os.path.isdir(path), f"{path} does not exist."

def test_c_file_exists():
    """Ensure the C source file exists."""
    path = "/home/user/health_reporter.c"
    assert os.path.isfile(path), f"{path} does not exist."

def test_executable_exists():
    """Ensure the compiled executable exists and is executable."""
    path = "/home/user/health_reporter"
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_bash_profile_exports():
    """Ensure .bash_profile contains the required environment variables."""
    path = "/home/user/.bash_profile"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "REPORTER_HOST=127.0.0.1" in content, "REPORTER_HOST=127.0.0.1 not found in .bash_profile"
    assert "REPORTER_PORT=8888" in content, "REPORTER_PORT=8888 not found in .bash_profile"

def test_run_sh_exists_and_executable():
    """Ensure run.sh exists, is executable, and contains necessary commands."""
    path = "/home/user/run.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."
    with open(path, "r") as f:
        content = f.read()
    assert ".bash_profile" in content, "run.sh does not seem to source .bash_profile"
    assert "health_reporter" in content, "run.sh does not seem to execute health_reporter"

def test_end_to_end_reporting():
    """Verify the end-to-end functionality by catching the TCP payload."""
    received_data = []

    def listener():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", 8888))
            s.listen(1)
            s.settimeout(5)
            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    received_data.append(data.decode("utf-8"))
            except socket.timeout:
                pass

    t = threading.Thread(target=listener)
    t.start()

    # Give the listener a moment to bind
    time.sleep(0.5)

    # Run the wrapper script
    result = subprocess.run(["bash", "/home/user/run.sh"], capture_output=True, text=True)

    t.join()

    assert received_data, "No data received on port 8888. The C program failed to connect or send data."
    output = received_data[0]

    # Validate the format of the received data
    match = re.match(r"^DATA_DIR_FREE_BYTES:(\d+)\n?$", output)
    assert match, f"Received data format is incorrect. Expected 'DATA_DIR_FREE_BYTES:<bytes>\\n', got {output!r}"