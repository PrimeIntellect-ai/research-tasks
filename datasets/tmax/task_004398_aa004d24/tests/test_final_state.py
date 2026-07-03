# test_final_state.py

import os
import csv
import math
import pytest

def test_script_exists():
    """Check if the generate_data.py script exists."""
    script_path = "/home/user/generate_data.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()
        assert "validate_solver" in content, "The script must define a validate_solver() function."
        assert "Regression Test Passed" in content, "The script must print 'Regression Test Passed'."

def test_csv_output_exists_and_format():
    """Check if training_data.csv exists and has the correct headers."""
    csv_path = "/home/user/training_data.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"{csv_path} is empty.")

        expected_headers = ["network_id", "node_id", "concentration"]
        assert headers == expected_headers, f"Headers in {csv_path} do not match expected: {expected_headers}"

def test_csv_output_values():
    """Validate the calculated concentrations in the CSV output."""
    csv_path = "/home/user/training_data.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    # Compute expected values analytically
    # net1
    # G1(t) = 100 * exp(-0.1*t)
    expected_g1 = 100 * math.exp(-5)
    # G2(t) = 500 * (exp(-0.1*t) - exp(-0.2*t))
    expected_g2 = 500 * (math.exp(-5) - math.exp(-10))

    # net2
    # A(t) = 50 * exp(-0.05*t)
    expected_a = 50 * math.exp(-2.5)
    # B(t) = 200 * exp(-0.05*t) - 190 * exp(-0.1*t)
    expected_b = 200 * math.exp(-2.5) - 190 * math.exp(-5)

    expected_data = [
        ("net1", "G1", f"{expected_g1:.4f}"),
        ("net1", "G2", f"{expected_g2:.4f}"),
        ("net2", "A", f"{expected_a:.4f}"),
        ("net2", "B", f"{expected_b:.4f}")
    ]

    actual_data = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) == 3:
                actual_data.append(tuple(row))

    # The rows should be sorted alphabetically by network_id, then by node_id
    assert actual_data == expected_data, f"CSV data does not match the expected values or sorting.\nExpected: {expected_data}\nActual: {actual_data}"