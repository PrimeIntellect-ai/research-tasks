# test_final_state.py

import os
import json
import pytest

def test_impact_json_exists():
    impact_path = "/home/user/impact.json"
    assert os.path.exists(impact_path), f"Expected output file {impact_path} is missing."
    assert os.path.isfile(impact_path), f"Path {impact_path} is not a file."

def test_impact_mae():
    impact_path = "/home/user/impact.json"

    # Ground truth impact scores
    truth = {
        "Gateway": 6,
        "Auth": 2,
        "Cart": 2,
        "Catalog": 2,
        "Inventory": 1,
        "DB": 0,
        "Redis": 0
    }

    try:
        with open(impact_path, 'r') as f:
            predicted = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {impact_path} as JSON: {e}")

    errors = []
    for k, v in truth.items():
        # Default to 0 if the service was missed
        pred_val = predicted.get(k, 0)
        if not isinstance(pred_val, (int, float)):
            try:
                pred_val = float(pred_val)
            except ValueError:
                pytest.fail(f"Predicted value for {k} is not a number: {pred_val}")
        errors.append(abs(v - pred_val))

    mae = sum(errors) / len(truth)

    assert mae <= 1.5, f"Mean Absolute Error (MAE) is {mae}, which is greater than the threshold of 1.5. Predicted: {predicted}"