# test_final_state.py
import os
import sys
import json
import csv
import subprocess
import pytest

def test_run_sh_exists_and_executable():
    run_script = "/home/user/run.sh"
    assert os.path.exists(run_script), f"Expected script {run_script} does not exist."
    assert os.access(run_script, os.X_OK), f"Script {run_script} is not executable."

def test_pipeline_execution_and_outputs():
    run_script = "/home/user/run.sh"

    # Execute the script with seed 123
    result = subprocess.run([run_script, "123"], capture_output=True, text=True)
    assert result.returncode == 0, f"run.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

    training_data_path = "/home/user/training_data.csv"
    stats_path = "/home/user/stats.json"

    assert os.path.exists(training_data_path), f"Output file {training_data_path} was not created."
    assert os.path.exists(stats_path), f"Output file {stats_path} was not created."

    # Compute golden values using a subprocess to avoid importing third-party libs directly in the test
    golden_script = """
import pandas as pd
from scipy import stats
import json

df = pd.read_csv('/home/user/raw_data.csv')
df = df[df['user_id'].notna()]
df = df[df['session_duration_sec'] > 0]
df = df[df['clicks'] >= 0]
df['clicks_per_minute'] = df['clicks'] / (df['session_duration_sec'] / 60)

c0 = df[df['converted'] == 0].sample(n=500, replace=True, random_state=123)
c1 = df[df['converted'] == 1].sample(n=500, replace=True, random_state=123)

t_stat, p_val = stats.ttest_ind(c1['clicks_per_minute'], c0['clicks_per_minute'], equal_var=True)
print(json.dumps({'t_statistic': t_stat, 'p_value': p_val}))
"""
    golden_result = subprocess.run([sys.executable, "-c", golden_script], capture_output=True, text=True)
    assert golden_result.returncode == 0, "Failed to compute golden values."

    golden_stats = json.loads(golden_result.stdout)

    # Verify stats.json
    with open(stats_path, 'r') as f:
        try:
            student_stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{stats_path} is not a valid JSON file.")

    assert "t_statistic" in student_stats, "stats.json missing 't_statistic' key."
    assert "p_value" in student_stats, "stats.json missing 'p_value' key."

    assert abs(student_stats["t_statistic"] - golden_stats["t_statistic"]) < 1e-4, \
        f"t_statistic mismatch. Expected approx {golden_stats['t_statistic']}, got {student_stats['t_statistic']}"
    assert abs(student_stats["p_value"] - golden_stats["p_value"]) < 1e-4, \
        f"p_value mismatch. Expected approx {golden_stats['p_value']}, got {student_stats['p_value']}"

    # Verify training_data.csv
    with open(training_data_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_columns = ['user_id', 'session_duration_sec', 'clicks', 'converted', 'clicks_per_minute']
        assert header == expected_columns, f"Columns in training_data.csv do not match expected. Got {header}"

        rows = list(reader)
        assert len(rows) == 1000, f"Expected exactly 1000 rows in training_data.csv, got {len(rows)}"