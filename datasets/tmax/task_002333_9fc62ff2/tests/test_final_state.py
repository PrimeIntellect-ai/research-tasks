# test_final_state.py
import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/etl_pipeline.py"
OUTPUT_PARQUET = "/home/user/output.parquet"
DATA_DIR = "/home/user/data"

def run_pipeline(input_file, output_file):
    """Helper to run the student's ETL pipeline script."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    result = subprocess.run(
        ["python3", SCRIPT_PATH, input_file, output_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Pipeline execution failed for {input_file}.\nSTDERR: {result.stderr}\nSTDOUT: {result.stdout}"

def get_parquet_data(file_path):
    """Helper to read Parquet data using pandas via a subprocess to avoid third-party imports in the test file."""
    assert os.path.isfile(file_path), f"Output file {file_path} was not created."
    code = f"""
import pandas as pd
import json
import sys
try:
    df = pd.read_parquet('{file_path}')
    # Convert timestamp to string if it's a datetime object
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(df.to_json(orient='records'))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to read parquet file {file_path}.\nSTDERR: {result.stderr}"

    data = json.loads(result.stdout)
    if isinstance(data, dict) and "error" in data:
        pytest.fail(f"Error reading parquet file: {data['error']}")
    return data

@pytest.fixture(scope="module")
def processed_data():
    """Run the pipeline on all batches and return the consolidated data."""
    # Ensure a clean state before running
    if os.path.exists(OUTPUT_PARQUET):
        os.remove(OUTPUT_PARQUET)

    batch1 = os.path.join(DATA_DIR, "batch1.jsonl")
    batch2 = os.path.join(DATA_DIR, "batch2.csv")
    batch3 = os.path.join(DATA_DIR, "batch3_retry.jsonl")

    run_pipeline(batch1, OUTPUT_PARQUET)
    run_pipeline(batch2, OUTPUT_PARQUET)
    run_pipeline(batch3, OUTPUT_PARQUET)

    records = get_parquet_data(OUTPUT_PARQUET)
    # Return records indexed by user_id for easier testing
    return {str(r.get("user_id")): r for r in records}

def test_pipeline_creates_output_file(processed_data):
    """Verify that the output parquet file is created."""
    assert os.path.isfile(OUTPUT_PARQUET), f"Output file {OUTPUT_PARQUET} is missing."

def test_deduplication_and_row_count(processed_data):
    """Verify that records are deduplicated by user_id."""
    assert len(processed_data) == 4, f"Expected exactly 4 unique users after deduplication, got {len(processed_data)}."
    expected_user_ids = {"1", "2", "3", "4"}
    assert set(processed_data.keys()) == expected_user_ids, f"Expected user IDs {expected_user_ids}, got {set(processed_data.keys())}."

def test_user1_masking(processed_data):
    """Verify masking for a standard email and phone number."""
    user = processed_data.get("1")
    assert user is not None, "User 1 is missing from the output."
    assert user.get("email") == "***@example.com", f"User 1 email not masked correctly. Got: {user.get('email')}"
    assert user.get("phone") == "123-456-XXXX", f"User 1 phone not masked correctly. Got: {user.get('phone')}"

def test_user2_update_and_masking(processed_data):
    """Verify that User 2 was updated with the latest timestamp and correctly masked."""
    user = processed_data.get("2")
    assert user is not None, "User 2 is missing from the output."
    assert user.get("name") == "Bob Updated", f"User 2 name not updated. Got: {user.get('name')}"
    assert user.get("email") == "***@test.com", f"User 2 email not masked correctly. Got: {user.get('email')}"
    assert user.get("phone") == "555-000-XXXX", f"User 2 phone not masked correctly. Got: {user.get('phone')}"
    assert user.get("timestamp") == "2023-10-01T10:15:00Z", f"User 2 timestamp not updated. Got: {user.get('timestamp')}"

def test_user3_csv_ingestion(processed_data):
    """Verify that data ingested from CSV is processed and masked correctly."""
    user = processed_data.get("3")
    assert user is not None, "User 3 is missing from the output."
    assert user.get("email") == "***@domain.org", f"User 3 email not masked correctly. Got: {user.get('email')}"
    assert user.get("phone") == "999-888-XXXX", f"User 3 phone not masked correctly. Got: {user.get('phone')}"

def test_user4_short_phone_masking(processed_data):
    """Verify masking for a phone number that is 4 characters or shorter."""
    user = processed_data.get("4")
    assert user is not None, "User 4 is missing from the output."
    assert user.get("email") == "***@company.net", f"User 4 email not masked correctly. Got: {user.get('email')}"
    assert user.get("phone") == "XXXX", f"User 4 short phone not masked correctly. Got: {user.get('phone')}"