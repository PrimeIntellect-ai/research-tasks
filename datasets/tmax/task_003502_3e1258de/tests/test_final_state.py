# test_final_state.py

import os
import json
import math
import pytest

def test_venv_exists():
    """Check if the virtual environment was created."""
    venv_python = "/home/user/scienv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment Python executable not found at {venv_python}."

def test_script_modified():
    """Check if the stiff_model.py script was modified correctly."""
    script_path = "/home/user/stiff_model.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "BDF" in content, "The script does not use the 'BDF' method."
    assert "1e-6" in content, "The script does not set rtol=1e-6."
    assert "1e-10" in content, "The script does not set atol=1e-10."

def test_results_json():
    """Check if the results.json file exists and contains the correct values."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The results file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    assert "y1_final" in data, "Missing 'y1_final' in results.json"
    assert "y2_final" in data, "Missing 'y2_final' in results.json"
    assert "y3_final" in data, "Missing 'y3_final' in results.json"

    y1 = data["y1_final"]
    y2 = data["y2_final"]
    y3 = data["y3_final"]

    assert math.isclose(y1, 0.002078, rel_tol=1e-3), f"y1_final incorrect: {y1}"
    assert math.isclose(y2, 8.44e-9, rel_tol=1e-3), f"y2_final incorrect: {y2}"
    assert math.isclose(y3, 0.9979, rel_tol=1e-3), f"y3_final incorrect: {y3}"