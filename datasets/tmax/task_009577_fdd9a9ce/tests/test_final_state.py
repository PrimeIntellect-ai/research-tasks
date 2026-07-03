# test_final_state.py
import os
import csv

def test_results_csv_exists():
    path = "/home/user/results.csv"
    assert os.path.isfile(path), f"Results file {path} does not exist. The task requires generating this file."

def test_results_csv_content():
    path = "/home/user/results.csv"
    assert os.path.isfile(path), f"Results file {path} does not exist."

    with open(path, "r", newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"Results file {path} is empty."

        assert header == ["Sequence_ID", "Root_X"], \
            f"Expected header ['Sequence_ID', 'Root_X'], but got {header}."

        results = {}
        for row in reader:
            assert len(row) == 2, f"Expected 2 columns in row, got {len(row)}: {row}"
            results[row[0].strip()] = row[1].strip()

    expected_results = {
        "seq1_match": "1.0850",
        "seq3_match": "1.7288",
        "seq5_match": "1.2384"
    }

    assert len(results) == len(expected_results), \
        f"Expected exactly {len(expected_results)} result rows, but got {len(results)}."

    for seq_id, expected_val in expected_results.items():
        assert seq_id in results, f"Expected sequence ID '{seq_id}' not found in results."

        actual_val = results[seq_id]
        try:
            actual_float = float(actual_val)
            expected_float = float(expected_val)
            # Check string representation for exact 4 decimal places rounding if needed,
            # but comparing floats with a small tolerance is safer while also checking string format.
            assert abs(actual_float - expected_float) < 1e-4, \
                f"For {seq_id}, expected Root_X near {expected_val}, got {actual_val}."

            # Check if it's rounded to 4 decimal places
            assert len(actual_val.split('.')[-1]) == 4 or actual_val == expected_val, \
                f"For {seq_id}, expected Root_X to be rounded to 4 decimal places (e.g., {expected_val}), got {actual_val}."
        except ValueError:
            assert False, f"Invalid numeric value for {seq_id}: {actual_val}"