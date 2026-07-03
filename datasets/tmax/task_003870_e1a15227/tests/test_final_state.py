# test_final_state.py

import os
import joblib
import pytest
from sklearn.datasets import make_classification

def test_solution_pipeline_exists():
    """Check if the solution pipeline file was created."""
    assert os.path.isfile('/home/user/solution_pipeline.joblib'), (
        "The file /home/user/solution_pipeline.joblib is missing. "
        "Did you save the fitted Pipeline?"
    )

def test_pipeline_architecture_and_accuracy():
    """Check the pipeline architecture and evaluate its accuracy on a holdout set."""
    try:
        pipeline = joblib.load('/home/user/solution_pipeline.joblib')
    except Exception as e:
        pytest.fail(f"Failed to load the pipeline from /home/user/solution_pipeline.joblib: {e}")

    # Check that it is a Pipeline
    assert hasattr(pipeline, "steps"), "The saved object is not a scikit-learn Pipeline."
    assert len(pipeline.steps) >= 2, "The pipeline should have at least a scaler and a classifier."

    # Extract the MLP classifier (assuming it's the last step)
    mlp = pipeline.steps[-1][1]
    assert type(mlp).__name__ == "MLPClassifier", "The last step of the pipeline is not an MLPClassifier."

    # Check architecture parameters
    assert mlp.hidden_layer_sizes == (128, 64), f"Expected hidden_layer_sizes=(128, 64), got {mlp.hidden_layer_sizes}"
    assert mlp.activation == 'relu', f"Expected activation='relu', got {mlp.activation}"
    assert mlp.alpha == 0.05, f"Expected alpha=0.05, got {mlp.alpha}"

    # Generate holdout dataset
    X_hold, y_hold = make_classification(n_samples=1000, n_features=20, n_informative=15, random_state=99)

    # Evaluate accuracy
    accuracy = pipeline.score(X_hold, y_hold)

    # Assert metric threshold
    threshold = 0.80
    assert accuracy >= threshold, (
        f"Pipeline accuracy on holdout set is {accuracy:.4f}, "
        f"which is below the required threshold of {threshold:.4f}. "
        "Ensure data was joined properly and scaling was applied without data leakage."
    )