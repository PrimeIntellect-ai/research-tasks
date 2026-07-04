# test_final_state.py

import os
import re

def test_profile_txt_exists_and_completed():
    """Check if profile.txt exists and contains COMPLETED."""
    profile_path = "/home/user/profile.txt"
    assert os.path.isfile(profile_path), f"{profile_path} is missing."
    with open(profile_path, "r") as f:
        content = f.read()
    assert "COMPLETED" in content, f"'COMPLETED' not found in {profile_path}."

def test_regression_results():
    """Check if regression_results.txt contains the correct derived slope and intercept."""
    pdb_path = "/home/user/data/input.pdb"
    assert os.path.isfile(pdb_path), f"{pdb_path} is missing."

    x_vals = []
    y_raw = []

    # Parse PDB for CA atoms
    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16] == " CA ":
                res_seq = int(line[22:26].strip())
                b_factor = float(line[60:66].strip())
                x_vals.append(res_seq)
                y_raw.append(b_factor)

    assert len(x_vals) > 0, "No CA atoms found in PDB file."

    # Apply SMA with window size 5
    n = len(y_raw)
    y_smoothed = []
    for i in range(n):
        start = max(0, i - 2)
        end = min(n, i + 3)
        window = y_raw[start:end]
        y_smoothed.append(sum(window) / len(window))

    # Linear regression
    x_mean = sum(x_vals) / n
    y_mean = sum(y_smoothed) / n

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_smoothed))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)

    expected_slope = numerator / denominator
    expected_intercept = y_mean - expected_slope * x_mean

    results_path = "/home/user/regression_results.txt"
    assert os.path.isfile(results_path), f"{results_path} is missing."

    with open(results_path, "r") as f:
        content = f.read()

    slope_match = re.search(r"Slope:\s*(-?\d+\.\d+)", content)
    intercept_match = re.search(r"Intercept:\s*(-?\d+\.\d+)", content)

    assert slope_match is not None, "Could not parse Slope from regression_results.txt"
    assert intercept_match is not None, "Could not parse Intercept from regression_results.txt"

    actual_slope = float(slope_match.group(1))
    actual_intercept = float(intercept_match.group(1))

    assert abs(actual_slope - expected_slope) < 1e-3, f"Expected slope {expected_slope:.4f}, got {actual_slope}"
    assert abs(actual_intercept - expected_intercept) < 1e-3, f"Expected intercept {expected_intercept:.4f}, got {actual_intercept}"