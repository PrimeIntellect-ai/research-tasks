# test_final_state.py

import os
import json
import pytest

def test_metadata_json_exists_and_valid():
    """Verify that run_metadata.json exists and contains the correct structure."""
    json_path = "/home/user/mlops_experiment/run_metadata.json"
    assert os.path.isfile(json_path), f"Metadata file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "test_accuracy" in data, "Key 'test_accuracy' missing from metadata JSON."
    assert isinstance(data["test_accuracy"], float), "Value for 'test_accuracy' must be a float."

    assert "model_path" in data, "Key 'model_path' missing from metadata JSON."
    assert data["model_path"] == "/home/user/mlops_experiment/model.pkl", "Value for 'model_path' is incorrect."

def test_model_pkl_exists():
    """Verify that the model.pkl file was generated."""
    model_path = "/home/user/mlops_experiment/model.pkl"
    assert os.path.isfile(model_path), f"Model file {model_path} is missing."
    assert os.path.getsize(model_path) > 0, f"Model file {model_path} is empty."

def test_train_script_fixed():
    """Verify that train.py is updated to use Pipeline and avoids data leakage."""
    script_path = "/home/user/mlops_experiment/train.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check that Pipeline is used
    assert "Pipeline" in content, "The script does not seem to use a scikit-learn Pipeline."

    # Check that the data leak is removed
    # The student shouldn't be fitting on the entire X dataset anymore.
    # Looking for signs of the old code.
    assert "imputer.fit_transform(X)" not in content, "Data leak still present: imputer.fit_transform(X) found."
    assert "scaler.fit_transform(X_imputed)" not in content, "Data leak still present: scaler.fit_transform(X_imputed) found."

    # Check that train_test_split is splitting X, not X_scaled
    assert "train_test_split(X," in content.replace(" ", "") or "train_test_split(X," in content, "train_test_split should split the original X, not scaled data."