# test_final_state.py
import json
import os

def test_benchmark_results():
    results_file = '/home/user/benchmark_results.json'
    assert os.path.isfile(results_file), f"Expected results file {results_file} does not exist. Did you run the script?"

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_file} is not valid JSON."

    assert "error" not in results, f"Results still contain an error: {results.get('error')}. The bug was not fixed properly."

    valid_count = results.get("valid_records_count")
    assert valid_count == 950, f"Expected valid_records_count to be 950, but got {valid_count}."

    p_value = results.get("p_value")
    assert isinstance(p_value, float), f"Expected p_value to be a float, but got {type(p_value)}."

    method_A_mean = results.get("method_A_mean_time")
    assert isinstance(method_A_mean, float), f"Expected method_A_mean_time to be a float, but got {type(method_A_mean)}."

    method_B_mean = results.get("method_B_mean_time")
    assert isinstance(method_B_mean, float), f"Expected method_B_mean_time to be a float, but got {type(method_B_mean)}."