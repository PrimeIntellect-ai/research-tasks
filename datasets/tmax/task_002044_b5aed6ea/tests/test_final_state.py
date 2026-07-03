# test_final_state.py
import os
import pandas as pd
import pytest

def test_top5_csv_exists_and_format():
    """Test that the top5.csv file exists and has the correct format."""
    csv_path = '/home/user/top5.csv'
    assert os.path.exists(csv_path), f"Expected output file not found at {csv_path}"

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    assert 'chunk_id' in df.columns, "CSV must contain a 'chunk_id' column"
    assert 'similarity' in df.columns, "CSV must contain a 'similarity' column"
    assert len(df) >= 5, f"CSV must contain at least 5 rows, found {len(df)}"

def test_similarity_metric():
    """Test that the top 5 chunks recommended match the ground truth chunks with at least 80% accuracy."""
    csv_path = '/home/user/top5.csv'
    assert os.path.exists(csv_path), f"Expected output file not found at {csv_path}"

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    if len(df) < 5:
        pytest.fail("CSV has fewer than 5 rows.")

    ground_truth = {10, 20, 30, 40, 50}

    try:
        top_5_ids = set(df['chunk_id'].head(5).astype(int).tolist())
    except Exception as e:
        pytest.fail(f"Could not parse 'chunk_id' column as integers: {e}")

    intersection = ground_truth.intersection(top_5_ids)
    metric = len(intersection) / 5.0

    assert metric >= 0.8, (
        f"Metric value {metric} is below the threshold of 0.8. "
        f"Top 5 IDs found: {top_5_ids}, Expected subset of: {ground_truth}"
    )