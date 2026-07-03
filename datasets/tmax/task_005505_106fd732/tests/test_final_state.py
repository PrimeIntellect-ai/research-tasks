# test_final_state.py

import os
import json
import math
import pytest

def test_experiment_json_exists():
    json_path = "/home/user/output/experiment.json"
    assert os.path.isfile(json_path), f"Expected output file {json_path} does not exist."

def test_experiment_json_content():
    json_path = "/home/user/output/experiment.json"
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "best_match_file" in data, "Missing 'best_match_file' in JSON output."
    assert "query_vector" in data, "Missing 'query_vector' in JSON output."
    assert "doc_vectors" in data, "Missing 'doc_vectors' in JSON output."

    assert data["best_match_file"] == "doc1.txt", f"Expected best_match_file to be 'doc1.txt', got {data['best_match_file']}."

    expected_query = [1.0, 2.0]
    assert len(data["query_vector"]) == 2, "query_vector should have 2 elements."
    for actual, expected in zip(data["query_vector"], expected_query):
        assert math.isclose(actual, expected, rel_tol=1e-5, abs_tol=1e-5), \
            f"Query vector mismatch: expected {expected_query}, got {data['query_vector']}"

    expected_docs = {
        "doc1.txt": [2.5, 2.5],
        "doc2.txt": [-1.5, -1.5],
        "doc3.txt": [0.0, 1.0]
    }

    doc_vectors = data["doc_vectors"]
    for doc, expected_vec in expected_docs.items():
        assert doc in doc_vectors, f"Missing {doc} in doc_vectors."
        actual_vec = doc_vectors[doc]
        assert len(actual_vec) == 2, f"Vector for {doc} should have 2 elements."
        for actual, expected in zip(actual_vec, expected_vec):
            assert math.isclose(actual, expected, rel_tol=1e-5, abs_tol=1e-5), \
                f"Vector mismatch for {doc}: expected {expected_vec}, got {actual_vec}"