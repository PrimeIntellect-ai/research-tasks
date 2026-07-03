# test_final_state.py
import os
import csv

def test_recommendations_csv_exists_and_correct():
    csv_path = "/home/user/recommendations.csv"

    assert os.path.exists(csv_path), f"File {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file."

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["item_id", "rec_id", "score"], f"Incorrect CSV header. Got {header}"

        rows = list(reader)

    expected_rows = [
        (10, 50, 0.8573),
        (20, 50, 0.6974),
        (30, 10, 0.3708),
        (40, 30, 0.1873),
        (50, 10, 0.8573)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        try:
            actual_item_id = int(actual[0])
            actual_rec_id = int(actual[1])
            actual_score = float(actual[2])
        except ValueError as e:
            raise AssertionError(f"Row {i+1} has invalid data types: {actual}") from e

        assert actual_item_id == expected[0], f"Row {i+1} item_id mismatch. Expected {expected[0]}, got {actual_item_id}."
        assert actual_rec_id == expected[1], f"Row {i+1} rec_id mismatch. Expected {expected[1]}, got {actual_rec_id}."

        # Check if the score string is formatted to exactly 4 decimal places
        score_str = actual[2].strip()
        if "." in score_str:
            decimals = len(score_str.split(".")[1])
            assert decimals == 4, f"Row {i+1} score '{score_str}' is not formatted to exactly 4 decimal places."
        else:
            raise AssertionError(f"Row {i+1} score '{score_str}' missing decimal point.")

        assert abs(actual_score - expected[2]) <= 0.0001, f"Row {i+1} score mismatch. Expected {expected[2]}, got {actual_score}."