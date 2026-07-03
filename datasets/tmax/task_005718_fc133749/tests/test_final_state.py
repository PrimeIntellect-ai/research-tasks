# test_final_state.py

import os
import json
import pytest
import subprocess

PIPELINE_PATH = "/home/user/pipeline.py"
RESULTS_PATH = "/home/user/experiment_results.json"

def test_pipeline_script_exists():
    assert os.path.exists(PIPELINE_PATH), f"File missing: {PIPELINE_PATH}"

def test_pipeline_script_env_vars():
    with open(PIPELINE_PATH, "r") as f:
        code = f.read()

    assert "OMP_NUM_THREADS" in code, "OMP_NUM_THREADS not found in pipeline.py"
    assert "OPENBLAS_NUM_THREADS" in code, "OPENBLAS_NUM_THREADS not found in pipeline.py"
    assert "MKL_NUM_THREADS" in code, "MKL_NUM_THREADS not found in pipeline.py"

def test_experiment_results_json():
    assert os.path.exists(RESULTS_PATH), f"Results file missing: {RESULTS_PATH}"

    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON")

    assert "best_alpha" in data, "Missing key 'best_alpha' in results JSON"
    assert "best_score" in data, "Missing key 'best_score' in results JSON"

    assert isinstance(data["best_alpha"], (int, float)), "'best_alpha' must be numeric"
    assert isinstance(data["best_score"], (int, float)), "'best_score' must be numeric"

def test_pipeline_execution():
    # Run the script to ensure it executes without errors and updates the JSON
    if os.path.exists(RESULTS_PATH):
        os.remove(RESULTS_PATH)

    result = subprocess.run(["python3", PIPELINE_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.py execution failed with error:\n{result.stderr}"

    assert os.path.exists(RESULTS_PATH), "pipeline.py did not generate experiment_results.json upon execution"

    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Generated {RESULTS_PATH} is not valid JSON")

    assert "best_alpha" in data, "Missing key 'best_alpha' in regenerated results JSON"
    assert "best_score" in data, "Missing key 'best_score' in regenerated results JSON"