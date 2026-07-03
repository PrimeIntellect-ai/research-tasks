# test_final_state.py

import os
import math
import re

class LCG:
    def __init__(self, seed=12345):
        self.state = seed

    def next_rand(self):
        self.state = (self.state * 1103515245 + 12345) & 0x7FFFFFFF
        return self.state

def compute_expected_stats(pdb_path):
    with open(pdb_path, "r") as f:
        lines = f.readlines()

    atoms = []
    for line in lines:
        if line.startswith("ATOM  "):
            try:
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                atoms.append((x, y, z))
            except ValueError:
                # Fallback to simple split if fixed-width parsing fails
                parts = line.split()
                # Find the first float-like token after ATOM and index
                # Usually columns 6, 7, 8 in 0-indexed split for this specific file
                x, y, z = float(parts[5]), float(parts[6]), float(parts[7])
                atoms.append((x, y, z))

    edges = []
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            dx = atoms[i][0] - atoms[j][0]
            dy = atoms[i][1] - atoms[j][1]
            dz = atoms[i][2] - atoms[j][2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            # strictly greater than 0.0 and less than or equal to 1.8
            if 0.0 < dist <= 1.8:
                edges.append(dist)

    n_atoms = len(atoms)
    n_edges = len(edges)
    mean_edge = sum(edges) / n_edges if n_edges > 0 else 0.0

    lcg = LCG()
    means = []
    for _ in range(10000):
        sample_sum = 0.0
        for _ in range(n_edges):
            idx = lcg.next_rand() % n_edges
            sample_sum += edges[idx]
        means.append(sample_sum / n_edges)

    means.sort()
    ci_lower = means[250] if n_edges > 0 else 0.0
    ci_upper = means[9749] if n_edges > 0 else 0.0

    return n_atoms, n_edges, mean_edge, ci_lower, ci_upper

def test_c_source_exists():
    assert os.path.isfile("/home/user/process_pdb.c"), "The C source file /home/user/process_pdb.c is missing."

def test_executable_exists():
    assert os.path.isfile("/home/user/process_pdb"), "The executable /home/user/process_pdb is missing."
    assert os.access("/home/user/process_pdb", os.X_OK), "The file /home/user/process_pdb is not executable."

def test_graph_stats_output():
    stats_path = "/home/user/graph_stats.txt"
    assert os.path.isfile(stats_path), f"The output file {stats_path} is missing."

    pdb_path = "/home/user/data.pdb"
    assert os.path.isfile(pdb_path), f"The input file {pdb_path} is missing."

    exp_atoms, exp_edges, exp_mean, exp_ci_lower, exp_ci_upper = compute_expected_stats(pdb_path)

    with open(stats_path, "r") as f:
        content = f.read().strip()

    lines = content.split('\n')
    parsed_stats = {}
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            parsed_stats[key.strip()] = val.strip()

    assert "Atoms" in parsed_stats, "Output is missing 'Atoms' field."
    assert int(parsed_stats["Atoms"]) == exp_atoms, f"Expected {exp_atoms} atoms, got {parsed_stats['Atoms']}."

    assert "Edges" in parsed_stats, "Output is missing 'Edges' field."
    assert int(parsed_stats["Edges"]) == exp_edges, f"Expected {exp_edges} edges, got {parsed_stats['Edges']}."

    assert "Mean" in parsed_stats, "Output is missing 'Mean' field."
    assert math.isclose(float(parsed_stats["Mean"]), exp_mean, abs_tol=1e-4), f"Expected Mean ~{exp_mean:.4f}, got {parsed_stats['Mean']}."

    assert "CI_Lower" in parsed_stats, "Output is missing 'CI_Lower' field."
    assert math.isclose(float(parsed_stats["CI_Lower"]), exp_ci_lower, abs_tol=1e-4), f"Expected CI_Lower ~{exp_ci_lower:.4f}, got {parsed_stats['CI_Lower']}."

    assert "CI_Upper" in parsed_stats, "Output is missing 'CI_Upper' field."
    assert math.isclose(float(parsed_stats["CI_Upper"]), exp_ci_upper, abs_tol=1e-4), f"Expected CI_Upper ~{exp_ci_upper:.4f}, got {parsed_stats['CI_Upper']}."