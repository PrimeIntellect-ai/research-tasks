# test_final_state.py
import os
import csv
import math

def test_script_exists():
    file_path = "/home/user/simulate_and_process.py"
    assert os.path.exists(file_path), f"The script {file_path} does not exist."

def test_max_error_file():
    file_path = "/home/user/max_error.txt"
    assert os.path.exists(file_path), f"{file_path} does not exist."
    with open(file_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Contents of {file_path} could not be parsed as a float. Got: '{content}'"

    assert math.isclose(val, 0.0342, abs_tol=1e-4), f"Expected max_error.txt to contain '0.0342', but got '{content}'."

def test_validation_results_csv():
    file_path = "/home/user/validation_results.csv"
    assert os.path.exists(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 7, f"Expected 7 rows (1 header + 6 data) in CSV, got {len(rows)}."

    header = rows[0]
    expected_header = ["gamma", "f_true", "f_peak", "error"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}."

    data_rows = rows[1:]

    gammas = [0.1, 0.5]
    fs = [15.0, 25.0, 35.0]

    expected_combinations = [(g, f) for g in gammas for f in fs]

    for i, (expected_g, expected_f) in enumerate(expected_combinations):
        row = data_rows[i]
        assert len(row) == 4, f"Row {i+1} does not have 4 columns: {row}"

        try:
            g_val = float(row[0])
            f_val = float(row[1])
            f_peak = float(row[2])
            error = float(row[3])
        except ValueError:
            assert False, f"Could not parse numeric values in row {i+1}: {row}"

        assert math.isclose(g_val, expected_g, rel_tol=1e-5), f"Expected gamma {expected_g}, got {g_val}."
        assert math.isclose(f_val, expected_f, rel_tol=1e-5), f"Expected f_true {expected_f}, got {f_val}."

        # Calculate the expected frequency bin
        dt = 2.0 / 1023.0
        df = 1.0 / (1024 * dt)

        if expected_f == 15.0:
            expected_f_peak = 30 * df
        elif expected_f == 25.0:
            expected_f_peak = 50 * df
        elif expected_f == 35.0:
            expected_f_peak = 70 * df
        else:
            expected_f_peak = expected_f

        assert math.isclose(f_peak, expected_f_peak, rel_tol=1e-2), f"Expected f_peak ~{expected_f_peak} for f={expected_f}, got {f_peak}."

        expected_error = abs(expected_f_peak - expected_f)
        assert math.isclose(error, expected_error, rel_tol=1e-2, abs_tol=1e-4), f"Expected error ~{expected_error} for f={expected_f}, got {error}."