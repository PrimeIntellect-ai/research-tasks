# test_final_state.py

import os
import subprocess
import pytest

def test_reproducible_result_matches_expected():
    result_path = "/home/user/reproducible_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. Did you run the script?"

    with open(result_path, "r") as f:
        actual_result = f.read().strip()

    # We need to compute the expected result using numpy in the user's venv
    venv_python = "/home/user/venv/bin/python"
    if not os.path.isfile(venv_python):
        # Fallback to system python if the user didn't use a venv but installed numpy globally
        venv_python = "python3"

    verifier_script = """
import numpy as np
import random

random.seed(42)
sequences = {}
for i in range(1, 101):
    seq_id = f"SEQ_{i:03d}"
    seq = "".join(random.choices(['A', 'C', 'G', 'T'], k=500))
    sequences[seq_id] = seq

def simulate(seq_id, sequence):
    numeric_id = int(seq_id.split('_')[1])
    np.random.seed(numeric_id)
    mutations = 0.0
    for char in sequence:
        if char == 'A': mutations += np.random.uniform(0, 0.01)
        elif char == 'C': mutations += np.random.uniform(0, 0.02)
        elif char == 'G': mutations += np.random.uniform(0, 0.015)
        elif char == 'T': mutations += np.random.uniform(0, 0.005)
    return mutations

total = 0.0
for sid in sorted(sequences.keys()):
    total += simulate(sid, sequences[sid])

print(f"{total:.15f}")
"""

    process = subprocess.run([venv_python, "-c", verifier_script], capture_output=True, text=True)
    assert process.returncode == 0, f"Failed to run verification script to compute truth. Is numpy installed? Error: {process.stderr}"

    expected_result = process.stdout.strip()

    assert actual_result == expected_result, f"Result mismatch! Expected {expected_result}, but got {actual_result}. Ensure floating point addition happens strictly in lexicographical order."

def test_script_maintains_parallelism():
    script_path = "/home/user/mutation_sim.py"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()

    assert "concurrent.futures.ProcessPoolExecutor" in content, "The script must maintain parallel execution using ProcessPoolExecutor."