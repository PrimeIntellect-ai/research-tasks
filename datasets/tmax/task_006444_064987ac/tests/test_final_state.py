# test_final_state.py

import os
import pytest

def test_engineered_csv():
    """Test the feature engineering output."""
    sensor_path = "/home/user/sensor_data.csv"
    engineered_path = "/home/user/engineered.csv"

    assert os.path.isfile(engineered_path), f"File {engineered_path} does not exist."
    assert os.path.isfile(sensor_path), f"File {sensor_path} does not exist."

    with open(sensor_path, "r") as f:
        sensor_lines = f.read().strip().splitlines()

    assert len(sensor_lines) > 1, "sensor_data.csv is empty or missing data."
    header = sensor_lines[0].split(',')

    # Extract v1 values to find max
    v1_idx = header.index("v1")
    v2_idx = header.index("v2")
    v1_values = [float(line.split(',')[v1_idx]) for line in sensor_lines[1:]]
    max_v1 = max(v1_values)

    with open(engineered_path, "r") as f:
        eng_lines = f.read().strip().splitlines()

    assert len(eng_lines) == len(sensor_lines), "engineered.csv does not have the same number of rows as sensor_data.csv"
    assert eng_lines[0] == "id,v1,v2,v1_norm,v_diff", f"Incorrect header in engineered.csv: {eng_lines[0]}"

    for i in range(1, len(sensor_lines)):
        s_parts = sensor_lines[i].split(',')
        e_parts = eng_lines[i].split(',')

        assert len(e_parts) == 5, f"Row {i} in engineered.csv does not have 5 columns."
        assert e_parts[0:3] == s_parts[0:3], f"Row {i} original columns do not match."

        v1 = float(s_parts[v1_idx])
        v2 = float(s_parts[v2_idx])

        expected_v1_norm = f"{v1 / max_v1:.4f}"
        expected_v_diff = f"{v2 - v1:.4f}"

        assert e_parts[3] == expected_v1_norm, f"Row {i} v1_norm mismatch: expected {expected_v1_norm}, got {e_parts[3]}"
        assert e_parts[4] == expected_v_diff, f"Row {i} v_diff mismatch: expected {expected_v_diff}, got {e_parts[4]}"


def test_bootstrap_means():
    """Test the bootstrap_means.txt file."""
    means_path = "/home/user/bootstrap_means.txt"
    assert os.path.isfile(means_path), f"File {means_path} does not exist."

    with open(means_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 100, f"bootstrap_means.txt should have exactly 100 lines, but has {len(lines)}."

    # Ensure all lines are valid floats
    for i, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line {i+1} in bootstrap_means.txt is not a valid number: {line}")


def test_confidence_interval():
    """Test the confidence_interval.txt file based on bootstrap_means.txt."""
    means_path = "/home/user/bootstrap_means.txt"
    ci_path = "/home/user/confidence_interval.txt"

    assert os.path.isfile(ci_path), f"File {ci_path} does not exist."
    assert os.path.isfile(means_path), f"File {means_path} does not exist."

    with open(means_path, "r") as f:
        means = [float(line) for line in f.read().strip().splitlines()]

    assert len(means) == 100, "bootstrap_means.txt does not have 100 valid numbers."

    sorted_means = sorted(means)

    with open(ci_path, "r") as f:
        ci_lines = f.read().strip().splitlines()

    assert len(ci_lines) == 2, f"confidence_interval.txt should have exactly 2 lines, got {len(ci_lines)}."

    try:
        lower = float(ci_lines[0])
        upper = float(ci_lines[1])
    except ValueError:
        pytest.fail("confidence_interval.txt contains non-numeric values.")

    expected_lower = sorted_means[2] # 3rd value (index 2)
    expected_upper = sorted_means[97] # 98th value (index 97)

    # Check bounds with a small tolerance in case of string parsing differences
    assert abs(lower - expected_lower) < 1e-4, f"Lower bound mismatch: expected {expected_lower}, got {lower}"
    assert abs(upper - expected_upper) < 1e-4, f"Upper bound mismatch: expected {expected_upper}, got {upper}"