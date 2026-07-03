# test_final_state.py
import json
import os
import pytest

def test_final_results_exists_and_correct():
    results_path = '/home/user/pipeline/final_results.json'
    assert os.path.isfile(results_path), f"{results_path} is missing. Did you run query_data.py?"

    try:
        with open(results_path, 'r') as f:
            results = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse {results_path} as JSON.")

    assert isinstance(results, dict), "final_results.json must contain a JSON dictionary."
    assert len(results) == 500, f"Expected exactly 500 keys in final_results.json, got {len(results)}. The race condition may not be fully fixed."

    data_dir = '/home/user/pipeline/data'
    assert os.path.isdir(data_dir), f"{data_dir} directory is missing."

    for i in range(500):
        filename = f'file_{i}.json'
        assert filename in results, f"'{filename}' is missing from final_results.json."

        filepath = os.path.join(data_dir, filename)
        assert os.path.isfile(filepath), f"Data file {filepath} is missing."

        with open(filepath, 'r') as f:
            data = json.load(f)

        values = data.get('values', [])

        # The correct formula is: 73 * Sum(data[i] * (i + 1))
        expected_score = 73 * sum(val * (idx + 1) for idx, val in enumerate(values))
        actual_score = results[filename]

        assert actual_score == expected_score, (
            f"Incorrect score for {filename}. "
            f"Expected {expected_score}, but got {actual_score}. "
            "Check that fast_math.c correctly implements `multiplier * Sum(data[i] * (i + 1))` "
            "and that the multiplier from liblegacy.so is correct."
        )