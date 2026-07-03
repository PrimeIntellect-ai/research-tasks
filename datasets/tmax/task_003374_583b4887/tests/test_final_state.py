# test_final_state.py

import os
import csv
import pytest

def test_optimized_results_exists():
    file_path = "/home/user/optimized_results.csv"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_optimized_results_content():
    file_path = "/home/user/optimized_results.csv"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    expected_results = {
        "seq_1": 1.7361,
        "seq_2": 2.2222,
        "seq_3": 1.3333,
        "seq_4": 1.2963,
        "seq_5": 4.4000
    }

    parsed_results = {}
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "optimized_results.csv is empty."
        assert header == ["SeqID", "Optimal_d"], f"Incorrect header in optimized_results.csv. Expected ['SeqID', 'Optimal_d'], got {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Row {row} does not have exactly 2 columns."
            seq_id, optimal_d = row
            try:
                parsed_results[seq_id] = float(optimal_d)
            except ValueError:
                pytest.fail(f"Could not parse Optimal_d value '{optimal_d}' for {seq_id} as a float.")

    assert len(parsed_results) == len(expected_results), f"Expected {len(expected_results)} results, found {len(parsed_results)}."

    for seq_id, expected_d in expected_results.items():
        assert seq_id in parsed_results, f"Missing result for {seq_id}."
        actual_d = parsed_results[seq_id]
        assert abs(actual_d - expected_d) < 1e-3, f"Incorrect Optimal_d for {seq_id}. Expected {expected_d}, got {actual_d}."