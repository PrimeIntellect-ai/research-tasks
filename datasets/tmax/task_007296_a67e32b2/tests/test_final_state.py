# test_final_state.py
import os
import csv
import hashlib
import pytest

def test_recommendations_file():
    rec_path = '/home/user/etl_pipeline/recommendations.txt'
    assert os.path.isfile(rec_path), f"Missing {rec_path}"

    with open(rec_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {rec_path} is empty."

    parts = content.split(',')
    assert len(parts) == 3, f"Expected 3 comma-separated IDs in {rec_path}, found {len(parts)}."

    for p in parts:
        assert p.strip().isdigit(), f"Expected integer IDs in {rec_path}, found '{p}'."

def test_embeddings_csv_format_and_sort():
    emb_path = '/home/user/etl_pipeline/embeddings.csv'
    assert os.path.isfile(emb_path), f"Missing {emb_path}"

    with open(emb_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['id', 'e0', 'e1', 'e2'], f"Incorrect header in {emb_path}: {header}"

        rows = list(reader)
        assert len(rows) == 100, f"Expected 100 rows in {emb_path}, found {len(rows)}."

        prev_id = -1
        for i, row in enumerate(rows):
            assert len(row) == 4, f"Row {i+1} does not have 4 columns."

            curr_id = int(row[0])
            assert curr_id > prev_id, f"IDs are not sorted ascending at row {i+1}."
            prev_id = curr_id

            for j in range(1, 4):
                val_str = row[j]
                assert '.' in val_str, f"Value {val_str} not rounded to 4 decimal places."
                decimals = val_str.split('.')[1]
                assert len(decimals) <= 4, f"Value {val_str} has more than 4 decimal places."

def test_reproducibility_file_and_md5():
    emb_path = '/home/user/etl_pipeline/embeddings.csv'
    rep_path = '/home/user/etl_pipeline/reproducibility.txt'

    assert os.path.isfile(emb_path), f"Missing {emb_path}"
    assert os.path.isfile(rep_path), f"Missing {rep_path}"

    with open(emb_path, 'rb') as f:
        actual_md5 = hashlib.md5(f.read()).hexdigest()

    with open(rep_path, 'r') as f:
        saved_md5 = f.read().strip()

    assert saved_md5 == actual_md5, f"MD5 hash in {rep_path} ({saved_md5}) does not match actual MD5 of {emb_path} ({actual_md5})."
    assert len(saved_md5) == 32, f"MD5 hash string should be 32 characters, got {len(saved_md5)}."