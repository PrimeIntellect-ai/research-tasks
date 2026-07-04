# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_c_exists_and_content():
    path = "/home/user/recovered.c"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "sqrt(256.0);" in content, f"File {path} does not contain the expected recovered source code."

def test_app_bin_exists_and_executable():
    path = "/home/user/app.bin"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_app_bin_linked_correctly():
    path = "/home/user/app.bin"
    try:
        output = subprocess.check_output(["ldd", path], stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ldd on {path}: {e.output.decode('utf-8')}")

    assert "libm.so" in output, f"File {path} does not link to libm (math library)."

def test_crash_payload():
    payload_path = "/home/user/crash_payload.txt"
    assert os.path.exists(payload_path), f"File {payload_path} is missing."

    with open(payload_path, "r") as f:
        payload = f.read().strip('\n') # Allow trailing newline but payload itself should be 'A's

    assert len(payload) > 0, "Payload is empty."
    assert all(c == 'A' for c in payload), "Payload contains characters other than 'A'."

    # Run the app with the payload
    app_path = "/home/user/app.bin"
    process = subprocess.Popen([app_path, payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()

    assert process.returncode == -11 or process.returncode == 139, f"Payload did not cause a segfault. Exit code: {process.returncode}"

    # Verify it is the shortest string (one 'A' less should not segfault)
    if len(payload) > 1:
        shorter_payload = payload[:-1]
        process_short = subprocess.Popen([app_path, shorter_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process_short.communicate()
        assert process_short.returncode not in (-11, 139), "A shorter payload also caused a segfault, so the provided payload is not the shortest."