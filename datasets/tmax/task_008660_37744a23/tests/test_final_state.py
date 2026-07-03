# test_final_state.py
import os
import json
import math

def test_evaluate_go_exists():
    assert os.path.isfile("/home/user/evaluate.go"), "/home/user/evaluate.go script not found."

def test_matches_json_exists():
    assert os.path.isfile("/home/user/matches.json"), "/home/user/matches.json output file not found."

def test_matches_json_content():
    matches_path = "/home/user/matches.json"
    assert os.path.isfile(matches_path), f"{matches_path} does not exist."

    with open(matches_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{matches_path} contains invalid JSON."

    assert isinstance(data, list), "JSON output must be an array."

    expected_data = [
        {"exp_id": "expA", "closest_baseline_id": "base1", "similarity": 0.9987},
        {"exp_id": "expB", "closest_baseline_id": "base2", "similarity": 0.9945},
        {"exp_id": "expC", "closest_baseline_id": "base3", "similarity": 0.9988},
        {"exp_id": "expD", "closest_baseline_id": "base4", "similarity": 0.9991}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in JSON array, but got {len(data)}."

    # Verify it is sorted by exp_id
    exp_ids = [item.get("exp_id") for item in data]
    assert exp_ids == sorted(exp_ids), "JSON array is not sorted alphabetically by exp_id."

    # Verify content
    for expected_item in expected_data:
        # Find matching item
        actual_item = next((item for item in data if item.get("exp_id") == expected_item["exp_id"]), None)
        assert actual_item is not None, f"Missing result for experiment {expected_item['exp_id']}."

        assert actual_item.get("closest_baseline_id") == expected_item["closest_baseline_id"], \
            f"Incorrect closest_baseline_id for {expected_item['exp_id']}. Expected {expected_item['closest_baseline_id']}, got {actual_item.get('closest_baseline_id')}."

        actual_sim = actual_item.get("similarity")
        assert isinstance(actual_sim, (int, float)), f"Similarity for {expected_item['exp_id']} must be a number."
        assert math.isclose(actual_sim, expected_item["similarity"], abs_tol=1e-4), \
            f"Incorrect similarity for {expected_item['exp_id']}. Expected {expected_item['similarity']}, got {actual_sim}."