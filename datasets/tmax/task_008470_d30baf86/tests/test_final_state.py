# test_final_state.py

import os
import json
import subprocess
import pytest

def get_truth():
    """
    Computes the exact expected output by using a fast pure-Python sliding window
    and the exact same ODE solver from scipy as the original script.
    We run this via subprocess to adhere to the standard-library-only rule for the test file.
    """
    script = """
import json
from scipy.integrate import solve_ivp

def decay_ode(t, y, k):
    return -k * y

def read_fasta(file_path):
    seqs = {}
    with open(file_path, 'r') as f:
        curr_id = ""
        curr_seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if curr_id:
                    seqs[curr_id] = "".join(curr_seq)
                curr_id = line[1:]
                curr_seq = []
            else:
                curr_seq.append(line)
        if curr_id:
            seqs[curr_id] = "".join(curr_seq)
    return seqs

seqs = read_fasta('/home/user/profiler_test/reads.fasta')
results = {}
for seq_id, seq in seqs.items():
    window = 100
    n = len(seq)
    if n < window:
        results[seq_id] = "0.00000"
        continue

    # Fast sliding window in pure Python
    gc_count = sum(1 for base in seq[:window] if base in "GC")
    max_gc_count = gc_count
    for i in range(1, n - window + 1):
        if seq[i - 1] in "GC":
            gc_count -= 1
        if seq[i + window - 1] in "GC":
            gc_count += 1
        if gc_count > max_gc_count:
            max_gc_count = gc_count

    max_gc = max_gc_count / window
    sol = solve_ivp(decay_ode, [0, 10], [100.0], args=(max_gc,))
    results[seq_id] = f"{sol.y[0][-1]:.5f}"

print(json.dumps(results))
"""
    out = subprocess.check_output(["python3", "-c", script])
    return json.loads(out)

def test_process_optimized_exists_and_uses_numpy():
    opt_path = "/home/user/profiler_test/process_optimized.py"
    assert os.path.isfile(opt_path), f"Optimized script {opt_path} does not exist."

    with open(opt_path, "r") as f:
        content = f.read()

    assert "import numpy" in content or "import numpy as np" in content, \
        "The optimized script must import and use numpy for vectorization."

def test_final_concentrations_csv_correctness():
    csv_path = "/home/user/profiler_test/final_concentrations.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "The CSV file is empty."
    assert lines[0] == "SeqID,Final_C", f"CSV header is incorrect. Expected 'SeqID,Final_C', got '{lines[0]}'"

    truth = get_truth()

    assert len(lines) - 1 == len(truth), f"Expected {len(truth)} data rows, found {len(lines) - 1}."

    for line in lines[1:]:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid CSV line format: {line}"
        seq_id, final_c = parts

        assert seq_id in truth, f"Unexpected SeqID found in CSV: {seq_id}"
        expected_c = truth[seq_id]
        assert final_c == expected_c, \
            f"Incorrect Final_C for {seq_id}. Expected {expected_c}, got {final_c}. " \
            "Make sure the values are rounded to 5 decimal places and match the original script's output."