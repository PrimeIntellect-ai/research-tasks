# test_final_state.py
import os
import csv
import math

def test_results_csv_exists():
    """Check if the results.csv file was created."""
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Expected results file {results_path} does not exist."

def test_results_csv_content():
    """Validate the contents of results.csv against expected diffusion results."""
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Expected results file {results_path} does not exist."

    expected = {
        0.1: 0.05260840134447475,
        0.2: 0.07629088689726887,
        0.25: -1.0,
        0.3: -1.0
    }

    actual_results = {}
    with open(results_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            assert len(row) == 2, f"Expected 2 columns in CSV row, found {len(row)}: {row}"
            try:
                alpha = float(row[0])
                dist = float(row[1])
            except ValueError:
                assert False, f"Could not parse row values as floats: {row}"
            actual_results[alpha] = dist

    assert len(actual_results) == 4, f"Expected exactly 4 rows in CSV, found {len(actual_results)}"

    for alpha, expected_dist in expected.items():
        assert actual_results.get(alpha) is not None, f"Missing result for alpha = {alpha}"
        actual_dist = actual_results[alpha]
        assert math.isclose(actual_dist, expected_dist, rel_tol=1e-5), \
            f"Incorrect distance for alpha={alpha}. Expected {expected_dist}, got {actual_dist}"

def test_script_exists():
    """Check if the Python script was created at the expected path."""
    script_path = "/home/user/diffusion_mpi.py"
    assert os.path.isfile(script_path), f"Expected MPI script {script_path} does not exist."