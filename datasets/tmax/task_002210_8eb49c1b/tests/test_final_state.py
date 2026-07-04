# test_final_state.py
import os
import time
import struct
import subprocess
import pytest
import numpy as np
from scapy.all import rdpcap, UDP

def test_setup_py_fixed():
    setup_path = "/app/vendored/fast_sensor_calc-0.1.0/setup.py"
    assert os.path.exists(setup_path), f"setup.py is missing at {setup_path}"
    with open(setup_path, 'r') as f:
        content = f.read()
    assert "src/math_utils.c" in content, "setup.py is still missing 'src/math_utils.c' in the sources list. The C-extension cannot build correctly without it."

def test_run_analysis_and_check_output():
    script_path = "/home/user/run_analysis.py"
    output_path = "/home/user/output_variances.txt"
    pcap_path = "/app/data/sensor_stream.pcap"

    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Remove output if it exists to ensure we are testing the script's execution
    if os.path.exists(output_path):
        os.remove(output_path)

    start_time = time.time()
    try:
        res = subprocess.run(["python3", script_path], timeout=10, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        pytest.fail("Execution timed out. The script took longer than 10 seconds.")

    duration = time.time() - start_time

    assert res.returncode == 0, f"Script failed with error:\n{res.stderr}"
    assert duration < 5.0, f"Execution took too long ({duration:.2f}s). Expected < 5.0s. Make sure you are using the C-extension and not pure Python for the math."

    assert os.path.exists(output_path), f"Output file {output_path} was not created by the script."

    # Read Gold Reference
    packets = rdpcap(pcap_path)
    gold_variances = []
    for p in packets:
        if UDP in p and p[UDP].dport == 5000:
            payload = bytes(p[UDP].payload)
            count = len(payload) // 8
            floats = struct.unpack(f'<{count}d', payload)
            gold_variances.append(np.var(floats, ddof=0))

    # Read Agent Output
    with open(output_path, 'r') as f:
        agent_lines = f.read().strip().split('\n')

    assert len(agent_lines) == len(gold_variances), f"Row count mismatch. Expected {len(gold_variances)}, got {len(agent_lines)}"

    agent_variances = []
    for val in agent_lines:
        try:
            agent_variances.append(float(val))
        except ValueError:
            pytest.fail(f"Invalid float in output: {val}")

    # Compute MSE
    mse = np.mean((np.array(gold_variances) - np.array(agent_variances))**2)

    threshold = 1e-6
    assert mse < threshold, f"MSE {mse} exceeds threshold {threshold}. The numerical instability in the C-extension was not properly fixed."