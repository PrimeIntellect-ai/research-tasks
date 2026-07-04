# test_final_state.py
import os
import json
import math
import cmath

def get_expected_results():
    fasta_path = '/home/user/input/sequences.fasta'
    sequences = {}
    with open(fasta_path, 'r') as f:
        curr_id = None
        curr_seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if curr_id:
                    sequences[curr_id] = "".join(curr_seq)
                curr_id = line[1:]
                curr_seq = []
            else:
                curr_seq.append(line)
        if curr_id:
            sequences[curr_id] = "".join(curr_seq)

    mapping = {'A': 1.0, 'C': -1.0, 'G': 2.0, 'T': -2.0}
    total_energy = 0.0
    max_energy = -1.0
    max_energy_id = ""

    for seq_id, seq in sequences.items():
        N = len(seq)
        x = [mapping[b] for b in seq]

        # Parseval's theorem: sum(|X[k]|^2) = N * sum(|x[n]|^2)
        sum_sq = sum(v * v for v in x)
        sum_psd = N * sum_sq

        # X[0] = sum(x)
        X0 = sum(x)
        psd_0 = X0**2

        # X[N-1] = sum(x[n] * exp(2j * pi * n / N))
        X_minus_1 = sum(x[n] * cmath.exp(2j * math.pi * n / N) for n in range(N))
        psd_minus_1 = abs(X_minus_1)**2

        # Trapezoidal rule: sum(psd) - 0.5*psd[0] - 0.5*psd[N-1]
        energy = sum_psd - 0.5 * psd_0 - 0.5 * psd_minus_1

        total_energy += energy
        if energy > max_energy:
            max_energy = energy
            max_energy_id = seq_id

    return max_energy_id, round(total_energy, 1)

def test_summary_json_exists_and_valid():
    """Check if summary.json exists and is valid JSON."""
    summary_path = '/home/user/summary.json'
    assert os.path.isfile(summary_path), f"Summary file {summary_path} is missing."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {summary_path} is not a valid JSON."

    assert isinstance(data, dict), "JSON root must be an object (dictionary)."
    assert "max_energy_id" in data, "Missing 'max_energy_id' in JSON."
    assert "total_energy" in data, "Missing 'total_energy' in JSON."
    assert "parallel_workers" in data, "Missing 'parallel_workers' in JSON."

def test_summary_json_values():
    """Verify the computed values in summary.json."""
    summary_path = '/home/user/summary.json'
    with open(summary_path, 'r') as f:
        data = json.load(f)

    expected_max_id, expected_total = get_expected_results()

    assert isinstance(data["parallel_workers"], int), "'parallel_workers' must be an integer."
    assert data["parallel_workers"] >= 4, f"Expected at least 4 parallel workers, got {data['parallel_workers']}."

    assert data["max_energy_id"] == expected_max_id, \
        f"Incorrect max_energy_id. Expected {expected_max_id}, got {data['max_energy_id']}."

    assert isinstance(data["total_energy"], (int, float)), "'total_energy' must be a number."
    assert abs(data["total_energy"] - expected_total) <= 0.1, \
        f"Incorrect total_energy. Expected approx {expected_total}, got {data['total_energy']}."