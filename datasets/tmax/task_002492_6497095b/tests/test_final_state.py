# test_final_state.py
import os
import subprocess
import pytest

def test_execution_log():
    log_path = "/home/user/execution_log.txt"
    assert os.path.isfile(log_path), f"Output file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "FINAL_ACCUMULATOR: 42", f"Expected 'FINAL_ACCUMULATOR: 42' in {log_path}, but got '{content}'"

def test_binary_exists_and_executable():
    bin_path = "/home/user/ws_interp"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_no_memory_leaks():
    bin_path = "/home/user/ws_interp"
    payload_path = "/home/user/payload.bin"

    assert os.path.isfile(bin_path), "Binary missing, cannot run valgrind."
    assert os.path.isfile(payload_path), "Payload missing, cannot run valgrind."

    cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=1",
        bin_path
    ]

    with open(payload_path, "rb") as f_in:
        result = subprocess.run(cmd, stdin=f_in, capture_output=True, text=True)

    stderr = result.stderr.lower()

    assert "definitely lost: 0 bytes" in stderr, f"Memory leak detected: 'definitely lost: 0 bytes' not found in valgrind output.\nValgrind stderr:\n{result.stderr}"
    assert result.returncode == 0, f"Valgrind reported errors or the program crashed. Return code: {result.returncode}\nStderr:\n{result.stderr}"