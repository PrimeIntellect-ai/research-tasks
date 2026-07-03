# test_final_state.py

import os
import subprocess
import tempfile
import time
import random
import string
import pytest

AGENT_SCRIPT = "/home/user/secure_hasher.py"
BINARY = "/app/log_hasher"

def generate_random_file(directory, size=1024):
    name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"
    path = os.path.join(directory, name)
    with open(path, "wb") as f:
        f.write(os.urandom(size))
    return path

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception:
        return "ERROR"

def test_secure_hasher_metrics():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

    num_safe = 500
    num_malicious = 100

    malicious_payloads = [
        "../../../etc/passwd",
        "file; id",
        "file && whoami",
        "../../var/log",
        "test|ls",
        "test`id`",
        "test$(id)",
        "/etc/shadow",
        "../app/log_hasher"
    ]

    correct_hashes = 0
    correctly_rejected = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        safe_files = [generate_random_file(tmpdir, random.randint(500, 5000)) for _ in range(num_safe)]

        # Measure C binary time
        start_c = time.time()
        c_outputs = []
        for f in safe_files:
            c_outputs.append(run_cmd([BINARY, f]))
        c_time = time.time() - start_c

        # Measure Python script time
        start_py = time.time()
        py_outputs = []
        for f in safe_files:
            py_outputs.append(run_cmd([AGENT_SCRIPT, f]))
        py_time = time.time() - start_py

        # Compare safe files
        for c_out, py_out in zip(c_outputs, py_outputs):
            if c_out and py_out and c_out.lower() == py_out.lower():
                correct_hashes += 1

        # Test malicious files
        for _ in range(num_malicious):
            payload = random.choice(malicious_payloads)
            py_out = run_cmd([AGENT_SCRIPT, payload])
            if py_out == "ERROR":
                correctly_rejected += 1

    accuracy = (correct_hashes + correctly_rejected) / (num_safe + num_malicious)

    # Avoid division by zero
    c_time = max(c_time, 0.001)
    runtime_ratio = py_time / c_time

    assert accuracy == 1.0, f"Accuracy is {accuracy}, expected 1.0. Correct hashes: {correct_hashes}/{num_safe}, Correctly rejected: {correctly_rejected}/{num_malicious}."
    assert runtime_ratio <= 5.0, f"Runtime ratio is {runtime_ratio:.2f} (Python: {py_time:.2f}s, C: {c_time:.2f}s), expected <= 5.0."