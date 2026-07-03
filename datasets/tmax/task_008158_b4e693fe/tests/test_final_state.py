# test_final_state.py

import os
import csv
import pytest

def test_author_metrics_csv_exists_and_content():
    csv_path = "/home/user/author_metrics.csv"
    assert os.path.exists(csv_path), f"The file {csv_path} was not created."

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The CSV file is empty."

    expected_header = ["Author", "Avg_Accuracy", "Avg_F1"]
    assert rows[0] == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {rows[0]}"

    # The expected data derived from the cross-query aggregation of publications.ttl and experiments.jsonl
    # Pub1 (ML): Alice Smith, Bob Jones. Acc: 0.955, F1: 0.925
    # Pub2 (ML): Alice Smith, Charlie Brown. Acc: 0.885, F1: 0.855
    # Pub3 (Databases): Ignored
    # Pub4 (ML): Charlie Brown. Acc: 0.910, F1: 0.900
    #
    # Author Aggregation:
    # Alice Smith: (0.955 + 0.885)/2 = 0.9200, (0.925 + 0.855)/2 = 0.8900
    # Bob Jones: 0.9550, 0.9250
    # Charlie Brown: (0.885 + 0.910)/2 = 0.8975, (0.855 + 0.900)/2 = 0.8775

    expected_data = [
        ["Alice Smith", "0.9200", "0.8900"],
        ["Bob Jones", "0.9550", "0.9250"],
        ["Charlie Brown", "0.8975", "0.8775"]
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(data_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_data, data_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."