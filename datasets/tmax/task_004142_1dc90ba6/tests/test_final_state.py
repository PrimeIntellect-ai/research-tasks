# test_final_state.py

import os
import csv
import pytest

def test_bad_output_exists():
    path = '/home/user/bad_output.csv'
    assert os.path.isfile(path), f"Missing file: {path}. You were supposed to run buggy_join.py."

def test_fixed_join_py_exists():
    path = '/home/user/fixed_join.py'
    assert os.path.isfile(path), f"Missing file: {path}. You need to write the corrected script."

def test_fixed_output_correct():
    path = '/home/user/fixed_output.csv'
    assert os.path.isfile(path), f"Missing file: {path}. Your script must generate this file."

    expected_tokens = {
        'doc_1': '9007199254740995',
        'doc_3': '9007199254740997',
        'doc_4': '1048576',
        'doc_5': '9007199254740993'
    }

    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 5, f"Expected 5 rows in {path}, found {len(rows)}"

    # Check that all expected doc_ids are present
    doc_ids = [row.get('doc_id') for row in rows]
    expected_docs = ['doc_1', 'doc_2', 'doc_3', 'doc_4', 'doc_5']
    for d in expected_docs:
        assert d in doc_ids, f"Missing {d} in {path}"

    for row in rows:
        doc_id = row.get('doc_id')
        token_id = row.get('token_id', '').strip()

        if doc_id in expected_tokens:
            expected_val = expected_tokens[doc_id]
            # It must be exactly the string representation of the large integer, no decimals
            assert token_id == expected_val, f"For {doc_id}, expected token_id '{expected_val}', got '{token_id}'"
        elif doc_id == 'doc_2':
            # Missing value should be empty or a pandas NA representation
            assert token_id in ('', '<NA>', 'NaN'), f"For doc_2, expected missing value representation, got '{token_id}'"

def test_precision_loss_docs_correct():
    path = '/home/user/precision_loss_docs.txt'
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        lines = f.readlines()

    corrupted_docs = {line.strip() for line in lines if line.strip()}
    expected_corrupted = {'doc_1', 'doc_3', 'doc_5'}

    assert corrupted_docs == expected_corrupted, f"Expected corrupted docs {expected_corrupted}, but got {corrupted_docs}"