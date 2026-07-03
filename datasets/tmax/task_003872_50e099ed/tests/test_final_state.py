# test_final_state.py

import os
import pytest
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

def test_script_exists():
    path = "/home/user/clean_and_train.py"
    assert os.path.isfile(path), f"Expected script missing at {path}"

def test_model_exists():
    path = "/home/user/model.pkl"
    assert os.path.isfile(path), f"Expected model missing at {path}"

def test_model_accuracy():
    model_path = "/home/user/model.pkl"
    test_data_path = "/hidden/test.csv"

    assert os.path.isfile(model_path), f"Model file not found at {model_path}"
    assert os.path.isfile(test_data_path), f"Hidden test data not found at {test_data_path}"

    try:
        model = joblib.load(model_path)
    except Exception as e:
        pytest.fail(f"Failed to load model from {model_path}: {e}")

    df_test = pd.read_csv(test_data_path)

    expected_features = ['age', 'income', 'cat_Clothing', 'cat_Electronics', 'cat_Home & Garden', 'cat_Sports', 'cat_Toys']

    for feat in expected_features:
        assert feat in df_test.columns, f"Test data is missing expected feature: {feat}"

    assert 'target' in df_test.columns, "Test data is missing 'target' column"

    X_test = df_test[expected_features]
    y_test = df_test['target']

    try:
        y_pred = model.predict(X_test)
    except Exception as e:
        pytest.fail(f"Model prediction failed: {e}")

    accuracy = accuracy_score(y_test, y_pred)
    assert accuracy >= 0.85, f"Model accuracy {accuracy:.4f} is below the required threshold of 0.85"