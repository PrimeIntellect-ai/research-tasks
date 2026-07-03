# test_final_state.py

import os
import json
import pickle
import pytest

METRICS_PATH = '/home/user/metrics.jsonl'
MODEL_PATH = '/home/user/best_model.pkl'

def test_metrics_file_exists():
    assert os.path.exists(METRICS_PATH), f"Metrics file not found at {METRICS_PATH}"
    assert os.path.isfile(METRICS_PATH), f"{METRICS_PATH} is not a file"

def test_metrics_content():
    assert os.path.exists(METRICS_PATH), "Metrics file missing"

    with open(METRICS_PATH, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"Expected exactly 2 lines in metrics.jsonl, found {len(lines)}"

    models_logged = []
    accuracies = {}

    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON line in metrics.jsonl: {line}")

        assert "model_name" in data, "Missing 'model_name' in JSON"
        assert "mean_cv_accuracy" in data, "Missing 'mean_cv_accuracy' in JSON"
        assert "hyperparameters" in data, "Missing 'hyperparameters' in JSON"

        models_logged.append(data['model_name'])
        accuracies[data['model_name']] = data['mean_cv_accuracy']

    assert set(models_logged) == {"LogisticRegression", "RandomForestClassifier"}, \
        f"Expected models LogisticRegression and RandomForestClassifier, got {models_logged}"

    lr_acc = accuracies.get("LogisticRegression")
    rf_acc = accuracies.get("RandomForestClassifier")

    assert isinstance(lr_acc, float), "LogisticRegression accuracy must be a float"
    assert isinstance(rf_acc, float), "RandomForestClassifier accuracy must be a float"

    assert 0.80 < lr_acc < 0.90, f"LogisticRegression accuracy out of expected bounds (0.80-0.90): {lr_acc}"
    assert 0.85 < rf_acc < 0.95, f"RandomForestClassifier accuracy out of expected bounds (0.85-0.95): {rf_acc}"

def test_best_model_exists():
    assert os.path.exists(MODEL_PATH), f"Best model file not found at {MODEL_PATH}"
    assert os.path.isfile(MODEL_PATH), f"{MODEL_PATH} is not a file"

def test_best_model_is_rf():
    assert os.path.exists(MODEL_PATH), "Best model file missing"

    try:
        with open(MODEL_PATH, 'rb') as f:
            best_model = pickle.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load best_model.pkl: {e}")

    model_type = type(best_model).__name__

    # It might be a Pipeline containing RandomForestClassifier, or the classifier itself.
    # The truth script expects the type to be exactly 'RandomForestClassifier' or at least we check for it.
    # If it's a pipeline, we check its steps. But truth script says type(best_model).__name__ == 'RandomForestClassifier'.
    # We will be slightly flexible to allow pipelines if the final step is a RandomForestClassifier.
    if model_type == 'Pipeline':
        final_step = best_model.steps[-1][1]
        model_type = type(final_step).__name__

    assert model_type == 'RandomForestClassifier', \
        f"Expected best model to be RandomForestClassifier (or a pipeline ending in it), got {model_type}"