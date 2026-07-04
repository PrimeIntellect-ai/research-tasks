# test_final_state.py

import os
import subprocess
import pytest

def test_minimal_hex_file():
    path = "/home/user/minimal_hex.txt"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_hex = "0080e03779c34143"
    assert content.lower() == expected_hex, f"Content of {path} is incorrect. Expected '{expected_hex}', got '{content}'."

def test_service_go_source():
    path = "/home/user/service.go"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "ctx.Done()" in content, f"File {path} does not seem to contain a check for ctx.Done()."

def test_fixed_service_executable():
    path = "/home/user/fixed_service"
    assert os.path.exists(path), f"Executable {path} is missing. Did you compile the service?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_fixed_service_execution():
    executable = "/home/user/fixed_service"
    payload = "/home/user/payload.bin"

    assert os.path.exists(executable), "Fixed service executable not found."
    assert os.path.exists(payload), "Payload file not found."

    try:
        result = subprocess.run([executable, payload], capture_output=True, text=True, timeout=2)
    except subprocess.TimeoutExpired:
        pytest.fail("The fixed_service timed out. The infinite loop or goroutine leak is likely still present.")

    assert result.returncode == 0, f"fixed_service exited with code {result.returncode}, expected 0. Output: {result.stdout}\n{result.stderr}"
    assert "Success" in result.stdout, "fixed_service did not print 'Success'."
    assert "Watchdog" not in result.stdout, "fixed_service triggered the watchdog timeout."