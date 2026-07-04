# test_final_state.py

import os
import csv
import pytest

def test_cv_results_file():
    """Verify the cv_results.csv file exists, has correct structure, and is sorted."""
    results_file = '/home/user/experiments/cv_results.csv'
    assert os.path.isfile(results_file), f"Missing cv_results.csv file: {results_file}"

    with open(results_file, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['degree', 'alpha', 'mean_mse'], f"Incorrect header in cv_results.csv: {header}"

        rows = list(reader)
        assert len(rows) == 12, f"Expected 12 rows of results, found {len(rows)}"

        degrees_alphas = set()
        mses = []
        for row in rows:
            assert len(row) == 3, f"Expected 3 columns per row, found {len(row)} in row {row}"
            degree, alpha, mean_mse = row

            try:
                d = int(degree)
                a = float(alpha)
                m = float(mean_mse)
            except ValueError as e:
                pytest.fail(f"Invalid data type in row {row}: {e}")

            assert d in [1, 2, 3, 4], f"Unexpected degree {d}"
            assert a in [0.1, 1.0, 10.0], f"Unexpected alpha {a}"

            # Check 4 decimal places formatting
            assert len(mean_mse.split('.')[-1]) <= 4 or mean_mse.endswith('0'), f"mean_mse {mean_mse} not rounded to 4 decimal places"

            degrees_alphas.add((d, a))
            mses.append(m)

        assert len(degrees_alphas) == 12, "Duplicate or missing degree/alpha combinations"

        # Check sorting
        assert mses == sorted(mses), "cv_results.csv is not sorted by mean_mse in ascending order"

def test_predictions_file():
    """Verify the predictions.txt file exists and has correct format."""
    preds_file = '/home/user/experiments/predictions.txt'
    assert os.path.isfile(preds_file), f"Missing predictions.txt file: {preds_file}"

    with open(preds_file, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 20, f"Expected 20 predictions, found {len(lines)}"

    for i, line in enumerate(lines):
        try:
            val = float(line)
        except ValueError:
            pytest.fail(f"Invalid prediction on line {i+1}: {line}")

        # Check 4 decimal places formatting
        if '.' in line:
            decimals = line.split('.')[1]
            assert len(decimals) == 4, f"Prediction {line} on line {i+1} is not formatted to exactly 4 decimal places"
        else:
            pytest.fail(f"Prediction {line} on line {i+1} is missing decimal places")