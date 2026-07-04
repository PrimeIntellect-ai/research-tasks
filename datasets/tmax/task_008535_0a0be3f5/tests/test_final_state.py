# test_final_state.py
import os
import csv
import pytest

def test_best_score_exists_and_valid():
    score_path = "/home/user/best_score.txt"
    assert os.path.isfile(score_path), f"Score artifact missing at {score_path}."

    with open(score_path, 'r') as f:
        content = f.read().strip()

    try:
        score = float(content)
    except ValueError:
        pytest.fail(f"Content of {score_path} is not a valid float: {content}")

def test_data_clean_csv():
    clean_path = "/home/user/data_clean.csv"
    assert os.path.isfile(clean_path), f"Clean data artifact missing at {clean_path}."

    with open(clean_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, "data_clean.csv is empty."
    assert 'group_id' in rows[0], "group_id column missing from data_clean.csv."

    group_ids = [row['group_id'] for row in rows]

    # Check that -1 is in the group_ids
    assert '-1' in group_ids, "Missing values were not filled with -1 in group_id column."

    # Check that all group_ids are formatted as integers (no decimals)
    for gid in group_ids:
        try:
            val = int(gid)
            # Ensure it's strictly formatted as an integer, not a float string like "1.0"
            assert str(val) == gid, f"group_id value '{gid}' is not strictly formatted as an integer."
        except ValueError:
            pytest.fail(f"group_id value '{gid}' is not a valid integer.")