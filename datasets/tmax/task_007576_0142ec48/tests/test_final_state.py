# test_final_state.py
import os
import csv
import math
import random

def simulate_mutations(args):
    seq, seed = args
    random.seed(seed)
    energy = len(seq) * 0.01
    for _ in range(100):
        energy += random.uniform(-0.1, 0.1) * math.pi
    return energy

def get_expected_energy_truth(seq, num_trials=500):
    args = [(seq, i) for i in range(num_trials)]
    results = list(map(simulate_mutations, args))
    return math.fsum(results) / num_trials

def test_mc_energy_fixed():
    path = "/home/user/mc_energy.py"
    assert os.path.exists(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "imap_unordered" not in content, "mc_energy.py still contains 'imap_unordered'."
    assert "fsum" in content, "mc_energy.py must use math.fsum() for summation."

def test_generate_data_script_exists():
    path = "/home/user/generate_data.py"
    assert os.path.exists(path), f"File missing: {path}"

def test_visualization_exists():
    path = "/home/user/visualization.png"
    assert os.path.exists(path), f"File missing: {path}"
    assert os.path.getsize(path) > 0, "Visualization image is empty."

def test_training_dataset():
    path = "/home/user/training_dataset.csv"
    assert os.path.exists(path), f"File missing: {path}"

    random.seed(42)
    expected_sequences = [''.join(random.choices("ACGT", k=50)) for _ in range(100)]

    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["Sequence", "Energy"], "CSV header must be Sequence,Energy"

        rows = list(reader)

    assert len(rows) == 100, f"Expected 100 rows in CSV, got {len(rows)}"

    for i, row in enumerate(rows):
        assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns."
        seq, energy_str = row
        assert seq == expected_sequences[i], f"Sequence at row {i+1} is incorrect."

        expected_energy = get_expected_energy_truth(seq)
        try:
            energy_val = float(energy_str)
        except ValueError:
            assert False, f"Energy value at row {i+1} is not a valid float: {energy_str}"

        assert math.isclose(energy_val, expected_energy, rel_tol=1e-12), \
            f"Energy value at row {i+1} is incorrect. Expected ~{expected_energy}, got {energy_val}."