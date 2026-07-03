# test_final_state.py
import os
import json
import csv
import pytest

def test_experiment_summary_exists():
    filepath = '/home/user/experiment_summary.json'
    assert os.path.isfile(filepath), f"The file {filepath} does not exist. Did you save the experiment summary?"

def test_experiment_summary_contents():
    filepath = '/home/user/experiment_summary.json'
    with open(filepath, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {filepath} is not valid JSON.")

    # Recompute basic counts using stdlib
    transactions_path = '/home/user/raw_data/transactions.csv'
    queries_path = '/home/user/raw_data/queries.json'

    with open(transactions_path, 'r') as f:
        reader = csv.DictReader(f)
        transactions = list(reader)

    with open(queries_path, 'r') as f:
        queries = json.load(f)

    # Join
    query_map = {q['user_id']: q['user_query'] for q in queries}
    joined = []
    for t in transactions:
        if t['user_id'] in query_map:
            joined.append({
                'revenue': float(t['revenue']),
                'user_query': query_map[t['user_id']]
            })

    expected_initial_rows = len(joined)

    # Outliers
    valid_rows = [row for row in joined if 0 <= row['revenue'] <= 5000]
    expected_cleaned_rows = len(valid_rows)
    expected_outliers_removed = expected_initial_rows - expected_cleaned_rows

    # Check keys
    expected_keys = {
        "initial_rows",
        "outliers_removed",
        "cleaned_rows",
        "bootstrap_revenue_ci_lower",
        "bootstrap_revenue_ci_upper",
        "embedding_sum_mean"
    }
    assert set(summary.keys()) == expected_keys, f"Expected keys {expected_keys}, but found {set(summary.keys())}."

    # Assert counts
    assert summary["initial_rows"] == expected_initial_rows, f"Expected initial_rows to be {expected_initial_rows}, got {summary['initial_rows']}."
    assert summary["outliers_removed"] == expected_outliers_removed, f"Expected outliers_removed to be {expected_outliers_removed}, got {summary['outliers_removed']}."
    assert summary["cleaned_rows"] == expected_cleaned_rows, f"Expected cleaned_rows to be {expected_cleaned_rows}, got {summary['cleaned_rows']}."

    # Assert complex computed values (since sklearn and numpy random are not available in stdlib, we use the known expected values)
    assert isinstance(summary["bootstrap_revenue_ci_lower"], (int, float)), "bootstrap_revenue_ci_lower must be a float."
    assert isinstance(summary["bootstrap_revenue_ci_upper"], (int, float)), "bootstrap_revenue_ci_upper must be a float."
    assert isinstance(summary["embedding_sum_mean"], (int, float)), "embedding_sum_mean must be a float."

    assert abs(summary["bootstrap_revenue_ci_lower"] - 72.43) < 0.01, f"Expected bootstrap_revenue_ci_lower to be ~72.43, got {summary['bootstrap_revenue_ci_lower']}."
    assert abs(summary["bootstrap_revenue_ci_upper"] - 250.71) < 0.01, f"Expected bootstrap_revenue_ci_upper to be ~250.71, got {summary['bootstrap_revenue_ci_upper']}."
    assert abs(summary["embedding_sum_mean"] - 0.165) < 0.001, f"Expected embedding_sum_mean to be ~0.165, got {summary['embedding_sum_mean']}."