# test_final_state.py
import os
import csv
import subprocess

def test_success_log():
    path = '/home/user/success.log'
    assert os.path.isfile(path), f"File {path} is missing. The script did not complete successfully."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "DATASET_GENERATED", f"Expected 'DATASET_GENERATED' in {path}, got '{content}'."

def test_training_data_csv_structure():
    path = '/home/user/training_data.csv'
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"File {path} is empty."

        expected_header = ['y1_initial', 'y2_initial', 'y1_final', 'y2_final']
        assert header == expected_header, f"Header mismatch in {path}: expected {expected_header}, got {header}"

        rows = list(reader)
        assert len(rows) == 100, f"Expected exactly 100 data rows in {path}, got {len(rows)}"

def test_training_data_values_via_venv():
    venv_python = '/home/user/venv/bin/python'
    assert os.path.isfile(venv_python), "Virtual environment python not found at /home/user/venv/bin/python. Did you create the venv?"

    # We use the agent's virtual environment to run the validation script, avoiding third-party imports in the pytest file.
    validation_script = """
import sys
try:
    import numpy as np
    import pandas as pd
    from scipy.integrate import solve_ivp
except ImportError as e:
    sys.exit(f"Missing required package in venv: {e}")

def vdp(t, y, mu=3.0):
    return [y[1], mu * (1 - y[0]**2) * y[1] - y[0]]

np.random.seed(42)
y0_mc = np.random.uniform(-3.0, 3.0, size=(100, 2))

truth_data = []
for y0 in y0_mc:
    sol = solve_ivp(vdp, [0, 10.0], y0, method='BDF', rtol=1e-6, atol=1e-8)
    truth_data.append({
        'y1_initial': y0[0],
        'y2_initial': y0[1],
        'y1_final': sol.y[0, -1],
        'y2_final': sol.y[1, -1]
    })

df_truth = pd.DataFrame(truth_data)
try:
    df_agent = pd.read_csv('/home/user/training_data.csv')
except Exception as e:
    sys.exit(f"Failed to read CSV: {e}")

if not np.allclose(df_truth['y1_initial'].values, df_agent['y1_initial'].values, atol=1e-5):
    sys.exit("Initial y1 states mismatch. Check your random seed and sampling logic.")
if not np.allclose(df_truth['y2_initial'].values, df_agent['y2_initial'].values, atol=1e-5):
    sys.exit("Initial y2 states mismatch. Check your random seed and sampling logic.")
if not np.allclose(df_truth['y1_final'].values, df_agent['y1_final'].values, atol=1e-2):
    sys.exit("Final y1 states mismatch. Check your ODE integration logic and parameters.")
if not np.allclose(df_truth['y2_final'].values, df_agent['y2_final'].values, atol=1e-2):
    sys.exit("Final y2 states mismatch. Check your ODE integration logic and parameters.")

print("VALIDATION_SUCCESS")
"""
    result = subprocess.run([venv_python, '-c', validation_script], capture_output=True, text=True)

    error_msg = f"Data validation failed.\nSTDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}"
    assert result.returncode == 0, error_msg
    assert "VALIDATION_SUCCESS" in result.stdout, error_msg