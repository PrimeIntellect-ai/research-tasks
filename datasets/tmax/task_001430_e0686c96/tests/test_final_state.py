# test_final_state.py

import os
import json
import csv
import hashlib
import pytest

PROCESSED_DIR = "/home/user/processed"
CLEAN_DATA_CSV = os.path.join(PROCESSED_DIR, "clean_data.csv")
SUMMARY_JSON = os.path.join(PROCESSED_DIR, "summary.json")

def test_processed_files_exist():
    """Ensure the processed directory and output files are created."""
    assert os.path.isdir(PROCESSED_DIR), f"Directory {PROCESSED_DIR} does not exist."
    assert os.path.exists(CLEAN_DATA_CSV), f"File {CLEAN_DATA_CSV} does not exist."
    assert os.path.exists(SUMMARY_JSON), f"File {SUMMARY_JSON} does not exist."

def test_summary_json_contents():
    """Verify that the summary JSON contains the correct counts per question."""
    with open(SUMMARY_JSON, 'r', encoding='utf-8') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUMMARY_JSON} is not valid JSON.")

    expected_summary = {"q1": 2, "q2": 2, "q3": 3}
    assert summary == expected_summary, f"Expected summary {expected_summary}, but got {summary}."

def test_clean_data_csv_structure_and_contents():
    """Verify the structure, hashing, deduplication, and sorting of the clean data CSV."""
    with open(CLEAN_DATA_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # 1. Check columns
        expected_columns = ['user_id', 'timestamp', 'question', 'feedback_hash', 'feedback']
        assert reader.fieldnames == expected_columns, \
            f"Expected columns {expected_columns}, but got {reader.fieldnames}."

        rows = list(reader)

    # 2. Check total row count (derived from expected deduplication)
    assert len(rows) == 7, f"Expected exactly 7 rows after deduplication and dropping empty feedback, got {len(rows)}."

    seen_hashes = set()
    for row in rows:
        feedback = row['feedback']

        # 3. Check for empty/whitespace feedback
        assert feedback.strip() != "", f"Row with user_id {row['user_id']} has empty or whitespace-only feedback."

        # 4. Check that hash is computed correctly from stripped text
        expected_hash = hashlib.sha256(feedback.strip().encode('utf-8')).hexdigest()
        assert row['feedback_hash'] == expected_hash, \
            f"Hash mismatch for user_id {row['user_id']}. Expected {expected_hash}, got {row['feedback_hash']}."

        # 5. Check for exact duplicate hashes (deduplication check)
        assert expected_hash not in seen_hashes, \
            f"Duplicate feedback hash found: {expected_hash} for feedback '{feedback}'."
        seen_hashes.add(expected_hash)

    # 6. Check sorting (question asc, timestamp asc, user_id asc)
    def sort_key(r):
        return (r['question'], r['timestamp'], r['user_id'])

    sorted_rows = sorted(rows, key=sort_key)
    for i, (actual, expected) in enumerate(zip(rows, sorted_rows)):
        assert actual == expected, \
            f"Row at index {i} is out of order. Expected {expected}, got {actual}. " \
            "Data must be sorted by question, timestamp, then user_id."