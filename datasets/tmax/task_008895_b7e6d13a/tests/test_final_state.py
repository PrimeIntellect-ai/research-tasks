# test_final_state.py

import os
import json

def test_benchmark_plot_exists_and_not_empty():
    plot_path = '/home/user/benchmark_plot.png'
    assert os.path.isfile(plot_path), f"Plot file {plot_path} does not exist. Did you run the script?"
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."

def test_benchmark_results_json():
    json_path = '/home/user/benchmark_results.json'
    assert os.path.isfile(json_path), f"Results file {json_path} does not exist. Did you run the script?"

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert "correlation" in results, "Key 'correlation' is missing from the JSON results."
    assert "covariance" in results, "Key 'covariance' is missing from the JSON results."

    expected_corr = 0.9998
    expected_cov = 3060.7143

    assert abs(results["correlation"] - expected_corr) < 1e-4, \
        f"Expected correlation around {expected_corr}, got {results['correlation']}. Check your outlier/NaN filtering logic."
    assert abs(results["covariance"] - expected_cov) < 1e-4, \
        f"Expected covariance around {expected_cov}, got {results['covariance']}. Check your outlier/NaN filtering logic."

def test_script_modifications():
    script_path = '/home/user/etl_benchmark.py'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "plt.show()" not in content, "plt.show() should be removed from the script to fix headless execution."