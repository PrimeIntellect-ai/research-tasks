# test_final_state.py

import os
import csv
import math
import pytest

def test_processed_files_exist():
    """Check that the processed train and test CSVs were created."""
    train_path = "/home/user/data/processed/train.csv"
    test_path = "/home/user/data/processed/test.csv"

    assert os.path.isfile(train_path), f"Processed train file missing: {train_path}"
    assert os.path.isfile(test_path), f"Processed test file missing: {test_path}"

    with open(train_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert set(header) == {"user_id", "age", "income", "activity_score"}, f"Incorrect columns in train.csv: {header}"
        rows = list(reader)
        assert len(rows) == 75, f"Expected 75 rows in train.csv, found {len(rows)}"

    with open(test_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert set(header) == {"user_id", "age", "income", "activity_score"}, f"Incorrect columns in test.csv: {header}"
        rows = list(reader)
        assert len(rows) == 25, f"Expected 25 rows in test.csv, found {len(rows)}"

def test_similarity_output():
    """Check that the similarity output file exists and contains the correct user_id."""
    output_path = "/home/user/data/processed/most_similar_user.txt"
    assert os.path.isfile(output_path), f"Similarity output missing: {output_path}"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Expected integer in {output_path}, got {content}"

    # The expected user_id based on the correct logic is 29
    assert content == "29", f"Expected most similar user_id to be 29, but got {content}. Ensure data leakage is fixed and outlier handling is applied correctly."