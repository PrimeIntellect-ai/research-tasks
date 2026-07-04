# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

def test_scripts_exist():
    run_script = '/home/user/run_pipeline.sh'
    py_script = '/home/user/etl_pipeline.py'

    assert os.path.isfile(run_script), f"{run_script} is missing. The orchestrator script must be created."
    assert os.access(run_script, os.X_OK), f"{run_script} is not executable. Make sure to chmod +x the script."
    assert os.path.isfile(py_script), f"{py_script} is missing. The Python pipeline code must be written here."

def test_parquet_exists():
    parquet_path = '/home/user/processed/stratified_sample.parquet'
    assert os.path.isfile(parquet_path), f"{parquet_path} is missing. The pipeline did not save the output."

def test_parquet_content():
    """
    Reads the parquet file using a subprocess to avoid third-party imports in the test suite,
    relying on the pandas library that the student's script was supposed to install.
    """
    parquet_path = '/home/user/processed/stratified_sample.parquet'

    script = f"""
import sys
import json
try:
    import pandas as pd
except ImportError:
    print("PANDAS_MISSING")
    sys.exit(0)

try:
    df = pd.read_parquet('{parquet_path}')
    print(df.to_json(orient='records'))
except Exception as e:
    print("ERROR:", str(e))
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    output = result.stdout.strip()

    assert output != "PANDAS_MISSING", "pandas is not installed in the environment. The bash script should install requirements."
    assert not output.startswith("ERROR:"), f"Failed to read parquet file: {output}"

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"Unexpected output from parquet reader: {output}\nStderr: {result.stderr}")

    assert len(data) == 9, f"Expected exactly 9 records in the stratified sample, got {len(data)}."

    # Verify the schema
    expected_cols = {'id', 'text', 'sentiment', 'source'}
    actual_cols = set(data[0].keys())
    assert actual_cols == expected_cols, f"Expected columns {expected_cols}, got {actual_cols}."

    # Verify deterministic stratified sampling (lowest 3 IDs per sentiment)
    # Negative: 1, 3, 9
    # Neutral: 2, 8, 14
    # Positive: 5, 7, 10
    expected_ids = {1, 2, 3, 5, 7, 8, 9, 10, 14}
    actual_ids = {row['id'] for row in data}
    assert actual_ids == expected_ids, f"Stratified sampling failed. Expected IDs {expected_ids}, got {actual_ids}."

    # Verify text cleaning (lowercase, only a-z, 0-9, and spaces)
    id_10_text = next(row['text'] for row in data if row['id'] == 10)
    assert id_10_text == "great product 1010", f"Text cleaning failed for ID 10. Expected 'great product 1010', got '{id_10_text}'."

    id_3_text = next(row['text'] for row in data if row['id'] == 3)
    # The exact spacing might vary depending on how replacement was done, but alphanumeric should be intact
    assert "awful experience" in id_3_text and "terrible" in id_3_text, f"Text cleaning failed for ID 3. Got '{id_3_text}'."
    assert "-" not in id_3_text, "Text cleaning failed to remove non-alphanumeric characters (found '-')."

    # Verify sentiment mapping
    expected_sentiments = {'positive', 'neutral', 'negative'}
    actual_sentiments = {row['sentiment'] for row in data}
    assert actual_sentiments == expected_sentiments, f"Expected sentiments {expected_sentiments}, got {actual_sentiments}."

    # Verify source tracking
    id_1_source = next(row['source'] for row in data if row['id'] == 1)
    assert id_1_source == "responses.xml", f"Source tracking failed for ID 1. Expected 'responses.xml', got '{id_1_source}'."