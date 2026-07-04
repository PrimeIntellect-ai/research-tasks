# test_final_state.py
import json
import math
import os

def test_results_file_exists():
    assert os.path.exists('/home/user/results.json'), "The results file /home/user/results.json does not exist."

def test_results_content():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"File {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} is not a valid JSON file."

    assert "mean_diff" in data, "Key 'mean_diff' is missing from the results JSON."
    assert "similar_users" in data, "Key 'similar_users' is missing from the results JSON."

    expected_mean_diff = 29.133333333333333
    assert isinstance(data['mean_diff'], (int, float)), "mean_diff must be a number."
    assert math.isclose(data['mean_diff'], expected_mean_diff, rel_tol=1e-5), \
        f"mean_diff is incorrect. Expected ~{expected_mean_diff}, got {data['mean_diff']}"

    expected_similar_users = ["U_6", "U_1", "U_4"]
    assert isinstance(data['similar_users'], list), "similar_users must be a list."
    assert data['similar_users'] == expected_similar_users, \
        f"similar_users is incorrect. Expected {expected_similar_users}, got {data['similar_users']}"