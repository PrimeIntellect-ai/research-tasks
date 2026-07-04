# test_final_state.py

import os
import subprocess
import pytest
import math

def test_executable_exists():
    """Check if the C program was compiled to the correct location and is executable."""
    exe_path = "/home/user/bin/ca_centroid"
    assert os.path.isfile(exe_path), f"Executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_mode_output_exists_and_format():
    """Check if the results file exists and has the correct format."""
    output_path = "/home/user/results/mode_output.txt"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 2, f"Output file should contain exactly two values separated by a comma, got: {content}"

    try:
        dist = float(parts[0])
        dens = float(parts[1])
    except ValueError:
        pytest.fail(f"Output values must be valid floats, got: {content}")

def test_correct_mode_and_density():
    """Recompute the expected distance and density, and verify the student's output."""
    # We use a subprocess to run the scipy computation since we are restricted to stdlib in the test file,
    # but the student environment must have scipy installed for the task.
    script = """
import os
import subprocess
import numpy as np
from scipy.stats import gaussian_kde
from scipy.optimize import minimize

# Compile a fresh copy to ensure correctness
subprocess.run(["gcc", "-O3", "/home/user/src/ca_centroid.c", "-o", "/tmp/ca_centroid_test", "-lm"], check=True)

pdbs = sorted([f for f in os.listdir("/home/user/data/pdbs") if f.endswith(".pdb")])
distances = []
for p in pdbs:
    res = subprocess.run(["/tmp/ca_centroid_test", os.path.join("/home/user/data/pdbs", p)], capture_output=True, text=True, check=True)
    distances.append(float(res.stdout.strip()))

distances = np.array(distances)
kde = gaussian_kde(distances)

def neg_kde(x):
    return -kde(x)[0]

res = minimize(neg_kde, x0=[np.mean(distances)], bounds=[(0, 100)])
print(f"{res.x[0]:.4f},{(-res.fun):.4f}")
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute expected values: {result.stderr}"

    expected_output = result.stdout.strip()
    expected_parts = expected_output.split(",")
    expected_dist = float(expected_parts[0])
    expected_dens = float(expected_parts[1])

    output_path = "/home/user/results/mode_output.txt"
    with open(output_path, "r") as f:
        student_content = f.read().strip()

    student_parts = student_content.split(",")
    student_dist = float(student_parts[0])
    student_dens = float(student_parts[1])

    assert math.isclose(student_dist, expected_dist, abs_tol=1e-3), \
        f"Expected distance ~{expected_dist:.4f}, but got {student_dist:.4f}"

    assert math.isclose(student_dens, expected_dens, abs_tol=1e-3), \
        f"Expected density ~{expected_dens:.4f}, but got {student_dens:.4f}"