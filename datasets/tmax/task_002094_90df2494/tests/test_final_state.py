# test_final_state.py
import os
import math
import re
import pytest

def get_particles():
    path = "/home/user/particles.csv"
    particles = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            particles.append({
                'id': int(parts[0]),
                'x': float(parts[1]),
                'y': float(parts[2]),
                'z': float(parts[3]),
                'q': float(parts[4])
            })
    return particles

def compute_expected_edges(particles):
    edges = []
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            if p1['id'] >= p2['id']:
                continue
            dx = p1['x'] - p2['x']
            dy = p1['y'] - p2['y']
            dz = p1['z'] - p2['z']
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < 4.0:
                energy = (p1['q'] * p2['q']) / dist
                edges.append((p1['id'], p2['id'], round(energy, 4)))
    # Sort by ID_i, then ID_j
    edges.sort(key=lambda e: (e[0], e[1]))
    return edges

def test_step1_pairwise_and_edges():
    script_path = "/home/user/step1_pairwise.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    edges_path = "/home/user/edges.csv"
    assert os.path.isfile(edges_path), f"Missing {edges_path}"

    particles = get_particles()
    expected_edges = compute_expected_edges(particles)

    actual_edges = []
    with open(edges_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            actual_edges.append((int(parts[0]), int(parts[1]), float(parts[2])))

    # Sort actual edges to be lenient on order for this specific test, 
    # though the task implies pairwise generation order.
    actual_edges.sort(key=lambda e: (e[0], e[1]))

    assert len(actual_edges) == len(expected_edges), f"Expected {len(expected_edges)} edges, got {len(actual_edges)}"
    for act, exp in zip(actual_edges, expected_edges):
        assert act[0] == exp[0] and act[1] == exp[1], f"Edge ID mismatch: {act} vs {exp}"
        assert math.isclose(act[2], exp[2], abs_tol=1e-4), f"Energy mismatch for edge {act[0]}-{act[1]}: expected {exp[2]}, got {act[2]}"

def test_total_energy_fixed():
    script_path = "/home/user/total_energy.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # Check that sorting is applied before awk
    assert "sort" in content, "The script /home/user/total_energy.sh does not use 'sort' to fix the reduction order."

    # Check total_fixed.txt
    fixed_path = "/home/user/total_fixed.txt"
    assert os.path.isfile(fixed_path), f"Missing {fixed_path}"

    # Compute expected fixed total
    particles = get_particles()
    expected_edges = compute_expected_edges(particles)
    expected_edges.sort(key=lambda e: (e[0], e[1]))

    total = 0.0
    for e in expected_edges:
        total += e[2]
        total = int(total * 100) / 100.0

    with open(fixed_path, "r") as f:
        fixed_content = f.read().strip()

    expected_str = f"Total Energy: {total:.2f}"
    assert expected_str in fixed_content, f"Expected '{expected_str}' in {fixed_path}, got '{fixed_content}'"

def test_step3_bootstrap_and_ci():
    script_path = "/home/user/step3_bootstrap.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    ci_path = "/home/user/ci.txt"
    assert os.path.isfile(ci_path), f"Missing {ci_path}"

    with open(ci_path, "r") as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) == 2, f"Expected 2 lines in {ci_path}, got {len(lines)}"

    assert lines[0].startswith("Lower: "), "First line must start with 'Lower: '"
    assert lines[1].startswith("Upper: "), "Second line must start with 'Upper: '"

    lower_val = lines[0].split("Lower: ")[1].strip()
    upper_val = lines[1].split("Upper: ")[1].strip()

    try:
        lower_f = float(lower_val)
        upper_f = float(upper_val)
    except ValueError:
        pytest.fail("Lower and Upper values in ci.txt must be numeric.")

    assert lower_f <= upper_f, "Lower bound should be less than or equal to Upper bound."