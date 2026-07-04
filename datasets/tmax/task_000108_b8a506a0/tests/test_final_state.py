# test_final_state.py

import os
import json
import math
import pytest

def test_results_json_exists_and_correct():
    results_path = "/home/user/results.json"

    assert os.path.exists(results_path), f"File {results_path} does not exist. The script must create this file."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not a valid JSON file.")

    assert "accuracy" in results, "Key 'accuracy' is missing from results.json."
    assert "roc_auc" in results, "Key 'roc_auc' is missing from results.json."

    acc = results["accuracy"]
    roc = results["roc_auc"]

    assert isinstance(acc, (int, float)), "'accuracy' must be a float."
    assert isinstance(roc, (int, float)), "'roc_auc' must be a float."

    expected_acc = 0.805
    expected_roc = 0.90225135

    assert math.isclose(acc, expected_acc, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected accuracy to be close to {expected_acc}, but got {acc}. Did you fix the data leakage correctly?"

    assert math.isclose(roc, expected_roc, rel_tol=1e-3, abs_tol=1e-4), \
        f"Expected roc_auc to be close to {expected_roc}, but got {roc}. Did you fix the data leakage correctly?"

def test_pipeline_script_fixed():
    pipeline_path = "/home/user/model_pipeline.py"

    assert os.path.exists(pipeline_path), f"File {pipeline_path} is missing."

    with open(pipeline_path, 'r') as f:
        content = f.read()

    # Check that fit_transform is not called on test sets
    assert "scaler.fit_transform(X_test)" not in content, \
        "Data leakage bug still exists: scaler.fit_transform() is called on X_test."
    assert "pca.fit_transform(X_test_scaled)" not in content, \
        "Data leakage bug still exists: pca.fit_transform() is called on X_test_scaled."

    # Check that transform is called instead
    assert "scaler.transform(X_test)" in content, \
        "Expected scaler.transform(X_test) to be used for the test set."
    assert "pca.transform(X_test_scaled)" in content, \
        "Expected pca.transform(X_test_scaled) to be used for the test set."