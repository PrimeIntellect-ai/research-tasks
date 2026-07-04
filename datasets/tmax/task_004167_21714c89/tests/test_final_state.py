# test_final_state.py

import os
import json
import subprocess
import pytest

def test_pcr_model_regression_test_passes():
    """Verify that the pcr_model.py script passes its regression test."""
    script_path = "/home/user/pcr_model.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    result = subprocess.run(
        ["python3", script_path, "--test"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, (
        f"pcr_model.py --test failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )
    assert "Test passed!" in result.stdout, "Expected 'Test passed!' in stdout."

def test_solution_json_exists_and_correct():
    """Verify that solution.json exists and contains the correct fitted parameters and primer."""
    solution_path = "/home/user/solution.json"
    assert os.path.isfile(solution_path), f"Solution file not found at {solution_path}"

    with open(solution_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{solution_path} is not a valid JSON file.")

    assert "fitted_r" in data, "Missing 'fitted_r' in solution.json"
    assert "fitted_K" in data, "Missing 'fitted_K' in solution.json"
    assert "primer_id" in data, "Missing 'primer_id' in solution.json"

    fitted_r = float(data["fitted_r"])
    fitted_K = float(data["fitted_K"])
    primer_id = str(data["primer_id"])

    # Check fitted_r with a tolerance of 0.02
    assert abs(fitted_r - 0.85) <= 0.02, f"fitted_r {fitted_r} is not within tolerance of 0.85"

    # Check fitted_K with a tolerance of 0.02
    assert abs(fitted_K - 120.0) <= 0.02, f"fitted_K {fitted_K} is not within tolerance of 120.0"

    # Check primer_id
    assert primer_id == "primer2", f"Expected primer_id 'primer2', but got '{primer_id}'"