# test_final_state.py
import os
import json
import pytest

def test_features_jsonl_exists_and_valid():
    file_path = "/home/user/output/features.jsonl"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 10, "features.jsonl should have exactly 10 lines"

    parsed_ids = set()
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {file_path} is not valid JSON")

        # Check required keys
        required_keys = {'id', 'svd_0', 'svd_1', 'svd_2', 'category_id'}
        missing_keys = required_keys - set(obj.keys())
        assert not missing_keys, f"Line {i+1} is missing keys: {missing_keys}"

        parsed_ids.add(obj['id'])

        # Check category_id type and value
        cat_id = obj['category_id']
        assert isinstance(cat_id, int), f"category_id must be an integer, got {type(cat_id)} on line {i+1}"
        assert not isinstance(cat_id, bool), f"category_id must be an integer, got bool on line {i+1}"

        # Check if missing values were filled with -1
        if obj['id'] in (5, 10):
            assert cat_id == -1, f"category_id for id {obj['id']} should be -1, got {cat_id}"

        # Check svd feature types
        assert isinstance(obj['svd_0'], (int, float)), f"svd_0 must be a number on line {i+1}"
        assert isinstance(obj['svd_1'], (int, float)), f"svd_1 must be a number on line {i+1}"
        assert isinstance(obj['svd_2'], (int, float)), f"svd_2 must be a number on line {i+1}"

    assert parsed_ids == set(range(1, 11)), "features.jsonl must contain all ids from 1 to 10"

def test_accuracy_txt_exists_and_valid():
    file_path = "/home/user/output/accuracy.txt"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    try:
        accuracy = float(content)
    except ValueError:
        pytest.fail(f"accuracy.txt must contain a valid float, got: {content}")

    assert 0.0 <= accuracy <= 1.0, f"accuracy must be between 0.0 and 1.0, got: {accuracy}"