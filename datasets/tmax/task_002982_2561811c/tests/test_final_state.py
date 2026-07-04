# test_final_state.py

import os
import re
import subprocess
import pytest

def test_benchmark_results_log():
    log_path = "/home/user/benchmark_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did you save the benchmark output?"

    with open(log_path, "r") as f:
        content = f.read()

    match = re.search(r'Result:\s+(\d+)\s+RPS', content)
    assert match is not None, "Could not parse RPS from benchmark_results.log. Ensure the exact output of the benchmark client was saved."

    rps = int(match.group(1))
    assert rps >= 10000, f"Logged RPS is {rps}, which is below the threshold of 10000 RPS. The concurrency bottleneck might not be fully resolved."

def test_server_running_and_performant():
    client_path = "/app/benchmark_client"
    assert os.path.isfile(client_path), f"Benchmark client {client_path} is missing."
    assert os.access(client_path, os.X_OK), f"Benchmark client {client_path} is not executable."

    # Run the client against the agent's background server
    proc = subprocess.run([client_path], capture_output=True, text=True)
    assert proc.returncode == 0, f"Benchmark client failed. Ensure the server is running on port 50051 and encoding logic is correct. Output: {proc.stdout}\nStderr: {proc.stderr}"

    match = re.search(r'Result:\s+(\d+)\s+RPS', proc.stdout)
    assert match is not None, "Could not parse RPS from live benchmark client output."

    rps = int(match.group(1))
    assert rps >= 10000, f"Live RPS is {rps}, which is below the threshold of 10000 RPS. The concurrency bottleneck might not be fully resolved."