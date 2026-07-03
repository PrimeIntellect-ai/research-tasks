# test_final_state.py

import os
import json
import subprocess
import pytest

def test_go_executable_exists():
    """Verify the Go program was built into an executable."""
    exe_path = "/home/user/asset_optimizer/optimizer"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_fixtures_exist_and_correct():
    """Verify the fixtures directory and files were created correctly."""
    fixtures_dir = "/home/user/fixtures"
    assert os.path.isdir(fixtures_dir), f"Directory {fixtures_dir} is missing."

    expected_fixtures = {
        "fixture_1.json": {"max_pixels": 2000000, "min_aspect": 1.3, "max_aspect": 1.4},
        "fixture_2.json": {"max_pixels": 8000000, "min_aspect": 1.7, "max_aspect": 1.8},
        "fixture_3.json": {"max_pixels": 500000, "min_aspect": 1.0, "max_aspect": 1.1}
    }

    for filename, expected_data in expected_fixtures.items():
        filepath = os.path.join(fixtures_dir, filename)
        assert os.path.isfile(filepath), f"Fixture file {filepath} is missing."
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"Fixture {filepath} is not valid JSON.")

            assert data == expected_data, f"Fixture {filepath} content {data} does not match expected {expected_data}."

def test_go_program_no_deadlock():
    """Verify the Go program runs successfully without deadlocking."""
    exe_path = "/home/user/asset_optimizer/optimizer"
    fixture_path = "/home/user/fixtures/fixture_3.json"

    try:
        result = subprocess.run([exe_path, fixture_path], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("The Go program timed out, indicating the deadlock was likely not fixed.")

    assert result.returncode == 0, f"Go program failed with return code {result.returncode} and stderr: {result.stderr}"

    try:
        output_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Go program output is not valid JSON: {result.stdout}")

    assert "Width" in output_data
    assert "Height" in output_data
    assert "Area" in output_data

def test_benchmark_results_json():
    """Verify the benchmark_results.json file exists, is valid, and has correct structure."""
    results_path = "/home/user/benchmark_results.json"
    assert os.path.isfile(results_path), f"Benchmark results file {results_path} is missing."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert isinstance(results, list), f"Expected a JSON list in {results_path}, got {type(results)}."
    assert len(results) == 3, f"Expected 3 results in {results_path}, got {len(results)}."

    expected_fixtures = [
        "/home/user/fixtures/fixture_1.json",
        "/home/user/fixtures/fixture_2.json",
        "/home/user/fixtures/fixture_3.json"
    ]

    for i, res in enumerate(results):
        assert "fixture" in res, f"Result {i} missing 'fixture' key."
        assert res["fixture"] == expected_fixtures[i], f"Result {i} 'fixture' expected {expected_fixtures[i]}, got {res['fixture']}."

        assert "time_seconds" in res, f"Result {i} missing 'time_seconds' key."
        assert isinstance(res["time_seconds"], float), f"Result {i} 'time_seconds' should be a float."

        assert "optimal_width" in res, f"Result {i} missing 'optimal_width' key."
        assert isinstance(res["optimal_width"], int), f"Result {i} 'optimal_width' should be an int."

        assert "optimal_height" in res, f"Result {i} missing 'optimal_height' key."
        assert isinstance(res["optimal_height"], int), f"Result {i} 'optimal_height' should be an int."

        assert res["optimal_width"] > 0, f"Result {i} 'optimal_width' should be > 0."
        assert res["optimal_height"] > 0, f"Result {i} 'optimal_height' should be > 0."