# test_final_state.py

import os
import json
import math
import pytest

METRICS_PATH = "/home/user/data_project/metrics.json"
MODEL_PATH = "/home/user/data_project/model.pkl"

def test_metrics_file_exists_and_valid():
    assert os.path.isfile(METRICS_PATH), f"Metrics file not found at {METRICS_PATH}"

    with open(METRICS_PATH, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {METRICS_PATH} is not valid JSON.")

    assert isinstance(metrics, dict), "Metrics JSON should be an object/dictionary."
    assert "test_accuracy" in metrics, "Key 'test_accuracy' missing in metrics.json"
    assert "pca_explained_variance_1" in metrics, "Key 'pca_explained_variance_1' missing in metrics.json"

def test_metrics_values():
    with open(METRICS_PATH, 'r') as f:
        metrics = json.load(f)

    acc = metrics.get("test_accuracy")
    pca_var = metrics.get("pca_explained_variance_1")

    assert isinstance(acc, (int, float)), "test_accuracy must be a number"
    assert isinstance(pca_var, (int, float)), "pca_explained_variance_1 must be a number"

    # Expected accuracy is exactly 0.875 for this setup, but we allow a small margin
    assert math.isclose(acc, 0.875, rel_tol=1e-2), f"test_accuracy {acc} is not close to expected 0.875"

    # Expected PCA variance is ~0.063189
    assert math.isclose(pca_var, 0.063189, rel_tol=1e-2), f"pca_explained_variance_1 {pca_var} is not close to expected 0.063189"

def test_model_file_exists_and_contains_pipeline():
    assert os.path.isfile(MODEL_PATH), f"Model file not found at {MODEL_PATH}"
    assert os.path.getsize(MODEL_PATH) > 0, f"Model file {MODEL_PATH} is empty"

    # We check the binary content for class names to avoid importing third-party libraries
    with open(MODEL_PATH, 'rb') as f:
        content = f.read()

    assert b"Pipeline" in content, "Model file does not appear to contain a scikit-learn Pipeline"
    assert b"StandardScaler" in content, "Model file does not appear to contain a StandardScaler"
    assert b"PCA" in content, "Model file does not appear to contain a PCA step"
    assert b"LogisticRegression" in content, "Model file does not appear to contain a LogisticRegression step"

def test_train_model_script_refactored():
    script_path = "/home/user/data_project/train_model.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # Verify that the pipeline is imported
    assert "Pipeline" in content or "make_pipeline" in content, "Script does not seem to use Pipeline"

    # Verify the leak is removed
    assert "scaler.fit_transform(X)" not in content, "Data leak is still present: scaler is fitted on the entire dataset X"
    assert "pca.fit_transform(X_scaled)" not in content, "Data leak is still present: pca is fitted on the entire dataset"