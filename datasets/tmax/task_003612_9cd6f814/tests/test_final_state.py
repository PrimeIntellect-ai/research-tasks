# test_final_state.py
import os
import json
import pytest

def test_analyze_script_exists():
    script_path = '/home/user/analyze.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_tracking_json_exists_and_correct():
    json_path = '/home/user/tracking.json'
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert "prior_alpha" in data, "Missing 'prior_alpha' in JSON."
    assert "prior_beta" in data, "Missing 'prior_beta' in JSON."
    assert data["prior_alpha"] == 2, f"Expected prior_alpha to be 2, got {data['prior_alpha']}."
    assert data["prior_beta"] == 2, f"Expected prior_beta to be 2, got {data['prior_beta']}."

    assert "results" in data, "Missing 'results' in JSON."
    assert isinstance(data["results"], list), "'results' should be a list."

    expected_results = [
        {"dataset_id": "alpha", "posterior_mean": 0.5862},
        {"dataset_id": "beta", "posterior_mean": 0.7083},
        {"dataset_id": "gamma", "posterior_mean": 0.8704}
    ]

    assert len(data["results"]) == len(expected_results), f"Expected {len(expected_results)} results, got {len(data['results'])}."

    for i, expected in enumerate(expected_results):
        actual = data["results"][i]
        assert "dataset_id" in actual, f"Result {i} missing 'dataset_id'."
        assert "posterior_mean" in actual, f"Result {i} missing 'posterior_mean'."
        assert actual["dataset_id"] == expected["dataset_id"], f"Expected dataset_id {expected['dataset_id']}, got {actual['dataset_id']}."
        assert actual["posterior_mean"] == expected["posterior_mean"], f"Expected posterior_mean {expected['posterior_mean']} for {expected['dataset_id']}, got {actual['posterior_mean']}."

def test_results_sorted():
    json_path = '/home/user/tracking.json'
    if not os.path.isfile(json_path):
        pytest.skip("tracking.json not found")

    with open(json_path, 'r') as f:
        data = json.load(f)

    dataset_ids = [r["dataset_id"] for r in data.get("results", []) if "dataset_id" in r]
    assert dataset_ids == sorted(dataset_ids), "The 'results' list is not sorted alphabetically by 'dataset_id'."