# test_final_state.py

import os
import pytest

def test_results_csv_exists():
    assert os.path.isfile('/home/user/results.csv'), "The file /home/user/results.csv does not exist."

def test_query_app_cpp_exists():
    assert os.path.isfile('/home/user/query_app.cpp'), "The file /home/user/query_app.cpp does not exist."

def test_results_csv_header():
    with open('/home/user/results.csv', 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "/home/user/results.csv is empty."
    header = lines[0].strip()
    assert header == "id,value", f"Expected header 'id,value', but got '{header}'."

def test_metric_jaccard_similarity():
    golden_file = '/app/golden_ids.txt'
    assert os.path.isfile(golden_file), f"{golden_file} is missing."

    with open(golden_file, 'r') as f:
        expected = set(f.read().strip().split(','))

    actual = set()
    with open('/home/user/results.csv', 'r') as f:
        lines = f.readlines()
        if len(lines) > 1:
            for line in lines[1:]: # skip header
                parts = line.strip().split(',')
                if len(parts) > 0 and parts[0]:
                    actual.add(parts[0])

    assert len(expected) > 0, "Expected IDs set is empty."
    assert len(actual) > 0, "Actual IDs set is empty (no results retrieved)."

    intersection = expected.intersection(actual)
    union = expected.union(actual)
    jaccard = len(intersection) / len(union)

    threshold = 1.0
    assert jaccard >= threshold, (
        f"Jaccard Similarity metric failed. "
        f"Expected >= {threshold}, but got {jaccard:.4f}. "
        f"Expected IDs: {expected}, Actual IDs: {actual}"
    )