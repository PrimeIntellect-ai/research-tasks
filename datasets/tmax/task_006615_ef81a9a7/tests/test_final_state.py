# test_final_state.py

import os

def test_predictions_file_exists():
    """Test that the predictions.txt file was created."""
    file_path = "/home/user/predictions.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run your script?"

def test_predictions_values():
    """Test that the predictions in the file are correct within a tolerance."""
    file_path = "/home/user/predictions.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, "The predictions.txt file is empty."

    parts = content.split(",")
    assert len(parts) == 2, f"Expected 2 comma-separated values in predictions.txt, got {len(parts)}."

    try:
        pred_lr = float(parts[0].strip())
        pred_ridge = float(parts[1].strip())
    except ValueError:
        assert False, "Could not parse the values in predictions.txt as floats."

    expected_lr = 5.9995166270422215
    expected_ridge = 5.999971936444853
    tolerance = 1e-2

    assert abs(pred_lr - expected_lr) <= tolerance, (
        f"LinearRegression prediction {pred_lr} is not within {tolerance} "
        f"of expected value {expected_lr}."
    )

    assert abs(pred_ridge - expected_ridge) <= tolerance, (
        f"Ridge prediction {pred_ridge} is not within {tolerance} "
        f"of expected value {expected_ridge}."
    )