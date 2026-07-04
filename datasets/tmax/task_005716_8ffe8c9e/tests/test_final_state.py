# test_final_state.py

import os
import json
import math

def test_fixed_pipeline_exists():
    file_path = "/home/user/fixed_pipeline.py"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    assert os.path.isfile(file_path), f"Not a file: {file_path}"
    with open(file_path, "r") as f:
        content = f.read()
        assert "experiment_v2.json" in content, "fixed_pipeline.py should reference experiment_v2.json"

def test_experiment_v1_output():
    file_path = "/home/user/experiment_v1.json"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Invalid JSON in {file_path}"
    assert "avg_top1_similarity" in data, f"Missing 'avg_top1_similarity' in {file_path}"
    v1 = data["avg_top1_similarity"]
    assert math.isclose(v1, 0.4485590396440231, rel_tol=1e-5), f"Expected avg_top1_similarity in v1 to be ~0.448559, got {v1}"

def test_experiment_v2_output():
    file_path = "/home/user/experiment_v2.json"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Invalid JSON in {file_path}"
    assert "avg_top1_similarity" in data, f"Missing 'avg_top1_similarity' in {file_path}"
    v2 = data["avg_top1_similarity"]
    assert math.isclose(v2, 0.4194511565268481, rel_tol=1e-5), f"Expected avg_top1_similarity in v2 to be ~0.419451, got {v2}"

def test_leakage_diff_output():
    file_path = "/home/user/leakage_diff.txt"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    with open(file_path, "r") as f:
        content = f.read().strip()

    try:
        diff = float(content)
    except ValueError:
        assert False, f"Could not parse float from {file_path}. Content: '{content}'"

    # Read v1 and v2 to compare
    with open("/home/user/experiment_v1.json", "r") as f:
        v1 = json.load(f)["avg_top1_similarity"]
    with open("/home/user/experiment_v2.json", "r") as f:
        v2 = json.load(f)["avg_top1_similarity"]

    expected_diff = abs(v1 - v2)
    assert math.isclose(diff, expected_diff, rel_tol=1e-5), f"Expected difference to be ~{expected_diff}, got {diff}"