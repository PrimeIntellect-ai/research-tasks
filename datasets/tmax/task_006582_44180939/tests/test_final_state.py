# test_final_state.py
import os
import json
import math

def test_model_persistence():
    model_path = "/home/user/best_model.pkl"
    assert os.path.isfile(model_path), f"Missing saved model file: {model_path}"
    assert os.path.getsize(model_path) > 0, f"Saved model file {model_path} is empty"

def test_pipeline_results_json():
    results_path = "/home/user/pipeline_results.json"
    assert os.path.isfile(results_path), f"Missing results JSON file: {results_path}"

    with open(results_path, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON"

    required_keys = {
        "best_alpha",
        "best_l1_ratio",
        "cv_best_score",
        "first_5_predictions",
        "inference_time_seconds"
    }
    missing_keys = required_keys - set(res.keys())
    assert not missing_keys, f"JSON report is missing required keys: {missing_keys}"

    # Check best_alpha
    assert isinstance(res["best_alpha"], (int, float)), "best_alpha must be a float"
    assert math.isclose(res["best_alpha"], 0.1, abs_tol=1e-5), f"Expected best_alpha to be 0.1, got {res['best_alpha']}"

    # Check best_l1_ratio
    assert isinstance(res["best_l1_ratio"], (int, float)), "best_l1_ratio must be a float"
    assert math.isclose(res["best_l1_ratio"], 0.9, abs_tol=1e-5), f"Expected best_l1_ratio to be 0.9, got {res['best_l1_ratio']}"

    # Check cv_best_score
    assert isinstance(res["cv_best_score"], (int, float)), "cv_best_score must be a float"
    assert math.isclose(res["cv_best_score"], 0.9790, abs_tol=0.0005), f"cv_best_score {res['cv_best_score']} is out of tolerance"

    # Check first_5_predictions
    preds = res["first_5_predictions"]
    assert isinstance(preds, list), "first_5_predictions must be a list"
    assert len(preds) == 5, f"first_5_predictions must have exactly 5 elements, got {len(preds)}"

    expected_preds = [-0.3662, 0.6970, -0.6695, 2.5085, -0.4034]
    for i, (p, e) in enumerate(zip(preds, expected_preds)):
        assert isinstance(p, (int, float)), f"Prediction at index {i} is not a float"
        assert math.isclose(p, e, abs_tol=0.0005), f"Prediction at index {i} was {p}, expected ~{e}"

    # Check inference_time_seconds
    inf_time = res["inference_time_seconds"]
    assert isinstance(inf_time, (int, float)), "inference_time_seconds must be a float"
    assert inf_time > 0.0, f"inference_time_seconds must be greater than 0.0, got {inf_time}"