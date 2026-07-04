# test_final_state.py

import os
import json
import pytest

def test_result_json_exists_and_valid():
    """Check that result.json exists and contains the correct structure."""
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Missing file: {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("result.json is not a valid JSON file.")

    expected_keys = {"success_rate", "ci_lower", "ci_upper", "ref_in_ci"}
    actual_keys = set(data.keys())
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}"

    assert isinstance(data["success_rate"], (int, float)), "success_rate must be a number"
    assert 0.0 <= data["success_rate"] <= 1.0, "success_rate must be between 0.0 and 1.0"

    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a number"
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a number"
    assert data["ci_lower"] <= data["ci_upper"], "ci_lower must be less than or equal to ci_upper"

    assert isinstance(data["ref_in_ci"], bool), "ref_in_ci must be a boolean"

def test_result_values_plausible():
    """Check that the values in result.json are plausible for the given dataset."""
    result_path = "/home/user/result.json"
    if not os.path.isfile(result_path):
        pytest.skip("result.json not found")

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Invalid JSON")

    # The dataset is highly collinear, so some solves should fail
    # success_rate should be less than 1.0
    assert data["success_rate"] < 1.0, "Expected success_rate to be < 1.0 due to singular matrices in bootstrap samples"

    # The reference w0 is 2.0. The confidence interval should ideally cover it,
    # or at least be somewhat close to it, but we mainly check that ref_in_ci is consistent
    # with the reported bounds.
    ref_w0 = 2.0
    expected_ref_in_ci = data["ci_lower"] <= ref_w0 <= data["ci_upper"]
    assert data["ref_in_ci"] == expected_ref_in_ci, (
        f"ref_in_ci is {data['ref_in_ci']}, but bounds are [{data['ci_lower']}, {data['ci_upper']}] "
        f"and ref_w0 is {ref_w0}"
    )