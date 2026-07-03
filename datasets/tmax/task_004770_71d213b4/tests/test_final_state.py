# test_final_state.py
import os
import json
import pytest

def test_parquet_file_exists():
    parquet_path = '/home/user/clean_sensor_data.parquet'
    assert os.path.isfile(parquet_path), f"Expected Parquet file missing at {parquet_path}"
    assert os.path.getsize(parquet_path) > 0, f"Parquet file {parquet_path} is empty"

def test_results_json_exists():
    json_path = '/home/user/results.json'
    assert os.path.isfile(json_path), f"Expected JSON summary missing at {json_path}"

def test_results_json_content():
    json_path = '/home/user/results.json'
    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    assert "valid_rows_count" in results, "Missing key 'valid_rows_count' in results.json"
    assert results["valid_rows_count"] == 150, f"Expected 150 valid rows, got {results['valid_rows_count']}"

    assert "SENS_0042_posterior_mean" in results, "Missing key 'SENS_0042_posterior_mean' in results.json"
    mean_val = results["SENS_0042_posterior_mean"]
    assert isinstance(mean_val, (int, float)), "Posterior mean must be a number"
    assert abs(mean_val - 1.4970) < 0.0001, f"Expected posterior mean ~1.4970, got {mean_val}"

    assert "SENS_0042_posterior_variance" in results, "Missing key 'SENS_0042_posterior_variance' in results.json"
    var_val = results["SENS_0042_posterior_variance"]
    assert isinstance(var_val, (int, float)), "Posterior variance must be a number"
    assert abs(var_val - 0.0200) < 0.0001, f"Expected posterior variance ~0.0200, got {var_val}"

    assert "benchmark_avg_ms" in results, "Missing key 'benchmark_avg_ms' in results.json"
    benchmark = results["benchmark_avg_ms"]
    assert isinstance(benchmark, (int, float)), "Benchmark time must be a number"
    assert benchmark >= 0, f"Benchmark time cannot be negative, got {benchmark}"