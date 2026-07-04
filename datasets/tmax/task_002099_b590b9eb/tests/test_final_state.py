# test_final_state.py

import os
import json
import math
import pytest

# Expected values derived from the canonical solution using fixed random seed
EXPECTED_MSE = 6.945229672076046
EXPECTED_PREDS = [
    0.28187834241648214,
    1.1093116467008127,
    1.071850699049448,
    -0.12920700512803875,
    -0.5694389635091218,
    0.43574163013860293,
    -0.012564245976523916,
    -0.6622431969894488,
    0.3150824883446549,
    -0.06540601550993098
]

def test_results_json_exists():
    """Check if the results.json file was generated."""
    assert os.path.exists("/home/user/results.json"), "/home/user/results.json does not exist."
    assert os.path.isfile("/home/user/results.json"), "/home/user/results.json is not a file."

def test_results_json_content():
    """Validate the content of results.json."""
    with open("/home/user/results.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not a valid JSON file.")

    assert "test_mse" in results, "Key 'test_mse' is missing in results.json."
    assert "avg_inference_time_sec" in results, "Key 'avg_inference_time_sec' is missing in results.json."
    assert "predictions" in results, "Key 'predictions' is missing in results.json."

    # Check types
    assert isinstance(results["test_mse"], (int, float)), "'test_mse' must be a float."
    assert isinstance(results["avg_inference_time_sec"], (int, float)), "'avg_inference_time_sec' must be a float."
    assert isinstance(results["predictions"], list), "'predictions' must be a list."

    # Check inference time
    assert results["avg_inference_time_sec"] > 0, "'avg_inference_time_sec' must be greater than 0."

    # Check MSE
    assert math.isclose(results["test_mse"], EXPECTED_MSE, rel_tol=1e-4, abs_tol=1e-4), \
        f"Expected test_mse to be close to {EXPECTED_MSE}, got {results['test_mse']}."

    # Check predictions
    preds = results["predictions"]
    assert len(preds) == 10, f"Expected 10 predictions, got {len(preds)}."

    for i, (pred, exp) in enumerate(zip(preds, EXPECTED_PREDS)):
        assert isinstance(pred, (int, float)), f"Prediction at index {i} is not a float."
        assert math.isclose(pred, exp, rel_tol=1e-4, abs_tol=1e-4), \
            f"Prediction at index {i} expected to be close to {exp}, got {pred}."

def test_run_pipeline_script_exists():
    """Check if the run_pipeline.py script exists."""
    assert os.path.exists("/home/user/run_pipeline.py"), "/home/user/run_pipeline.py does not exist."
    assert os.path.isfile("/home/user/run_pipeline.py"), "/home/user/run_pipeline.py is not a file."