# test_final_state.py

import os
import csv
import math
import pytest

def test_discarded_log():
    log_path = '/home/user/discarded.log'
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_discarded = ['3', 'bad_id', '8']
    assert lines == expected_discarded, f"Expected discarded ids {expected_discarded}, but got {lines}."

def test_csv_splits():
    train_path = '/home/user/ml_prep/train.csv'
    val_path = '/home/user/ml_prep/val.csv'

    assert os.path.isfile(train_path), f"{train_path} is missing."
    assert os.path.isfile(val_path), f"{val_path} is missing."

    with open(train_path, 'r') as f:
        train_rows = list(csv.reader(f))

    with open(val_path, 'r') as f:
        val_rows = list(csv.reader(f))

    expected_header = ['id', 'feature_a', 'feature_b', 'category']
    assert train_rows[0] == expected_header, f"train.csv header incorrect: {train_rows[0]}"
    assert val_rows[0] == expected_header, f"val.csv header incorrect: {val_rows[0]}"

    assert len(train_rows) == 5, f"train.csv should have 5 lines (header + 4 rows), got {len(train_rows)}"
    assert len(val_rows) == 5, f"val.csv should have 5 lines (header + 4 rows), got {len(val_rows)}"

    # Verify the contents
    expected_data = {
        '1': ('-0.307238', '-0.365397', 'cat1'),
        '2': ('0.076810', '-0.783001', 'cat2'),
        '4': ('1.228952', '1.235389', 'cat3'),
        '5': ('-1.459381', '0.260998', 'cat1'),
        '6': ('-0.537667', '-0.504596', 'cat3'),
        '7': ('0.460857', '-1.479002', 'cat1'),
        '9': ('1.612999', '1.722585', 'cat1'),
        '10': ('-1.075334', '-0.086999', 'cat2')
    }

    all_data_rows = train_rows[1:] + val_rows[1:]

    seen_ids = set()
    for row in all_data_rows:
        assert len(row) == 4, f"Row {row} does not have exactly 4 columns."
        row_id, fa, fb, cat = row
        assert row_id in expected_data, f"Unexpected id {row_id} in output."
        seen_ids.add(row_id)

        exp_fa, exp_fb, exp_cat = expected_data[row_id]
        assert fa == exp_fa, f"For id {row_id}, expected feature_a {exp_fa}, got {fa}."
        assert fb == exp_fb, f"For id {row_id}, expected feature_b {exp_fb}, got {fb}."
        assert cat == exp_cat, f"For id {row_id}, expected category {exp_cat}, got {cat}."

    assert seen_ids == set(expected_data.keys()), "Not all expected valid rows were found in train.csv and val.csv."