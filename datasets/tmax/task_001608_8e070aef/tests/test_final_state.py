# test_final_state.py

import os
import subprocess
import struct
import random
import tempfile
import urllib.request
import urllib.error
import json
import time
import pytest

ORACLE_PATH = "/opt/oracle/worker_oracle"
AGENT_PATH = "/home/user/workspace/worker_fixed"
GATEWAY_PATH = "/home/user/workspace/gateway.py"

def generate_fuzz_input(num_records):
    """Generate a binary payload of 9-byte records."""
    data = bytearray()
    # Use a large mean to trigger catastrophic cancellation in naive variance formulas
    mean_val = random.choice([1e6, 5e6, 1e7])
    for _ in range(num_records):
        sensor_id = random.randint(1, 5)
        timestamp = random.randint(1600000000, 1700000000)
        # Small variance around a large mean
        value = mean_val + random.uniform(-0.5, 0.5)
        data.extend(struct.pack('<BIf', sensor_id, timestamp, value))
    return bytes(data)

def test_worker_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

    random.seed(42)

    for i in range(100):
        num_records = random.randint(10, 100)
        input_data = generate_fuzz_input(num_records)

        with tempfile.NamedTemporaryFile(delete=False) as f_in, \
             tempfile.NamedTemporaryFile(delete=False) as f_out_oracle, \
             tempfile.NamedTemporaryFile(delete=False) as f_out_agent:

            f_in.write(input_data)
            f_in.flush()

            in_name = f_in.name
            out_oracle_name = f_out_oracle.name
            out_agent_name = f_out_agent.name

        try:
            # Run oracle
            subprocess.run(
                [ORACLE_PATH, "--file-mode", in_name, out_oracle_name],
                check=True,
                capture_output=True
            )

            # Run agent
            agent_res = subprocess.run(
                [AGENT_PATH, "--file-mode", in_name, out_agent_name],
                capture_output=True,
                text=True
            )
            assert agent_res.returncode == 0, f"Agent program failed on fuzz input {i}:\n{agent_res.stderr}"

            with open(out_oracle_name, 'rb') as f:
                oracle_out = f.read()

            with open(out_agent_name, 'rb') as f:
                agent_out = f.read()

            assert oracle_out == agent_out, (
                f"Mismatch on fuzz iteration {i} (num_records={num_records}).\n"
                f"Oracle output: {oracle_out.hex()}\n"
                f"Agent output: {agent_out.hex()}"
            )
        finally:
            os.remove(in_name)
            os.remove(out_oracle_name)
            os.remove(out_agent_name)

def test_end_to_end_pipeline():
    # Start gateway
    gateway_proc = subprocess.Popen(["python3", GATEWAY_PATH])

    # Start agent worker in daemon mode
    worker_proc = subprocess.Popen([AGENT_PATH, "--daemon"])

    try:
        # Wait for gateway to start
        time.sleep(2)

        # Clear redis list before test
        subprocess.run(["redis-cli", "DEL", "processed_variances"], check=True)

        # Send requests
        sensor_id = 42
        base_val = 1000000.0
        values = [base_val + 0.1, base_val + 0.3, base_val - 0.2, base_val + 0.5, base_val - 0.1]

        for i, val in enumerate(values):
            req_data = json.dumps({
                "sensor_id": sensor_id,
                "timestamp": 1620000000 + i,
                "value": val
            }).encode('utf-8')

            req = urllib.request.Request(
                "http://127.0.0.1:5000/ingest",
                data=req_data,
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req)

        time.sleep(2)

        # Check Redis for processed variances
        res = subprocess.run(
            ["redis-cli", "LPOP", "processed_variances"],
            capture_output=True,
            text=True
        )
        output = res.stdout.strip()
        assert output != "" and output != "(nil)", "No output found in Redis list 'processed_variances'. Pipeline communication may still be broken."

    finally:
        gateway_proc.terminate()
        worker_proc.terminate()
        gateway_proc.wait()
        worker_proc.wait()