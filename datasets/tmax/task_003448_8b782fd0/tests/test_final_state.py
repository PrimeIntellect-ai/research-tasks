# test_final_state.py
import os
import json
import subprocess

def test_report_json_content():
    report_path = '/home/user/output/report.json'
    assert os.path.exists(report_path), f"The file {report_path} does not exist."

    with open(report_path, 'r', encoding='utf-8') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} is not valid JSON."

    assert "total_records_read" in report, "Missing 'total_records_read' in report.json"
    assert report["total_records_read"] == 10, f"Expected 10 total_records_read, got {report['total_records_read']}"

    assert "total_duplicates_removed" in report, "Missing 'total_duplicates_removed' in report.json"
    assert report["total_duplicates_removed"] == 6, f"Expected 6 total_duplicates_removed, got {report['total_duplicates_removed']}"

    assert "user_with_most_duplicates" in report, "Missing 'user_with_most_duplicates' in report.json"
    assert report["user_with_most_duplicates"] == 3, f"Expected user 3 to have most duplicates, got {report['user_with_most_duplicates']}"

def test_parquet_file_exists_and_content():
    parquet_path = '/home/user/output/clean_data.parquet'
    assert os.path.exists(parquet_path), f"The file {parquet_path} does not exist."
    assert os.path.getsize(parquet_path) > 0, f"The file {parquet_path} is empty."

    # Use a subprocess to read the Parquet file using pandas or pyarrow if available,
    # to avoid importing third-party libraries directly in the test file.
    script = f"""
import json
import sys

try:
    import pandas as pd
    df = pd.read_parquet('{parquet_path}')
    records = df.to_dict(orient='records')
    print(json.dumps(records))
except ImportError:
    try:
        import pyarrow.parquet as pq
        table = pq.read_table('{parquet_path}')
        records = table.to_pylist()
        print(json.dumps(records))
    except ImportError:
        print("NO_PARQUET_READER", file=sys.stderr)
        sys.exit(0)
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True)

    if "NO_PARQUET_READER" in result.stderr:
        # If the environment lacks pandas/pyarrow during testing, we fallback to just checking file existence
        pass
    else:
        assert result.returncode == 0, f"Error reading parquet file in subprocess: {result.stderr}"
        try:
            records = json.loads(result.stdout)
        except json.JSONDecodeError:
            assert False, f"Failed to parse subprocess output as JSON: {result.stdout}"

        assert len(records) == 4, f"Expected exactly 4 deduplicated records in Parquet, found {len(records)}."

        # Map user_id to timestamp to verify that the earliest timestamps were kept
        user_timestamps = {int(r['user_id']): int(r['timestamp']) for r in records}

        expected_timestamps = {
            1: 1600000000,
            2: 1600000005,
            3: 1600000000,
            4: 1600000000
        }

        for uid, expected_ts in expected_timestamps.items():
            assert uid in user_timestamps, f"User {uid} is missing from the Parquet file."
            assert user_timestamps[uid] == expected_ts, f"Expected timestamp {expected_ts} for user {uid}, got {user_timestamps[uid]}."