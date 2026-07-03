# test_final_state.py

import os
import csv
import pytest

def test_evaluate_script_exists():
    """Check if the Python evaluation script exists."""
    assert os.path.isfile('/home/user/evaluate.py'), "/home/user/evaluate.py is missing"

def test_bash_script_exists():
    """Check if the Bash orchestration script exists."""
    assert os.path.isfile('/home/user/run_experiments.sh'), "/home/user/run_experiments.sh is missing"

def test_log_file_exists():
    """Check if the experiment log file exists."""
    assert os.path.isfile('/home/user/experiment_log.csv'), "/home/user/experiment_log.csv is missing"

def test_log_file_contents():
    """Check if the experiment log file has the correct contents."""
    log_file = '/home/user/experiment_log.csv'
    assert os.path.isfile(log_file), f"{log_file} does not exist."

    expected_data = {
        'data_A.csv': ('10.0', '0.835'),
        'data_B.csv': ('10.0', '3.951'),
        'data_C.csv': ('10.0', '7.994')
    }

    with open(log_file, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['dataset', 'best_alpha', 'best_mae'], f"Incorrect header in {log_file}: {header}"

        rows = list(reader)
        assert len(rows) == 3, f"Expected 3 data rows in {log_file}, got {len(rows)}"

        for row in rows:
            assert len(row) == 3, f"Malformed row in {log_file}: {row}"
            dataset, best_alpha, best_mae = row
            assert dataset in expected_data, f"Unexpected dataset {dataset} in {log_file}"

            exp_alpha, exp_mae = expected_data[dataset]

            # Allow slight floating point differences by converting to float
            try:
                alpha_val = float(best_alpha)
                mae_val = float(best_mae)
                exp_alpha_val = float(exp_alpha)
                exp_mae_val = float(exp_mae)
            except ValueError:
                pytest.fail(f"Non-numeric value found in row: {row}")

            assert abs(alpha_val - exp_alpha_val) < 1e-3, f"Incorrect best_alpha for {dataset}: expected {exp_alpha}, got {best_alpha}"
            assert abs(mae_val - exp_mae_val) < 1e-2, f"Incorrect best_mae for {dataset}: expected {exp_mae}, got {best_mae}"