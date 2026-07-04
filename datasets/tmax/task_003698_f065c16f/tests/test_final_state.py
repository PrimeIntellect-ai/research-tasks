# test_final_state.py
import os
import pytest

def test_pipeline_log_exists_and_content():
    log_path = '/home/user/outputs/pipeline.log'
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_steps = [
        "Step extract completed",
        "Step clean completed",
        "Step extract_features completed",
        "Step load completed"
    ]

    for step in expected_steps:
        assert step in content, f"Expected log entry '{step}' not found in {log_path}."

def test_final_parquet_exists_and_valid():
    try:
        import pandas as pd
    except ImportError:
        pytest.fail("pandas is not installed, but it is required to verify the parquet output.")

    parquet_path = '/home/user/outputs/final_catalog.parquet'
    assert os.path.isfile(parquet_path), f"The final output file {parquet_path} does not exist."

    try:
        df = pd.read_parquet(parquet_path)
    except Exception as e:
        pytest.fail(f"Failed to read {parquet_path} as a Parquet file: {e}")

    assert len(df) == 4, f"Expected 4 rows in the final dataset, got {len(df)}."

    expected_columns = {'id', 'desc', 'category', 'price', 'stock'}
    assert set(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {set(df.columns)}."

    # Verify P001
    p1 = df[df['id'] == 'P001']
    assert len(p1) == 1, "Expected exactly one row for P001."
    p1 = p1.iloc[0]
    assert p1['desc'] == 'Running shoes (黒)', f"Incorrect normalized description for P001: {p1['desc']}"
    assert p1['category'] == 'Footwear', f"Incorrect category for P001: {p1['category']}"
    assert float(p1['price']) == 89.99, f"Incorrect price for P001: {p1['price']}"
    assert int(p1['stock']) == 120, f"Incorrect stock for P001: {p1['stock']}"

    # Verify P002
    p2 = df[df['id'] == 'P002']
    assert len(p2) == 1, "Expected exactly one row for P002."
    p2 = p2.iloc[0]
    assert p2['desc'] == 'Camiseta de algodón XL', f"Incorrect normalized description for P002: {p2['desc']}"
    assert p2['category'] == 'Apparel', f"Incorrect category for P002: {p2['category']}"

    # Verify P003
    p3 = df[df['id'] == 'P003']
    assert len(p3) == 1, "Expected exactly one row for P003."
    p3 = p3.iloc[0]
    assert p3['desc'] == 'Televisor 4K 55"', f"Incorrect normalized description for P003: {p3['desc']}"
    assert p3['category'] == 'Other', f"Incorrect category for P003: {p3['category']}"

    # Verify P005
    p5 = df[df['id'] == 'P005']
    assert len(p5) == 1, "Expected exactly one row for P005."
    p5 = p5.iloc[0]
    assert p5['desc'] == 'Classic シャツ', f"Incorrect normalized description for P005: {p5['desc']}"
    assert p5['category'] == 'Apparel', f"Incorrect category for P005: {p5['category']}"