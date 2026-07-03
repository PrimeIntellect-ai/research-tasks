# test_final_state.py
import os
import json
import stat
import subprocess
import pytest

def test_scripts_exist_and_executable():
    """Verify that the required scripts exist and run_pipeline.sh is executable."""
    pipeline_sh = "/home/user/run_pipeline.sh"
    variance_py = "/home/user/variance_test.py"

    assert os.path.isfile(pipeline_sh), f"{pipeline_sh} does not exist."
    assert os.path.isfile(variance_py), f"{variance_py} does not exist."

    st = os.stat(pipeline_sh)
    assert bool(st.st_mode & stat.S_IXUSR), f"{pipeline_sh} is not executable."

def test_venv_exists():
    """Verify that the virtual environment was created and contains Python."""
    python_bin = "/home/user/venv/bin/python"
    assert os.path.isfile(python_bin), "Python executable not found in /home/user/venv/bin/python. Was the venv created?"

def get_ground_truth():
    """Compute the ground truth errors using the venv's numpy."""
    script = """
import numpy as np
import json

rng = np.random.RandomState(42)
x = rng.normal(loc=1e7, scale=2.5, size=100000).astype(np.float32)

x64 = x.astype(np.float64)
true_var = np.var(x64)

naive_var = np.mean(x**2) - np.mean(x)**2
naive_error = abs(naive_var - true_var)

count = 0
mean = 0.0
M2 = 0.0
for val in x:
    count += 1
    delta = val - mean
    mean += delta / count
    delta2 = val - mean
    M2 += delta * delta2
welford_var = M2 / count
welford_error = abs(welford_var - true_var)

print(json.dumps({"naive_error": float(naive_error), "welford_error": float(welford_error)}))
"""
    result = subprocess.run(
        ["/home/user/venv/bin/python", "-c", script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        pytest.fail(f"Failed to run ground truth script using venv python. Error: {result.stderr}")
    return json.loads(result.stdout)

def test_report_json_content():
    """Verify the contents of report.json."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    expected_keys = {"naive_error", "welford_error", "welford_time_ci_low", "welford_time_ci_high"}
    assert set(report.keys()) == expected_keys, f"report.json keys {set(report.keys())} do not match expected {expected_keys}."

    for k in expected_keys:
        assert isinstance(report[k], (int, float)), f"Value for {k} must be a number."

    ci_low = report["welford_time_ci_low"]
    ci_high = report["welford_time_ci_high"]

    assert ci_low > 0, "welford_time_ci_low must be greater than 0."
    assert ci_high > 0, "welford_time_ci_high must be greater than 0."
    assert ci_low < ci_high, "welford_time_ci_low must be less than welford_time_ci_high."

    truth = get_ground_truth()

    # Check naive_error within 1%
    naive_diff = abs(report["naive_error"] - truth["naive_error"])
    assert naive_diff <= 0.01 * truth["naive_error"], \
        f"naive_error {report['naive_error']} is not within 1% of expected {truth['naive_error']}."

    # Check welford_error within 1e-3
    welford_diff = abs(report["welford_error"] - truth["welford_error"])
    assert welford_diff <= 1e-3, \
        f"welford_error {report['welford_error']} is not within 1e-3 of expected {truth['welford_error']}."