# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def test_parquet_exists_and_types():
    """
    Validates that the cleaned.parquet file exists, and that the review_id and user_id 
    columns are integer types. Also ensures there are no nulls in is_verified.
    Uses a subprocess to read the parquet file via pandas (which the student must have installed).
    """
    path = '/home/user/processed/cleaned.parquet'
    assert os.path.exists(path), f"{path} does not exist. The ETL pipeline did not save the output."

    code = f"""
import pandas as pd
import json
try:
    df = pd.read_parquet('{path}')
    dtypes = df.dtypes.astype(str).to_dict()
    nulls = df.isnull().sum().to_dict()
    print(json.dumps({{"dtypes": dtypes, "nulls": nulls}}))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
"""
    res = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
    assert res.returncode == 0, f"Error running pandas check: {res.stderr}"

    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse subprocess output: {res.stdout}")

    assert "error" not in data, f"Failed to read parquet file: {data.get('error')}"

    dtypes = data['dtypes']
    assert 'review_id' in dtypes, "review_id column missing from the parquet file"
    assert 'user_id' in dtypes, "user_id column missing from the parquet file"
    assert 'is_verified' in dtypes, "is_verified column missing from the parquet file"

    # Check if they are integer types (e.g., 'Int64', 'int64', 'int32')
    assert 'int' in dtypes['review_id'].lower(), f"review_id is not an integer type, got {dtypes['review_id']}"
    assert 'int' in dtypes['user_id'].lower(), f"user_id is not an integer type, got {dtypes['user_id']}"

    nulls = data['nulls']
    assert nulls.get('is_verified', 0) == 0, "is_verified column still contains null values"

def test_top_3_json():
    """
    Validates that top_3.json contains the exact sequence of 3 review_ids 
    most similar to the query.
    """
    path = '/home/user/processed/top_3.json'
    assert os.path.exists(path), f"{path} does not exist"

    with open(path, 'r') as f:
        try:
            top_3 = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("top_3.json is not valid JSON")

    assert isinstance(top_3, list), "top_3.json should contain a JSON list"
    assert len(top_3) == 3, f"Expected exactly 3 review_ids, got {len(top_3)}"

    # The expected IDs based on cosine similarity with all-MiniLM-L6-v2
    expected = [104, 110, 102]
    assert top_3 == expected, f"Expected top 3 review_ids to be {expected}, got {top_3}"

def test_stats_json():
    """
    Validates that stats.json contains the correct p-value for the Welch's t-test.
    """
    path = '/home/user/processed/stats.json'
    assert os.path.exists(path), f"{path} does not exist"

    with open(path, 'r') as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("stats.json is not valid JSON")

    assert "p_value" in stats, "stats.json is missing the 'p_value' key"
    p_value = stats["p_value"]
    assert isinstance(p_value, float), "p_value should be a float"

    # Compute expected p-value using scipy in a subprocess
    true_lengths = [45, 55, 49, 56, 54, 48]
    false_lengths = [40, 31, 42, 47]

    code = f"""
import scipy.stats
p = scipy.stats.ttest_ind({true_lengths}, {false_lengths}, equal_var=False).pvalue
print(p)
"""
    res = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
    if res.returncode == 0:
        expected_p = float(res.stdout.strip())
    else:
        # Fallback approximate p-value if scipy is somehow missing in the test env
        expected_p = 0.03345

    assert math.isclose(p_value, expected_p, rel_tol=1e-2), f"Expected p-value approximately {expected_p}, got {p_value}"