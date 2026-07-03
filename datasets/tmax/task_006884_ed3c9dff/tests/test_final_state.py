# test_final_state.py

import os
import csv
import pytest

def test_error_txt_exists_and_valid():
    """Verify /home/user/error.txt exists and contains a valid SSE value."""
    file_path = "/home/user/error.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    try:
        sse = float(content)
    except ValueError:
        pytest.fail(f"Content of {file_path} is not a valid float: {content}")

    assert 0.8 <= sse <= 1.1, f"Expected SSE to be between 0.8 and 1.1, but got {sse}"

def test_posterior_samples_exists_and_format():
    """Verify /home/user/posterior_samples.csv exists, has correct header and row count."""
    file_path = "/home/user/posterior_samples.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["a", "b"], f"Expected header ['a', 'b'], got {header}"

        rows = list(reader)
        assert len(rows) == 500, f"Expected exactly 500 data rows, but got {len(rows)}"

def test_posterior_samples_values():
    """Verify the means of the posterior samples are within the expected ranges."""
    file_path = "/home/user/posterior_samples.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    a_vals = []
    b_vals = []

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            try:
                a_vals.append(float(row["a"]))
                b_vals.append(float(row["b"]))
            except (ValueError, KeyError) as e:
                pytest.fail(f"Error parsing row {i+1} in {file_path}: {e}")

    assert len(a_vals) > 0, "No data found in posterior_samples.csv"

    a_mean = sum(a_vals) / len(a_vals)
    b_mean = sum(b_vals) / len(b_vals)

    assert 0.45 <= a_mean <= 0.55, f"Mean of 'a' ({a_mean}) is outside expected range [0.45, 0.55]"
    assert 3.10 <= b_mean <= 3.18, f"Mean of 'b' ({b_mean}) is outside expected range [3.10, 3.18]"