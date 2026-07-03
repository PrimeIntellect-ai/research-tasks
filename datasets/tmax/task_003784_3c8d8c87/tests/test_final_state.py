# test_final_state.py
import os
import json

def test_pipeline_results_exists():
    file_path = '/home/user/pipeline_results.json'
    assert os.path.exists(file_path), f"File {file_path} is missing. The script did not create the required output file."

def test_pipeline_results_content():
    file_path = '/home/user/pipeline_results.json'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    expected_keys = ["invalid_rows_dropped", "valid_rows_trained", "anomalies_detected"]
    for key in expected_keys:
        assert key in results, f"Key '{key}' is missing from the JSON results."

    assert results["invalid_rows_dropped"] == 5, f"Expected 5 invalid_rows_dropped, got {results['invalid_rows_dropped']}"
    assert results["valid_rows_trained"] == 21, f"Expected 21 valid_rows_trained, got {results['valid_rows_trained']}"
    assert results["anomalies_detected"] == 2, f"Expected 2 anomalies_detected, got {results['anomalies_detected']}"