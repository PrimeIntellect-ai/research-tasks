# test_final_state.py

import os
import csv
import pytest

CLEANED_DATASET_PATH = "/home/user/cleaned_dataset.csv"
REMOVED_DUPLICATES_PATH = "/home/user/removed_duplicates.txt"

def test_cleaned_dataset_exists():
    assert os.path.exists(CLEANED_DATASET_PATH), f"The file {CLEANED_DATASET_PATH} is missing."
    assert os.path.isfile(CLEANED_DATASET_PATH), f"The path {CLEANED_DATASET_PATH} is not a file."

def test_removed_duplicates_exists():
    assert os.path.exists(REMOVED_DUPLICATES_PATH), f"The file {REMOVED_DUPLICATES_PATH} is missing."
    assert os.path.isfile(REMOVED_DUPLICATES_PATH), f"The path {REMOVED_DUPLICATES_PATH} is not a file."

def test_cleaned_dataset_content():
    with open(CLEANED_DATASET_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames == ["id", "description", "confidence"], "Cleaned dataset header is incorrect."

        rows = list(reader)

    ids = [int(row["id"]) for row in rows]

    # Phase 2 dropped IDs should definitely not be here
    assert 3 not in ids, "ID 3 should have been dropped in Phase 2 (length <= 15)."
    assert 4 not in ids, "ID 4 should have been dropped in Phase 2 (confidence < 0.80)."

    # Phase 4 dropped IDs (identical or obvious duplicates)
    assert 2 not in ids, "ID 2 should have been dropped in Phase 4 (identical to ID 1 with lower confidence)."
    assert 10 not in ids, "ID 10 should have been dropped in Phase 4 (duplicate of 9, equal confidence, higher ID)."

def test_removed_duplicates_content():
    with open(REMOVED_DUPLICATES_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    try:
        removed_ids = [int(line) for line in lines]
    except ValueError:
        pytest.fail("removed_duplicates.txt should contain only integer IDs.")

    assert removed_ids == sorted(removed_ids), "The IDs in removed_duplicates.txt must be sorted in ascending order."

    # Phase 2 drops should NOT be in this file
    assert 3 not in removed_ids, "ID 3 was dropped in Phase 2 and should NOT be in removed_duplicates.txt."
    assert 4 not in removed_ids, "ID 4 was dropped in Phase 2 and should NOT be in removed_duplicates.txt."

    # Obvious Phase 4 drops MUST be in this file
    assert 2 in removed_ids, "ID 2 was a duplicate dropped in Phase 4 and should be in removed_duplicates.txt."
    assert 10 in removed_ids, "ID 10 was a duplicate dropped in Phase 4 and should be in removed_duplicates.txt."