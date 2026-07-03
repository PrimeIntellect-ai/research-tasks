# test_final_state.py

import os
import pytest
import requests
import pandas as pd

def test_clean_data_csv_exists_and_valid():
    """Test that /app/clean_data.csv exists and contains valid data."""
    path = '/app/clean_data.csv'
    assert os.path.exists(path), f"Expected file {path} does not exist."
    assert os.path.isfile(path), f"Expected {path} to be a file."

    df = pd.read_csv(path)

    # Check constraints
    assert (df['alpha'] >= 0.0).all(), "Some rows in clean_data.csv violate alpha >= 0.0"
    assert (df['beta'] <= 100.0).all(), "Some rows in clean_data.csv violate beta <= 100.0"
    assert df['gamma'].isin([0, 1]).all(), "Some rows in clean_data.csv violate gamma in [0, 1]"
    assert (df['target'] > 0.0).all(), "Some rows in clean_data.csv violate target > 0.0"

    # Check exact count based on truth
    assert len(df) == 139, f"Expected 139 rows in clean_data.csv, found {len(df)}"

def test_api_stats_endpoint():
    """Test the GET /stats endpoint."""
    url = "http://127.0.0.1:8080/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from /stats, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /stats is not valid JSON.")

    assert "initial_rows" in data, "Key 'initial_rows' missing in /stats response."
    assert "cleaned_rows" in data, "Key 'cleaned_rows' missing in /stats response."

    assert data["initial_rows"] == 1000, f"Expected initial_rows to be 1000, got {data['initial_rows']}"
    assert data["cleaned_rows"] == 139, f"Expected cleaned_rows to be 139, got {data['cleaned_rows']}"

def test_api_data_endpoint():
    """Test the GET /data endpoint."""
    url = "http://127.0.0.1:8080/data"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from /data, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /data is not valid JSON.")

    assert isinstance(data, list), "Expected response from /data to be a JSON array."
    assert len(data) == 139, f"Expected 139 items in /data response, got {len(data)}"

    for i, row in enumerate(data):
        assert 'alpha' in row, f"Row {i} missing 'alpha'"
        assert 'beta' in row, f"Row {i} missing 'beta'"
        assert 'gamma' in row, f"Row {i} missing 'gamma'"
        assert 'target' in row, f"Row {i} missing 'target'"

        assert row['alpha'] >= 0.0, f"Row {i} violates alpha >= 0.0: {row['alpha']}"
        assert row['beta'] <= 100.0, f"Row {i} violates beta <= 100.0: {row['beta']}"
        assert row['gamma'] in [0, 1], f"Row {i} violates gamma in [0, 1]: {row['gamma']}"
        assert row['target'] > 0.0, f"Row {i} violates target > 0.0: {row['target']}"