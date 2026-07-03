# test_final_state.py

import os
import csv
import json
import pytest

def test_predictions_csv_exists_and_format():
    pred_path = '/home/user/predictions.csv'
    assert os.path.isfile(pred_path), f"Expected output file {pred_path} does not exist."

    with open(pred_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames is not None, f"File {pred_path} is empty."

        expected_cols = ['review_id', 'prob_books', 'prob_electronics']
        assert fieldnames == expected_cols, f"Expected columns {expected_cols}, got {fieldnames}."

        rows = list(reader)

    assert len(rows) == 4, f"Expected 4 rows in predictions.csv, got {len(rows)}."

    review_ids = []
    for row in rows:
        try:
            rid = int(row['review_id'])
            review_ids.append(rid)
        except ValueError:
            pytest.fail(f"review_id {row['review_id']} is not an integer.")

        try:
            p_books = float(row['prob_books'])
            p_elec = float(row['prob_electronics'])
        except ValueError:
            pytest.fail("Probabilities must be valid floats.")

        assert abs(p_books + p_elec - 1.0) < 1e-4, f"Probabilities {p_books} and {p_elec} do not sum to 1."

    expected_ids = [6, 7, 9, 10]
    assert review_ids == expected_ids, f"Expected review_ids {expected_ids} (sorted), got {review_ids}."

def test_benchmark_json():
    bench_path = '/home/user/benchmark.json'
    assert os.path.isfile(bench_path), f"Expected benchmark file {bench_path} does not exist."

    with open(bench_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {bench_path} is not valid JSON.")

    assert isinstance(data, dict), "Benchmark JSON must be an object/dict."
    assert "avg_inference_time_sec" in data, "Key 'avg_inference_time_sec' missing from benchmark.json."

    avg_time = data["avg_inference_time_sec"]
    assert isinstance(avg_time, float), f"Expected float for avg_inference_time_sec, got {type(avg_time)}."
    assert avg_time >= 0.0, "Average inference time should be non-negative."