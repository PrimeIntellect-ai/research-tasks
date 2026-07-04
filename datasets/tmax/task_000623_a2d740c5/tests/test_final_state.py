# test_final_state.py
import os
import subprocess
import struct
import random
import pytest

def test_fuzz_equivalence():
    """Verify the C program behaves bit-exactly identically to the oracle."""
    oracle_path = "/app/oracle_filter"
    agent_path = "/home/user/bayesian_filter"

    assert os.path.isfile(agent_path), f"Agent program {agent_path} not found."
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable."

    random.seed(42)

    for i in range(20):
        num_doubles = random.randint(1, 10000)
        input_data = bytearray()
        for _ in range(num_doubles):
            if random.random() < 0.15:
                val = -999.0
            else:
                val = random.uniform(-1000.0, 1000.0)
            input_data += struct.pack("<d", val)

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle program failed on valid input."
        assert agent_proc.returncode == 0, f"Agent program failed (return code {agent_proc.returncode}) on fuzz input."

        if oracle_proc.stdout != agent_proc.stdout:
            assert False, f"Agent output does not match oracle output on fuzz input #{i} (length {num_doubles} doubles)."

def test_etl_pipeline_files():
    """Verify the generated binary files match expected properties and oracle behavior."""
    raw_path = "/home/user/raw_measurements.bin"
    smoothed_path = "/home/user/smoothed_measurements.bin"

    assert os.path.isfile(raw_path), f"Raw measurements file {raw_path} not found."
    assert os.path.isfile(smoothed_path), f"Smoothed measurements file {smoothed_path} not found."

    with open(raw_path, "rb") as f:
        raw_data = f.read()

    # The video has 100 frames, so we expect 100 doubles (800 bytes)
    assert len(raw_data) == 800, f"Expected 800 bytes in {raw_path}, got {len(raw_data)} bytes."

    oracle_proc = subprocess.run(["/app/oracle_filter"], input=raw_data, capture_output=True)
    assert oracle_proc.returncode == 0, "Oracle failed on raw measurements."

    with open(smoothed_path, "rb") as f:
        smoothed_data = f.read()

    assert smoothed_data == oracle_proc.stdout, (
        "The contents of smoothed_measurements.bin do not match the expected "
        "output of running raw_measurements.bin through the Bayesian filter."
    )