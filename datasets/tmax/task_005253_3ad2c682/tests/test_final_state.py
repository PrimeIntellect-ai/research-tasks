# test_final_state.py

import os
import random
import subprocess
import socket
import threading
import time
import pytest

def test_files_exist_and_executable():
    """Check that the required files exist and have correct permissions."""
    c_file = "/home/user/mc_profiler.c"
    binary = "/home/user/mc_profiler"
    script = "/home/user/run_pipeline.sh"

    assert os.path.isfile(c_file), f"Source file {c_file} is missing."
    assert os.path.isfile(binary), f"Compiled binary {binary} is missing."
    assert os.access(binary, os.X_OK), f"Compiled binary {binary} is not executable."
    assert os.path.isfile(script), f"Pipeline script {script} is missing."
    assert os.access(script, os.X_OK), f"Pipeline script {script} is not executable."

def test_fuzz_equivalence():
    """Fuzz test the compiled binary against the oracle."""
    oracle_path = "/app/oracle_mc"
    agent_path = "/home/user/mc_profiler"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} missing."

    random.seed(42)
    inputs = []
    for _ in range(1000):
        seed = random.randint(0, 4294967295)
        iterations = random.randint(100, 100000)
        inputs.append(f"{seed} {iterations}")

    input_str = "\n".join(inputs) + "\n"
    input_bytes = input_str.encode('utf-8')

    oracle_proc = subprocess.run([oracle_path], input=input_bytes, capture_output=True, text=True)
    assert oracle_proc.returncode == 0, "Oracle failed to execute."

    agent_proc = subprocess.run([agent_path], input=input_bytes, capture_output=True, text=True)

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent binary failed with return code {agent_proc.returncode}. Stderr: {agent_proc.stderr}")

    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    assert len(oracle_lines) == len(inputs), f"Oracle output line count mismatch. Expected {len(inputs)}, got {len(oracle_lines)}"
    assert len(agent_lines) == len(inputs), f"Agent output line count mismatch. Expected {len(inputs)}, got {len(agent_lines)}"

    for i, (oracle_val, agent_val) in enumerate(zip(oracle_lines, agent_lines)):
        if oracle_val != agent_val:
            pytest.fail(f"Mismatch on input '{inputs[i]}'. Oracle output: '{oracle_val}', Agent output: '{agent_val}'")

def test_pipeline_script():
    """Test that the run_pipeline.sh script properly routes data between ports 5001 and 5002."""
    script = "/home/user/run_pipeline.sh"
    oracle_path = "/app/oracle_mc"

    test_input = b"42 1000\n12345 500\n"

    oracle_proc = subprocess.run([oracle_path], input=test_input, capture_output=True)
    expected_output = oracle_proc.stdout

    received_data = []
    error_occurred = []

    def emitter():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', 5001))
            s.listen(1)
            conn, addr = s.accept()
            conn.sendall(test_input)
            conn.close()
            s.close()
        except Exception as e:
            error_occurred.append(f"Emitter error: {e}")

    def aggregator():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', 5002))
            s.listen(1)
            conn, addr = s.accept()
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
            received_data.append(data)
            conn.close()
            s.close()
        except Exception as e:
            error_occurred.append(f"Aggregator error: {e}")

    t1 = threading.Thread(target=emitter)
    t2 = threading.Thread(target=aggregator)
    t1.start()
    t2.start()

    time.sleep(0.5)

    try:
        proc = subprocess.run([script], timeout=5, capture_output=True, text=True)
        assert proc.returncode == 0, f"run_pipeline.sh exited with code {proc.returncode}. Stderr: {proc.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("run_pipeline.sh timed out. It may not be closing connections properly.")
    finally:
        t1.join(timeout=1)
        t2.join(timeout=1)

    assert not error_occurred, f"Socket errors occurred: {error_occurred}"
    assert len(received_data) == 1, "Aggregator did not receive connection/data."
    assert received_data[0] == expected_output, f"Data mismatch in pipeline. Expected {expected_output}, got {received_data[0]}"