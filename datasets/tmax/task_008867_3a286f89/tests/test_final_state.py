# test_final_state.py

import os
import json
import csv
import re
import math
import pytest

RAW_LOGS_PATH = '/home/user/data/raw_logs.jsonl'
CLEAN_LOGS_PATH = '/home/user/data/clean_logs.csv'
RESULTS_PATH = '/home/user/etl_output/results.json'

def compute_expected_data():
    """Parse raw logs and compute expected intermediate data."""
    expected_rows = []
    with open(RAW_LOGS_PATH, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            # 1. lowercase
            text = row['text'].lower()
            # 2. remove punctuation (keep word chars and whitespace)
            text = re.sub(r'[^\w\s]', '', text)
            # 3. split by whitespace
            tokens = text.split()
            # 4. filter > 10
            if len(tokens) > 10:
                expected_rows.append({
                    'id': str(row['id']),
                    'experiment_group': row['experiment_group'],
                    'resolution_time': float(row['resolution_time']),
                    'token_count': len(tokens)
                })
    return expected_rows

def test_clean_logs_csv():
    """Validate the clean_logs.csv file structure and contents."""
    assert os.path.isfile(CLEAN_LOGS_PATH), f"File {CLEAN_LOGS_PATH} does not exist."

    expected_rows = compute_expected_data()

    with open(CLEAN_LOGS_PATH, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['id', 'experiment_group', 'resolution_time', 'token_count'], \
            f"CSV headers are incorrect. Got: {headers}"

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in CSV, got {len(actual_rows)}."

    # Check a sample of rows to ensure correctness
    expected_dict = {r['id']: r for r in expected_rows}
    for row in actual_rows:
        row_id = row[0]
        assert row_id in expected_dict, f"Unexpected ID {row_id} in clean_logs.csv"
        exp = expected_dict[row_id]
        assert row[1] == exp['experiment_group'], f"Group mismatch for ID {row_id}"
        assert math.isclose(float(row[2]), exp['resolution_time'], rel_tol=1e-5), \
            f"Resolution time mismatch for ID {row_id}"
        assert int(row[3]) == exp['token_count'], f"Token count mismatch for ID {row_id}"

def test_results_json():
    """Validate the results.json file structure and calculated metrics."""
    assert os.path.isfile(RESULTS_PATH), f"File {RESULTS_PATH} does not exist."

    with open(RESULTS_PATH, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    expected_keys = {
        "valid_records", "group_a_mean", "group_b_mean",
        "ci_lower", "ci_upper", "p_value"
    }
    assert set(results.keys()) == expected_keys, \
        f"results.json keys mismatch. Expected {expected_keys}, got {set(results.keys())}"

    expected_rows = compute_expected_data()

    group_a = [r['resolution_time'] for r in expected_rows if r['experiment_group'] == 'A']
    group_b = [r['resolution_time'] for r in expected_rows if r['experiment_group'] == 'B']

    mean_a = sum(group_a) / len(group_a)
    mean_b = sum(group_b) / len(group_b)

    assert results["valid_records"] == len(expected_rows), \
        f"valid_records mismatch. Expected {len(expected_rows)}, got {results['valid_records']}"

    assert math.isclose(results["group_a_mean"], round(mean_a, 4), rel_tol=1e-4), \
        f"group_a_mean mismatch. Expected {round(mean_a, 4)}, got {results['group_a_mean']}"

    assert math.isclose(results["group_b_mean"], round(mean_b, 4), rel_tol=1e-4), \
        f"group_b_mean mismatch. Expected {round(mean_b, 4)}, got {results['group_b_mean']}"

    # Verify the specific statistical values based on the deterministic seed
    # Since exact t-distribution critical values and p-values require scipy,
    # we use the known deterministic output for these specific fields.
    assert math.isclose(results["ci_lower"], 2.5833, rel_tol=1e-3), \
        f"ci_lower mismatch. Expected ~2.5833, got {results['ci_lower']}"

    assert math.isclose(results["ci_upper"], 7.0583, rel_tol=1e-3), \
        f"ci_upper mismatch. Expected ~7.0583, got {results['ci_upper']}"

    assert math.isclose(results["p_value"], 0.0000, abs_tol=1e-4), \
        f"p_value mismatch. Expected ~0.0000, got {results['p_value']}"