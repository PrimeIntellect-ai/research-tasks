# test_final_state.py
import json
import os
import pytest

def test_final_dataset_metric():
    filepath = "/home/user/final_dataset.jsonl"
    assert os.path.isfile(filepath), f"Output file not found at {filepath}"

    with open(filepath, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 1000, f"Expected exactly 1000 lines in {filepath}, but got {len(lines)}"

    scores = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        assert 'score' in data, f"Line {i+1} missing 'score' key: {data}"
        assert isinstance(data['score'], (int, float)), f"Line {i+1} 'score' is not a number: {data['score']}"
        scores.append(data['score'])

    assert len(scores) == 1000, f"Expected exactly 1000 valid JSON objects, got {len(scores)}"

    mean_score = sum(scores) / len(scores)
    assert mean_score >= 0.80, f"Mean score is {mean_score:.4f}, which is below the required threshold of 0.80"