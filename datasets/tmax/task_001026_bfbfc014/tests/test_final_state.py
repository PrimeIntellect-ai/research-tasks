# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_edges_csv():
    path = "/home/user/edges.csv"
    assert os.path.exists(path), f"File {path} does not exist."

    try:
        df = pd.read_csv(path)
    except Exception as e:
        pytest.fail(f"Failed to read {path} as CSV: {e}")

    expected_cols = ['source', 'target', 'weight']
    assert list(df.columns) == expected_cols, f"edges.csv columns are incorrect. Expected {expected_cols}, got {list(df.columns)}"
    assert len(df) == 4, f"edges.csv should have 4 rows, found {len(df)}."

def test_awk_bug_fixed():
    path = "/app/pagerank-awk-1.0/pr.awk"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check that the bug was modified
    # The original buggy line was `base = 1 - d;`
    assert "base = 1 - d" not in content.replace(" ", ""), f"The bug `base = 1 - d` is still present in {path}."
    assert "/N" in content, f"The fix dividing by N was not found in {path}."

def exact_root(p):
    # Solve X^3 + X - P = 0
    roots = np.roots([1, 0, 1, -p])
    # Return the real root
    return roots[np.isreal(roots)][0].real

def test_training_data_metric():
    path = "/home/user/training_data.csv"
    assert os.path.exists(path), f"File {path} does not exist."

    try:
        df = pd.read_csv(path)
    except Exception as e:
        pytest.fail(f"Failed to read {path}: {e}")

    expected_cols = ['Node', 'PageRank', 'Derived_X']
    assert list(df.columns) == expected_cols, f"Incorrect columns in {path}. Expected {expected_cols}, got {list(df.columns)}."

    # Check sorting by Node ID
    assert df['Node'].is_monotonic_increasing, "The rows in training_data.csv must be sorted numerically by Node ID."

    # Check that PageRanks sum to 1.0 (verifies that the awk bug was fixed and ran correctly)
    sum_pr = df['PageRank'].sum()
    assert np.isclose(sum_pr, 1.0, atol=1e-3), f"PageRanks sum to {sum_pr}, expected 1.0. The awk bug might not be properly fixed or script wasn't re-run."

    # Re-derive the exact roots
    df['Expected_X'] = df['PageRank'].apply(exact_root)

    # Compute Maximum Absolute Error (MAE)
    mae = np.max(np.abs(df['Derived_X'] - df['Expected_X']))

    threshold = 1e-4
    assert mae <= threshold, f"FAIL: MAE {mae} > {threshold}. The derived features are not accurate enough."