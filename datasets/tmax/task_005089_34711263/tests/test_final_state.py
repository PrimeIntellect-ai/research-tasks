# test_final_state.py

import os
import math
import pytest

def test_rust_project_exists():
    project_dir = "/home/user/bio_divergence"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory is missing at {project_dir}"
    assert os.path.isfile(cargo_toml), f"Cargo.toml is missing in {project_dir}, ensuring it is a valid Rust project"

def test_kl_divergence_output():
    fasta_path = "/home/user/input.fasta"
    csv_path = "/home/user/background.csv"
    output_path = "/home/user/kl_divergence.txt"

    assert os.path.isfile(output_path), f"Output file is missing at {output_path}"

    # Compute ground truth dynamically based on the input files
    std_aas = set("ACDEFGHIKLMNPQRSTVWY")
    counts = {aa: 1 for aa in std_aas}  # Add-one smoothing base

    # Read FASTA
    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith(">"):
                for char in line:
                    if char in std_aas:
                        counts[char] += 1

    total_count = sum(counts.values())
    p = {aa: count / total_count for aa, count in counts.items()}

    # Read CSV
    q = {}
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(',')
                aa = parts[0].strip()
                prob = float(parts[1].strip())
                if aa in std_aas:
                    q[aa] = prob

    # Calculate KL divergence
    kl = 0.0
    for aa in std_aas:
        if p[aa] > 0 and q[aa] > 0:
            kl += p[aa] * math.log(p[aa] / q[aa])

    expected_val = f"{kl:.4f}"

    # Read actual output
    with open(output_path, 'r') as f:
        actual_val = f.read().strip()

    assert actual_val == expected_val, f"Expected KL divergence to be '{expected_val}', but got '{actual_val}'"