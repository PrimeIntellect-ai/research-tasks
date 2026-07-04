# test_final_state.py

import os
import subprocess
import pytest

def get_expected_value():
    """
    Recomputes the expected optimized threshold using the fixed deterministic logic.
    We use a subprocess to invoke the environment's installed scientific libraries
    while keeping the test file itself restricted to the standard library.
    """
    script = """
import h5py
import numpy as np
from scipy.optimize import minimize
import networkx as nx

def evaluate_threshold(thresh, file_path):
    thresh_val = thresh[0]
    with h5py.File(file_path, 'r') as f:
        G = nx.Graph()
        nodes = sorted(list(f.keys()))

        for n in nodes:
            G.add_node(n, signal=f[n][:])

        total_energy = 0.0
        for n in nodes:
            sig = G.nodes[n]['signal']
            sig_masked = np.where(np.abs(sig) > thresh_val, sig, 0)
            sp = np.fft.fft(sig_masked)
            energy = np.sum(np.abs(sp)**2)
            total_energy += energy

    return -total_energy

res = minimize(evaluate_threshold, x0=[0.5], args=('/home/user/sim_data.h5',), method='Nelder-Mead', options={'xatol': 1e-8, 'fatol': 1e-8})
print(f"{res.x[0]:.4f}")
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_analyze_script_fixed():
    """Check if analyze.py was modified to remove the non-deterministic set() operation."""
    file_path = "/home/user/analyze.py"
    assert os.path.isfile(file_path), f"Expected script {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "set(f.keys())" not in content, "The script still contains the non-deterministic `set(f.keys())` operation."
    assert "sorted" in content or "list(f" in content, "The script does not appear to sort or deterministically order the nodes."

def test_answer_file_correct():
    """Check if answer.txt contains the correct reproducible optimized threshold."""
    answer_path = "/home/user/answer.txt"
    assert os.path.isfile(answer_path), f"Expected answer file {answer_path} is missing."

    with open(answer_path, "r") as f:
        answer_text = f.read().strip()

    expected_val = get_expected_value()

    assert answer_text == expected_val, f"Incorrect optimized threshold in {answer_path}. Expected {expected_val}, got {answer_text}."