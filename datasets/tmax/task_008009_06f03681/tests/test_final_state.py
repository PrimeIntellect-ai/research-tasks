# test_final_state.py
import os
import csv

def test_recommendation_stability_csv():
    csv_path = "/home/user/recommendation_stability.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    expected_rows = [
        ["neighbor_id", "count"],
        ["5", "50"],
        ["1", "21"],
        ["8", "19"],
        ["9", "10"]
    ]

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"CSV content does not match expected output. Got {actual_rows}, expected {expected_rows}"