# test_final_state.py

import os
import csv
import json
import pytest

def test_duplicate_pairs_json():
    """Verify that duplicate_pairs.json exists and contains the expected pairs."""
    json_path = '/home/user/duplicate_pairs.json'
    assert os.path.isfile(json_path), f"Missing {json_path}"

    with open(json_path, 'r') as f:
        try:
            pairs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert isinstance(pairs, list), "JSON root must be a list."
    assert len(pairs) == 3, f"Expected 3 duplicate pairs, found {len(pairs)}."

    expected_pairs = [[1, 3], [4, 8], [2, 6]]

    # Check that each item is a list of 2 integers, sorted
    for p in pairs:
        assert isinstance(p, list) and len(p) == 2, "Each pair must be a list of 2 integers."
        assert p[0] < p[1], f"Pair {p} is not sorted (smaller ID must come first)."

    # We expect the exact set of pairs, though order might vary slightly due to float precision
    # but the prompt implies a specific top 3.
    sorted_expected = sorted(expected_pairs)
    sorted_actual = sorted(pairs)
    assert sorted_actual == sorted_expected, f"Expected pairs {sorted_expected}, got {sorted_actual}"

def test_cleaned_dataset_csv():
    """Verify that cleaned_dataset.csv exists, has correct structure, and dropped the right docs."""
    csv_path = '/home/user/cleaned_dataset.csv'
    assert os.path.isfile(csv_path), f"Missing {csv_path}"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."
    header = rows[0]
    expected_header = ['doc_id', 'title', 'text', 'pca_1', 'pca_2']
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 7, f"Expected exactly 7 remaining documents, found {len(data_rows)}."

    remaining_ids = []
    for row in data_rows:
        assert len(row) == 5, f"Row does not have 5 columns: {row}"
        doc_id_str, title, text, pca_1_str, pca_2_str = row

        try:
            doc_id = int(doc_id_str)
            remaining_ids.append(doc_id)
        except ValueError:
            pytest.fail(f"Invalid doc_id '{doc_id_str}' in row: {row}")

        try:
            float(pca_1_str)
            float(pca_2_str)
        except ValueError:
            pytest.fail(f"PCA values must be numeric, got pca_1='{pca_1_str}', pca_2='{pca_2_str}' in row: {row}")

    # The documents to drop were the larger IDs of the pairs: 3, 8, 6
    expected_remaining_ids = [1, 2, 4, 5, 7, 9, 10]
    assert sorted(remaining_ids) == expected_remaining_ids, f"Expected remaining doc_ids {expected_remaining_ids}, got {sorted(remaining_ids)}"