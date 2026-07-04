# test_final_state.py

import os
import subprocess
import pytest
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

def test_model_accuracy():
    """Verify that the saved model achieves at least 0.80 accuracy on a holdout set."""
    model_path = "/home/user/model.joblib"
    assert os.path.exists(model_path), f"The model file {model_path} does not exist."
    assert os.path.isfile(model_path), f"The path {model_path} is not a file."

    test_data_path = "/tmp/test_data.csv"
    generator_path = "/app/data_generator"

    # Generate test data
    try:
        with open(test_data_path, "w") as f:
            subprocess.run([generator_path, "5000"], stdout=f, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to generate test data using {generator_path}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error generating test data: {e}")

    assert os.path.exists(test_data_path), "Test data was not generated."

    # Load test data
    try:
        df = pd.read_csv(test_data_path)
    except Exception as e:
        pytest.fail(f"Failed to read generated test data: {e}")

    assert "target" in df.columns, "Generated data is missing the 'target' column."

    X_test = df.drop(columns=["target"])
    y_test = df["target"]

    # Load agent's model
    try:
        model = joblib.load(model_path)
    except Exception as e:
        pytest.fail(f"Failed to load model from {model_path}: {e}")

    # Predict and evaluate
    try:
        preds = model.predict(X_test)
    except Exception as e:
        pytest.fail(f"Model prediction failed: {e}")

    acc = accuracy_score(y_test, preds)

    assert acc >= 0.80, f"Model accuracy {acc:.4f} is below the required threshold of 0.80"

def test_train_script_exists():
    """Verify that the training script was created."""
    script_path = "/home/user/train.py"
    assert os.path.exists(script_path), f"The training script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_dataset_exists():
    """Verify that the dataset was generated."""
    dataset_path = "/home/user/dataset.csv"
    assert os.path.exists(dataset_path), f"The dataset {dataset_path} does not exist."
    assert os.path.isfile(dataset_path), f"The path {dataset_path} is not a file."