# test_final_state.py

import os
import json
import pytest

INDEX_DIR = "/home/user/indexes"
OUTPUT_DIR = "/home/user/output"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results.json")

def test_directories_created():
    assert os.path.isdir(INDEX_DIR), f"Directory {INDEX_DIR} does not exist."
    assert os.path.isdir(OUTPUT_DIR), f"Directory {OUTPUT_DIR} does not exist."

def test_users_sorted_file():
    filepath = os.path.join(INDEX_DIR, "users_sorted.csv")
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    user_ids = []
    for line in lines:
        parts = line.split(',')
        assert len(parts) >= 2, f"Invalid line format in {filepath}: {line}"
        user_ids.append(int(parts[0]))

    assert user_ids == sorted(user_ids), f"{filepath} is not sorted numerically by user_id."
    assert len(user_ids) == 6, f"Expected 6 users in {filepath}, found {len(user_ids)}."

def test_follows_by_followee_file():
    filepath = os.path.join(INDEX_DIR, "follows_by_followee.csv")
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    followee_ids = []
    for line in lines:
        parts = line.split(',')
        assert len(parts) >= 2, f"Invalid line format in {filepath}: {line}"
        followee_ids.append(int(parts[1]))

    assert followee_ids == sorted(followee_ids), f"{filepath} is not sorted numerically by followee_id."
    assert len(followee_ids) == 5, f"Expected 5 follows in {filepath}, found {len(followee_ids)}."

def test_posts_by_user_file():
    filepath = os.path.join(INDEX_DIR, "posts_by_user.csv")
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    user_ids = []
    for line in lines:
        parts = line.split(',')
        assert len(parts) >= 3, f"Invalid line format in {filepath}: {line}"
        user_ids.append(int(parts[1]))

    assert user_ids == sorted(user_ids), f"{filepath} is not sorted numerically by user_id."
    assert len(user_ids) == 4, f"Expected 4 posts in {filepath}, found {len(user_ids)}."

def test_results_json():
    assert os.path.isfile(RESULTS_FILE), f"File {RESULTS_FILE} does not exist."

    with open(RESULTS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_FILE} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {RESULTS_FILE}, got {type(data)}."
    assert data == ["Alice", "Eve"], f"Expected [\"Alice\", \"Eve\"], got {data}."

def test_results_json_formatting():
    with open(RESULTS_FILE, 'r') as f:
        content = f.read()

    expected_format = '[\n  "Alice",\n  "Eve"\n]'
    assert content.strip() == expected_format, f"JSON formatting does not match expected 2-space indentation.\nExpected:\n{expected_format}\nGot:\n{content}"