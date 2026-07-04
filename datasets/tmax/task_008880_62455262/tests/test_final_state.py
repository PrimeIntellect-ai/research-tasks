# test_final_state.py
import os
import csv

def test_validation_results_exists():
    path = "/home/user/validation_results.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

def test_validation_results_content():
    path = "/home/user/validation_results.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The validation_results.csv file is empty."
    assert rows[0] == ["record_id", "status", "max_similarity"], f"Incorrect CSV header: {rows[0]}"

    # Expected values based on the deterministic TF-IDF and cosine similarity calculations
    # using default parameters and the provided golden/incoming records.
    expected_rows = [
        ["0", "VALID", "0.1873"],
        ["1", "VALID", "0.0000"],
        ["2", "VALID", "0.2222"],
        ["3", "VALID", "0.0000"],
        ["4", "VALID", "0.3848"],
        ["5", "VALID", "0.0000"],
        ["6", "VALID", "0.3015"],
    ]

    assert len(rows) - 1 == len(expected_rows), f"Expected {len(expected_rows)} data rows, but found {len(rows) - 1}."

    for i, (actual, expected) in enumerate(zip(rows[1:], expected_rows)):
        assert len(actual) == 3, f"Row {i+1} does not have exactly 3 columns: {actual}"
        assert actual[0] == expected[0], f"Row {i+1}: expected record_id {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1}: expected status {expected[1]}, got {actual[1]}"

        # Check similarity formatting and value
        try:
            actual_sim = float(actual[2])
            expected_sim = float(expected[2])
        except ValueError:
            pytest.fail(f"Row {i+1}: max_similarity '{actual[2]}' is not a valid float.")

        assert len(actual[2].split('.')[-1]) == 4, f"Row {i+1}: max_similarity '{actual[2]}' must be formatted to exactly 4 decimal places."

        # Allow a tiny margin of error in case of different architecture floating point math, 
        # but string should match up to 4 decimals in most standard environments.
        assert abs(actual_sim - expected_sim) < 0.0002, f"Row {i+1}: expected max_similarity ~{expected[2]}, got {actual[2]}"