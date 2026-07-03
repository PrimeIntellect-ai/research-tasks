# test_final_state.py
import os
import json
import subprocess
import math
import pytest

def test_venv_and_dependencies():
    venv_python = "/home/user/venv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment python not found at {venv_python}"

    # Check if pandas, scipy, matplotlib are installed in the venv
    result = subprocess.run([venv_python, "-c", "import pandas, scipy, matplotlib"], capture_output=True, text=True)
    assert result.returncode == 0, f"Dependencies not installed in venv. Error: {result.stderr}"

def test_plot_exists():
    plot_path = "/home/user/artifacts/correlation_plot.png"
    assert os.path.isfile(plot_path), f"Plot file not found at {plot_path}"
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty"

def test_report_json_correctness():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report JSON not found at {report_path}"

    with open(report_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    expected_keys = {
        "correlation_coefficient",
        "correlation_p_value",
        "t_statistic",
        "t_test_p_value"
    }
    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(results.keys())}"

    # Compute expected values
    venv_python = "/home/user/venv/bin/python"
    compute_script = """
import pandas as pd
import scipy.stats as stats
import json

df = pd.read_csv('/home/user/experiments.csv')
corr, p_corr = stats.pearsonr(df['learning_rate'], df['val_loss'])
t_stat, p_t = stats.ttest_ind(
    df[df['architecture'] == 'Arch_A']['val_loss'],
    df[df['architecture'] == 'Arch_B']['val_loss'],
    equal_var=True
)

expected = {
    "correlation_coefficient": round(corr, 4),
    "correlation_p_value": round(p_corr, 4),
    "t_statistic": round(t_stat, 4),
    "t_test_p_value": round(p_t, 4)
}
print(json.dumps(expected))
"""
    result = subprocess.run([venv_python, "-c", compute_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute expected values: {result.stderr}"

    expected_results = json.loads(result.stdout)

    for key in expected_keys:
        expected_val = expected_results[key]
        actual_val = results[key]
        assert isinstance(actual_val, (int, float)), f"Value for {key} must be a number"
        assert math.isclose(actual_val, expected_val, rel_tol=1e-4, abs_tol=1e-4), \
            f"Expected {key} to be {expected_val}, but got {actual_val}"