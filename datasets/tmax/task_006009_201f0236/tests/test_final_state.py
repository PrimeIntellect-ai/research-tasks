# test_final_state.py

import os
import re
import math
import pytest

def test_executable_exists():
    path = "/home/user/diffusion_sim"
    assert os.path.isfile(path), f"Missing executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_sim_results_exists():
    path = "/home/user/sim_results.csv"
    assert os.path.isfile(path), f"Missing simulation results: {path}"

    with open(path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 10, "sim_results.csv seems to have too few lines."
    assert "Time,SystemEnergy" in lines[0], "Header missing or incorrect in sim_results.csv"

def test_report_content():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"Missing report file: {path}"

    with open(path, "r") as f:
        content = f.read()

    computed_match = re.search(r"Computed Alpha:\s*([0-9.]+)", content)
    reference_match = re.search(r"Reference Alpha:\s*([0-9.]+)", content)
    diff_match = re.search(r"Difference:\s*([0-9.]+)", content)

    assert computed_match is not None, "Could not find 'Computed Alpha: [value]' in report.txt"
    assert reference_match is not None, "Could not find 'Reference Alpha: [value]' in report.txt"
    assert diff_match is not None, "Could not find 'Difference: [value]' in report.txt"

    computed_alpha = float(computed_match.group(1))
    reference_alpha = float(reference_match.group(1))
    difference = float(diff_match.group(1))

    # The reference alpha for Mol_Beta is 1.1716
    assert math.isclose(reference_alpha, 1.1716, abs_tol=0.0001), f"Expected Reference Alpha to be 1.1716, got {reference_alpha}"

    # The computed alpha should be roughly 1.1716
    assert math.isclose(computed_alpha, 1.1716, abs_tol=0.05), f"Computed Alpha {computed_alpha} is not close to the expected ~1.1716"

    # Difference should be correctly calculated
    expected_diff = abs(computed_alpha - reference_alpha)
    assert math.isclose(difference, expected_diff, abs_tol=0.0002), f"Difference is not calculated correctly. Expected {expected_diff}, got {difference}"

def test_diffusion_c_fixed():
    path = "/home/user/diffusion.c"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "dt = dt * 1.5;" not in content, "The buggy adaptive step size logic 'dt = dt * 1.5;' was not removed from diffusion.c"