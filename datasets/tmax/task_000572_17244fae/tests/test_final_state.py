# test_final_state.py

import os
import joblib
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline

def test_best_model_exists():
    assert os.path.exists('/app/best_model.pkl'), "The best model file '/app/best_model.pkl' is missing."

def test_model_performance_and_structure():
    model_path = '/app/best_model.pkl'
    assert os.path.exists(model_path), "Model file missing."

    try:
        model = joblib.load(model_path)
    except Exception as e:
        pytest.fail(f"Failed to load the model from '/app/best_model.pkl'. Error: {e}")

    # Check if it's a Pipeline to ensure data preprocessing is encapsulated
    assert isinstance(model, Pipeline), "The saved model is not a scikit-learn Pipeline. You must use a Pipeline to prevent data leakage."

    hidden_data_path = '/app/data/hidden_test.parquet'
    assert os.path.exists(hidden_data_path), "Hidden test data is missing."

    hidden_df = pd.read_parquet(hidden_data_path)
    X_hidden = hidden_df.drop('target', axis=1)
    y_hidden = hidden_df['target']

    # Generate predictions
    try:
        if hasattr(model, "decision_function"):
            preds = model.decision_function(X_hidden)
        else:
            preds = model.predict_proba(X_hidden)[:, 1]
    except Exception as e:
        pytest.fail(f"Failed to generate predictions on the hidden dataset using the saved model. Ensure it accepts raw features. Error: {e}")

    auc_score = roc_auc_score(y_hidden, preds)

    # The threshold condition as specified in the verifier details
    assert auc_score >= 0.85, f"Model ROC AUC on hidden test set is {auc_score:.4f}, which is below the required threshold of 0.85. This might indicate data leakage or improper scaling."

def test_ci_txt_exists_and_format():
    ci_path = '/app/ci.txt'
    assert os.path.exists(ci_path), "The confidence interval file '/app/ci.txt' is missing."

    with open(ci_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"The file '/app/ci.txt' should contain exactly two comma-separated values (lower_bound,upper_bound), but got: '{content}'."

    try:
        lower = float(parts[0])
        upper = float(parts[1])
    except ValueError:
        pytest.fail(f"The values in '/app/ci.txt' could not be parsed as floats. Got: '{content}'.")

    assert 0.0 <= lower <= 1.0, f"Lower bound of CI ({lower}) is out of expected range [0, 1]."
    assert 0.0 <= upper <= 1.0, f"Upper bound of CI ({upper}) is out of expected range [0, 1]."
    assert lower <= upper, f"Lower bound of CI ({lower}) is greater than upper bound ({upper})."