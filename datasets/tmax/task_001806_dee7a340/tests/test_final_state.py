# test_final_state.py

import os
import re
import subprocess
import time
import pytest
import signal

def test_benchmark_log_exists_and_format():
    log_path = "/home/user/benchmark.log"
    assert os.path.exists(log_path), f"Benchmark log not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, "Benchmark log should contain at least two lines"

    assert "All values correct: True" in content[0], "First line of benchmark.log must be 'All values correct: True'"

    latency_match = re.search(r"Average latency:\s+\d+\.\d+\s+ms", content[1])
    assert latency_match is not None, "Second line of benchmark.log must match 'Average latency: X.XX ms'"

def test_server_binary_exists():
    binary_path = "/home/user/backend/build/server"
    assert os.path.exists(binary_path), f"Compiled server binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Server binary at {binary_path} is not executable"

def test_server_logic_and_memory_leak():
    binary_path = "/home/user/backend/build/server"
    client_path = "/home/user/client/client_v3.py"

    assert os.path.exists(client_path), f"Client script not found at {client_path}"

    # Start the server under valgrind
    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--show-leak-kinds=all",
        "--error-exitcode=1",
        binary_path
    ]

    server_proc = subprocess.Popen(
        valgrind_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Give the server a moment to start
    time.sleep(2)

    # Run the client
    client_env = os.environ.copy()
    client_env["PYTHONPATH"] = "/home/user/client:" + client_env.get("PYTHONPATH", "")
    client_proc = subprocess.run(
        ["python3", client_path],
        cwd="/home/user/client",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=client_env
    )

    # Terminate the server
    server_proc.send_signal(signal.SIGINT)
    try:
        server_stdout, server_stderr = server_proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        server_proc.kill()
        server_stdout, server_stderr = server_proc.communicate()

    assert client_proc.returncode == 0, f"Client script failed to run. Stderr: {client_proc.stderr.decode('utf-8')}"

    # Check valgrind output for memory leaks
    # "definitely lost: 0 bytes in 0 blocks"
    assert "definitely lost: 0 bytes in 0 blocks" in server_stderr, "Memory leak detected in the C++ server or valgrind did not run properly"