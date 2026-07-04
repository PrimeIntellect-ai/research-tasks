# test_final_state.py

import os
import json
import math
import pytest

def test_welford_ref_executable():
    """Check that the compiled C binary exists and is executable."""
    bin_path = "/home/user/bin/welford_ref"
    assert os.path.isfile(bin_path), f"Executable {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

    # Check that it's an ELF file
    with open(bin_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {bin_path} is not a valid ELF executable."

def test_ref_output_txt():
    """Check that ref_output.txt exists and contains the correct reference output."""
    output_path = "/home/user/output/ref_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read()

    assert "Mean: 1000000000.4999500000" in content, "ref_output.txt does not contain the correct Mean."
    assert "Sample Variance: 0.0833416667" in content, "ref_output.txt does not contain the correct Sample Variance."

def test_results_json():
    """Check that results.json exists, is valid JSON, and contains correct calculations."""
    json_path = "/home/user/output/results.json"
    assert os.path.isfile(json_path), f"File {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    required_keys = {"naive_variance", "welford_variance", "welford_mean"}
    assert required_keys.issubset(data.keys()), f"results.json is missing one or more required keys: {required_keys - data.keys()}"

    welford_var = data["welford_variance"]
    welford_mean = data["welford_mean"]
    naive_var = data["naive_variance"]

    assert isinstance(welford_var, (int, float)), "welford_variance must be a number."
    assert isinstance(welford_mean, (int, float)), "welford_mean must be a number."
    assert isinstance(naive_var, (int, float)), "naive_variance must be a number."

    assert math.isclose(welford_mean, 1000000000.4999500000, abs_tol=1e-5), \
        f"welford_mean {welford_mean} is not close to the expected value 1000000000.4999500000."

    assert math.isclose(welford_var, 0.0833416667, abs_tol=1e-5), \
        f"welford_variance {welford_var} is not close to the expected value 0.0833416667."

    assert abs(naive_var - welford_var) >= 1.0, \
        f"naive_variance ({naive_var}) is too close to welford_variance ({welford_var}). It should demonstrate catastrophic cancellation."