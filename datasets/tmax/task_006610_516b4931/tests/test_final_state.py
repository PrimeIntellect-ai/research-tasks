# test_final_state.py

import os
import csv
import hashlib
import pytest

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_makefile_exists():
    assert os.path.exists('/home/user/Makefile'), "/home/user/Makefile does not exist."
    assert os.path.isfile('/home/user/Makefile'), "/home/user/Makefile is not a file."

def test_cleaned_csv():
    file_path = '/home/user/cleaned.csv'
    assert os.path.exists(file_path), f"{file_path} does not exist."

    data = read_csv(file_path)
    assert len(data) == 8, f"Expected 8 rows in cleaned.csv, got {len(data)}."

    ids = {row['id'] for row in data}
    assert '2' not in ids, "Row with id 2 (embedded newline) was not dropped."
    assert '9' not in ids, "Row with id 9 (embedded newline) was not dropped."
    expected_ids = {'1', '3', '4', '5', '6', '7', '8', '10'}
    assert ids == expected_ids, f"Expected IDs {expected_ids}, got {ids}."

def test_reshaped_csv():
    file_path = '/home/user/reshaped.csv'
    assert os.path.exists(file_path), f"{file_path} does not exist."

    data = read_csv(file_path)
    assert len(data) == 24, f"Expected 24 rows in reshaped.csv, got {len(data)}."

    columns = data[0].keys()
    assert 'question' in columns, "Column 'question' not found in reshaped.csv."
    assert 'score' in columns, "Column 'score' not found in reshaped.csv."

    scores = [row['score'] for row in data]
    assert '3.7' in scores, "Imputed score 3.7 not found in reshaped.csv."

def test_anonymized_csv():
    file_path = '/home/user/anonymized.csv'
    assert os.path.exists(file_path), f"{file_path} does not exist."

    data = read_csv(file_path)
    assert len(data) == 24, f"Expected 24 rows in anonymized.csv, got {len(data)}."

    for row in data:
        assert row['name'] == 'REDACTED', f"Name not REDACTED for id {row.get('id')}."

    alice_hash = hashlib.sha256(b"alice@test.com").hexdigest()
    emails = {row['email'] for row in data}
    assert alice_hash in emails, "Lowercase hashed email for Alice not found."

def test_final_sample_csv():
    file_path = '/home/user/final_sample.csv'
    assert os.path.exists(file_path), f"{file_path} does not exist."

    data = read_csv(file_path)
    assert len(data) == 12, f"Expected 12 rows in final_sample.csv, got {len(data)}."

    hr_count = sum(1 for row in data if row['department'] == 'HR')
    eng_count = sum(1 for row in data if row['department'] == 'ENG')

    assert hr_count == 6, f"Expected 6 HR rows, got {hr_count}."
    assert eng_count == 6, f"Expected 6 ENG rows, got {eng_count}."

    for row in data:
        assert row['name'] == 'REDACTED', "Not all names are REDACTED in final_sample.csv."

    scores = [row['score'] for row in data]
    assert '3.7' in scores, "Imputed score 3.7 not found in final_sample.csv."