# test_final_state.py

import os
import math
import pytest

def compute_expected_kl(pdb_path):
    # Parse CA atoms
    ca_coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM  ") or line.startswith("HETATM"):
                atom_name = line[12:16].strip()
                if atom_name == "CA":
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    ca_coords.append((x, y, z))

    # Compute pairwise distances
    distances = []
    n = len(ca_coords)
    for i in range(n):
        for j in range(i + 1, n):
            c1 = ca_coords[i]
            c2 = ca_coords[j]
            dist = math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)
            distances.append(dist)

    # Build histogram
    histogram = [0] * 100
    total_pairs = 0
    for d in distances:
        if d < 100.0:
            bin_idx = int(math.floor(d))
            if 0 <= bin_idx < 100:
                histogram[bin_idx] += 1
                total_pairs += 1

    # Calculate KL divergence
    if total_pairs == 0:
        return 0.0

    kl_div = 0.0
    q = 0.01
    for count in histogram:
        if count > 0:
            p = count / total_pairs
            kl_div += p * math.log(p / q)

    return kl_div

def test_c_source_exists():
    assert os.path.isfile('/home/user/spectro_profile.c'), "/home/user/spectro_profile.c does not exist."

def test_kl_divergence_output():
    output_file = '/home/user/kl_divergence.txt'
    pdb_file = '/home/user/input.pdb'

    assert os.path.isfile(output_file), f"{output_file} does not exist. Did the program run successfully?"
    assert os.path.isfile(pdb_file), f"{pdb_file} is missing."

    expected_kl = compute_expected_kl(pdb_file)
    expected_str = f"{expected_kl:.6f}"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content == expected_str, f"Expected KL divergence {expected_str}, but got {content} in {output_file}."