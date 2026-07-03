# test_final_state.py
import os
import csv
import pytest

def test_predictions_file_exists():
    pred_path = "/home/user/predictions.csv"
    assert os.path.exists(pred_path), f"The output file {pred_path} was not found."
    assert os.path.isfile(pred_path), f"{pred_path} is not a file."

def test_predictions_mse():
    truth_path = "/home/user/truth_predictions.csv"
    pred_path = "/home/user/predictions.csv"

    assert os.path.exists(truth_path), f"Truth file {truth_path} missing."
    assert os.path.exists(pred_path), f"Predictions file {pred_path} missing."

    truth = {}
    with open(truth_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            truth[(row["user_id"], row["target_item_id"])] = float(row["predicted_ctr"])

    preds = {}
    with open(pred_path) as f:
        reader = csv.DictReader(f)
        assert "user_id" in reader.fieldnames and "target_item_id" in reader.fieldnames and "predicted_ctr" in reader.fieldnames, \
            "Predictions file is missing required columns: user_id, target_item_id, predicted_ctr"

        for row in reader:
            try:
                preds[(row["user_id"], row["target_item_id"])] = float(row["predicted_ctr"])
            except ValueError:
                pytest.fail(f"Invalid predicted_ctr value for {row['user_id']}, {row['target_item_id']}")

    missing_keys = set(truth.keys()) - set(preds.keys())
    assert not missing_keys, f"Predictions file is missing predictions for queries: {missing_keys}"

    mse = 0.0
    for k in truth:
        err = truth[k] - preds[k]
        mse += err * err
    mse /= len(truth)

    threshold = 0.0001
    assert mse <= threshold, f"MSE is {mse:.6f}, which is greater than the threshold {threshold}. Predictions are not accurate enough."