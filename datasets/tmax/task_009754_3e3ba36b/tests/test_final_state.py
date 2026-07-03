# test_final_state.py

import os
import json
import pytest

def test_embeddings_jsonl():
    filepath = "/home/user/output/embeddings.jsonl"
    assert os.path.exists(filepath), f"File {filepath} does not exist. The Go program must create it."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in {filepath}, but found {len(lines)}."

    expected_vectors = {
        "1": [0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
        "2": [2, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        "3": [1, 0, 0, 0, 0, 1, 1, 1, 0, 2]
    }

    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {filepath} is not valid JSON.")

        assert "id" in obj, f"Missing 'id' key in line {i+1} of {filepath}."
        assert "vector" in obj, f"Missing 'vector' key in line {i+1} of {filepath}."

        row_id = obj["id"]
        assert row_id in expected_vectors, f"Unexpected id '{row_id}' found in {filepath}."

        expected_vector = expected_vectors[row_id]
        assert obj["vector"] == expected_vector, f"Incorrect vector for id '{row_id}'. Expected {expected_vector}, got {obj['vector']}."

def test_run_metrics_txt():
    filepath = "/home/user/output/run_metrics.txt"
    assert os.path.exists(filepath), f"File {filepath} does not exist. The Go program must create it."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_content = "Run completed. Total records processed: 3"

    # Check if the expected string is present in the file (to handle if they appended multiple times or added newlines)
    assert expected_content in content, f"Expected '{expected_content}' to be in {filepath}, but found:\n{content}"