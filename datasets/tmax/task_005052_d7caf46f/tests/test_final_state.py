# test_final_state.py

import os
import csv
import json
import pytest

def test_clean_data_csv():
    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_data_path), f"Missing {clean_data_path}"

    with open(clean_data_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 5, f"Expected 5 rows in clean_data.csv, got {len(rows)}"

    expected_rows = [
        {"id": "1", "income": 50000.0, "score": 80.0},
        {"id": "2", "income": 50000.0, "score": 90.0},
        {"id": "3", "income": 100000.0, "score": 0.0},
        {"id": "4", "income": 40000.0, "score": 75.0},
        {"id": "5", "income": 50000.0, "score": 85.0},
    ]

    for i, expected in enumerate(expected_rows):
        row = rows[i]
        assert float(row["id"]) == float(expected["id"]), f"Row {i+1} id mismatch"
        assert float(row["income"]) == expected["income"], f"Row {i+1} income mismatch"
        assert float(row["score"]) == expected["score"], f"Row {i+1} score mismatch"

def test_timing_json():
    timing_path = "/home/user/timing.json"
    assert os.path.isfile(timing_path), f"Missing {timing_path}"

    with open(timing_path, 'r') as f:
        try:
            timing_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("timing.json is not a valid JSON file")

    expected_keys = {"feat_a.py", "feat_b.py", "feat_c.py"}
    assert set(timing_data.keys()) == expected_keys, f"timing.json keys must be exactly {expected_keys}"

    for k, v in timing_data.items():
        assert isinstance(v, (int, float)), f"Value for {k} must be a number"

    assert timing_data["feat_b.py"] > 2.0, "feat_b.py execution time should be > 2.0s"
    assert timing_data["feat_a.py"] < 2.0, "feat_a.py execution time should be < 2.0s"
    assert timing_data["feat_c.py"] < 2.0, "feat_c.py execution time should be < 2.0s"

def test_final_training_data_csv():
    final_data_path = "/home/user/final_training_data.csv"
    assert os.path.isfile(final_data_path), f"Missing {final_data_path}"

    with open(final_data_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    assert fieldnames is not None, "final_training_data.csv must have a header"

    expected_fields = {"id", "income", "score", "feat_A", "feat_C"}
    assert set(fieldnames) == expected_fields, f"final_training_data.csv columns must be exactly {expected_fields}"

    assert len(rows) == 5, f"Expected 5 rows in final_training_data.csv, got {len(rows)}"

    expected_rows = [
        {"id": "1", "income": 50000.0, "score": 80.0, "feat_A": 100000.0, "feat_C": 50080.0},
        {"id": "2", "income": 50000.0, "score": 90.0, "feat_A": 100000.0, "feat_C": 50090.0},
        {"id": "3", "income": 100000.0, "score": 0.0, "feat_A": 200000.0, "feat_C": 100000.0},
        {"id": "4", "income": 40000.0, "score": 75.0, "feat_A": 80000.0, "feat_C": 40075.0},
        {"id": "5", "income": 50000.0, "score": 85.0, "feat_A": 100000.0, "feat_C": 50085.0},
    ]

    for i, expected in enumerate(expected_rows):
        row = rows[i]
        for field, expected_val in expected.items():
            assert float(row[field]) == expected_val, f"Row {i+1} field {field} mismatch: expected {expected_val}, got {row[field]}"