# test_final_state.py
import os
import json
import math

def test_results_json_exists():
    """Check that the results.json file was created."""
    assert os.path.isfile("/home/user/results.json"), "/home/user/results.json is missing"

def test_results_json_content():
    """Check the contents of results.json for correct keys and reasonable values."""
    with open("/home/user/results.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/results.json is not valid JSON"

    expected_keys = {"flawed_mean_auc", "corrected_mean_auc", "p_value"}
    assert set(results.keys()) == expected_keys, f"results.json keys do not match expected. Got {list(results.keys())}"

    flawed_auc = results["flawed_mean_auc"]
    corrected_auc = results["corrected_mean_auc"]
    p_value = results["p_value"]

    assert isinstance(flawed_auc, float), "flawed_mean_auc must be a float"
    assert isinstance(corrected_auc, float), "corrected_mean_auc must be a float"
    assert isinstance(p_value, float), "p_value must be a float"

    # Check approximate values based on the ground truth
    assert math.isclose(flawed_auc, 0.8710, abs_tol=0.01), f"flawed_mean_auc {flawed_auc} is not within expected range (~0.8710)"
    assert math.isclose(corrected_auc, 0.8654, abs_tol=0.01), f"corrected_mean_auc {corrected_auc} is not within expected range (~0.8654)"

    # Corrected AUC should generally be lower than flawed AUC due to fixed data leakage
    assert corrected_auc < flawed_auc, "corrected_mean_auc should be lower than flawed_mean_auc due to removed data leakage"

    # p-value should be a valid probability
    assert 0.0 <= p_value <= 1.0, f"p_value {p_value} is not a valid probability"

def test_etl_pipeline_modified():
    """Check that the etl_pipeline.py script was modified to include a Pipeline."""
    assert os.path.isfile("/home/user/etl_pipeline.py"), "/home/user/etl_pipeline.py is missing"
    with open("/home/user/etl_pipeline.py", "r") as f:
        content = f.read()

    assert "Pipeline" in content or "make_pipeline" in content, "The ETL script does not seem to use a scikit-learn Pipeline"