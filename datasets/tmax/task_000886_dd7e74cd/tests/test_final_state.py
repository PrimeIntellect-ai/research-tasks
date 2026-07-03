# test_final_state.py

import os
import json
import math

def test_results_json_exists():
    """Ensure the results file exists."""
    assert os.path.exists("/home/user/results.json"), "/home/user/results.json does not exist."

def test_results_json_content():
    """Validate the contents of results.json."""
    with open("/home/user/results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    assert "best_score" in data, "results.json is missing 'best_score'."
    assert "largest_stable_dt" in data, "results.json is missing 'largest_stable_dt'."
    assert "final_C_at_stable_dt" in data, "results.json is missing 'final_C_at_stable_dt'."

    assert data["best_score"] == 8, f"Expected best_score to be 8, got {data['best_score']}."

    expected_dt = 0.0001
    assert math.isclose(data["largest_stable_dt"], expected_dt, rel_tol=1e-5), \
        f"Expected largest_stable_dt to be {expected_dt}, got {data['largest_stable_dt']}."

    expected_C = 0.9965
    assert math.isclose(data["final_C_at_stable_dt"], expected_C, abs_tol=0.0002), \
        f"Expected final_C_at_stable_dt to be close to {expected_C}, got {data['final_C_at_stable_dt']}."