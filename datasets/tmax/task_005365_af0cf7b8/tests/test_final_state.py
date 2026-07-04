# test_final_state.py

import os
import pytest

def read_spectrum(filepath):
    """Reads a spectrum file and returns a dictionary of frequency -> probability."""
    spectrum = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 2:
                freq, prob = parts[0], float(parts[1])
                spectrum[freq] = prob
    return spectrum

def calculate_tvd(p, q):
    """Calculates the Total Variation Distance between two probability distributions."""
    tvd = 0.0
    all_keys = set(p.keys()).union(set(q.keys()))
    for k in all_keys:
        p_val = p.get(k, 0.0)
        q_val = q.get(k, 0.0)
        tvd += abs(p_val - q_val)
    return tvd / 2.0

def test_accepted_machines_log_correctness():
    baseline_path = "/home/user/baseline_spectrum.txt"
    candidates_dir = "/home/user/candidates"
    output_log_path = "/home/user/accepted_machines.log"

    assert os.path.exists(baseline_path), f"Baseline file missing at {baseline_path}"
    assert os.path.exists(candidates_dir), f"Candidates directory missing at {candidates_dir}"
    assert os.path.exists(output_log_path), f"Output log file missing at {output_log_path}"

    baseline_spectrum = read_spectrum(baseline_path)

    expected_accepted = []

    for filename in os.listdir(candidates_dir):
        if not filename.endswith('.txt'):
            continue

        candidate_path = os.path.join(candidates_dir, filename)
        candidate_spectrum = read_spectrum(candidate_path)

        tvd = calculate_tvd(baseline_spectrum, candidate_spectrum)

        if tvd <= 0.15:
            machine_name = filename[:-4] # remove .txt
            expected_accepted.append(machine_name)

    expected_accepted.sort()

    with open(output_log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_accepted, (
        f"The contents of {output_log_path} do not match the expected accepted machines.\n"
        f"Expected: {expected_accepted}\n"
        f"Found: {actual_lines}"
    )