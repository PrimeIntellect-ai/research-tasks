# test_final_state.py

import os
import json
import math
import pytest

def test_final_state():
    mesh_file = "/home/user/data/mesh.csv"
    output_file = "/home/user/pipeline/output.json"

    assert os.path.isfile(mesh_file), f"Data file {mesh_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    # Read the CSV and extract Q1 and Q4
    q1 = []
    q4 = []
    with open(mesh_file, 'r') as f:
        for row_idx, line in enumerate(f):
            if not line.strip():
                continue
            cols = [float(x) for x in line.strip().split(',')]
            if row_idx < 50:
                q1.extend(cols[:50])
            elif 50 <= row_idx < 100:
                q4.extend(cols[50:100])

    n1 = len(q1)
    n4 = len(q4)

    assert n1 == 2500, f"Expected 2500 elements in Q1, got {n1}"
    assert n4 == 2500, f"Expected 2500 elements in Q4, got {n4}"

    # Calculate statistics
    mean_q1 = sum(q1) / n1
    mean_q4 = sum(q4) / n4

    var_q1 = sum((x - mean_q1) ** 2 for x in q1) / (n1 - 1)
    var_q4 = sum((x - mean_q4) ** 2 for x in q4) / (n4 - 1)

    t_stat = (mean_q1 - mean_q4) / math.sqrt(var_q1 / n1 + var_q4 / n4)

    num = (var_q1 / n1 + var_q4 / n4) ** 2
    den = ((var_q1 / n1) ** 2) / (n1 - 1) + ((var_q4 / n4) ** 2) / (n4 - 1)
    df = num / den

    expected = {
        "mean_q1": mean_q1,
        "mean_q4": mean_q4,
        "var_q1": var_q1,
        "var_q4": var_q4,
        "t_stat": t_stat,
        "df": df
    }

    # Read the generated JSON
    try:
        with open(output_file, 'r') as f:
            actual = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {output_file} is not valid JSON.")

    # Compare expected and actual
    for key, expected_val in expected.items():
        assert key in actual, f"Missing key '{key}' in {output_file}."
        actual_val = actual[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a float."
        assert math.isclose(actual_val, expected_val, rel_tol=1e-4, abs_tol=1e-4), \
            f"Value for '{key}' is incorrect. Expected {expected_val}, got {actual_val}."