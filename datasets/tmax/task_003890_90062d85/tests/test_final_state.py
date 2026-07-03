# test_final_state.py
import os
import json

def test_results_json_exists_and_valid():
    results_path = '/home/user/sim/results.json'
    assert os.path.isfile(results_path), f"File {results_path} is missing."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} is not valid JSON."

    required_keys = ["A_map", "lambda_map", "B_map", "A_kde_peak"]
    for key in required_keys:
        assert key in results, f"Key '{key}' missing from results.json."
        assert isinstance(results[key], (int, float)), f"Value for '{key}' must be a float."

    assert abs(results["A_map"] - 4.88) < 0.2, f"A_map value {results['A_map']} is not within expected range."
    assert abs(results["lambda_map"] - 0.47) < 0.1, f"lambda_map value {results['lambda_map']} is not within expected range."

def test_posterior_image_exists():
    image_path = '/home/user/sim/posterior_A.png'
    assert os.path.isfile(image_path), f"Image file {image_path} is missing."

    # Check if it's a valid PNG file by reading the magic number
    with open(image_path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"File {image_path} is not a valid PNG image."

def test_pytest_log_exists_and_passed():
    log_path = '/home/user/sim/test_results.log'
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        log_content = f.read()

    assert "passed" in log_content.lower(), f"Pytest log {log_path} does not indicate a passed test."

def test_scripts_exist():
    assert os.path.isfile('/home/user/sim/run_analysis.py'), "Script run_analysis.py is missing."
    assert os.path.isfile('/home/user/sim/test_model.py'), "Test script test_model.py is missing."