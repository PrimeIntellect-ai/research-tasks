# test_final_state.py

import os
import json
import numpy as np
import joblib
from sklearn.metrics import r2_score

def test_surrogate_model_performance():
    json_path = '/home/user/feature_correlations.json'
    model_path = '/home/user/surrogate_model.pkl'

    assert os.path.isfile(json_path), f"Missing feature correlations JSON: {json_path}"
    assert os.path.isfile(model_path), f"Missing surrogate model: {model_path}"

    with open(json_path, 'r') as f:
        try:
            ci_data = json.load(f)
        except json.JSONDecodeError:
            raise AssertionError(f"Invalid JSON format in {json_path}")

    selected_indices = []
    for i in range(20):
        fname = f"f{i}"
        assert fname in ci_data, f"Feature {fname} missing from correlations JSON"

        bounds = ci_data[fname]
        assert 'lower_bound' in bounds, f"Missing lower_bound for {fname}"
        assert 'upper_bound' in bounds, f"Missing upper_bound for {fname}"

        lower = bounds['lower_bound']
        upper = bounds['upper_bound']

        if lower > 0 or upper < 0:
            selected_indices.append(i)

    assert len(selected_indices) > 0, "No features selected based on confidence intervals."

    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise AssertionError(f"Failed to load model from {model_path}: {e}")

    assert hasattr(model, 'predict'), "Loaded model does not have a 'predict' method."

    # Generate hidden test set
    np.random.seed(42)
    X_test_full = np.random.randn(5000, 20)
    y_test = (4.5 * X_test_full[:, 3] 
              - 2.1 * X_test_full[:, 8] 
              + 3.8 * X_test_full[:, 14] 
              + 1.2 * X_test_full[:, 18] 
              + np.sin(X_test_full[:, 0]))

    X_test_selected = X_test_full[:, selected_indices]

    try:
        y_pred = model.predict(X_test_selected)
    except ValueError as e:
        raise AssertionError(f"Model prediction failed. Expected {len(selected_indices)} features. Error: {e}")

    metric_value = r2_score(y_test, y_pred)
    threshold = 0.90

    assert metric_value >= threshold, f"R^2 score {metric_value:.4f} is below the threshold of {threshold}"