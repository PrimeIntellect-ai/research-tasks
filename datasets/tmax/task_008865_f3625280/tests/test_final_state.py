# test_final_state.py
import os
import json
import math

def test_result_json_exists_and_correct():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Output file {result_path} is missing."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {result_path} does not contain valid JSON."

    assert "largest_component_size" in data, "Key 'largest_component_size' is missing in JSON."
    assert "target_primer" in data, "Key 'target_primer' is missing in JSON."
    assert "stability_score" in data, "Key 'stability_score' is missing in JSON."

    assert data["largest_component_size"] == 4, f"Expected largest_component_size to be 4, got {data['largest_component_size']}."
    assert data["target_primer"] == "AAAAAAAAAAAAAAAAAAAA", f"Expected target_primer to be 'AAAAAAAAAAAAAAAAAAAA', got '{data['target_primer']}'."

    score = data["stability_score"]
    assert isinstance(score, (int, float)), f"Expected stability_score to be a number, got {type(score)}."
    assert math.isclose(score, 0.5, abs_tol=1e-4), f"Expected stability_score to be approximately 0.5 (numerically stable), got {score}."