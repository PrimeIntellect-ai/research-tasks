# test_final_state.py
import os
import json
import csv
import subprocess
from datetime import datetime, timedelta
import pytest

def test_processed_jsonl():
    """
    Validates that the processed.jsonl file matches the expected output
    derived from transactions.csv, including the 60-second gap-filling rule
    and the correct subset of columns.
    """
    processed_path = "/app/processed.jsonl"
    assert os.path.exists(processed_path), f"Missing file: {processed_path}"

    csv_path = "/app/transactions.csv"
    assert os.path.exists(csv_path), f"Missing file: {csv_path}"

    expected_records = []
    last_timestamp = None

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tx_id = row.get("tx_id", "")
            amount = row.get("amount", "")
            description = row.get("description", "")

            ts_str = row.get("timestamp", "").strip()
            if not ts_str:
                if last_timestamp is None:
                    # If the very first row is missing a timestamp, we just leave it empty
                    # (though ideally the first row has one).
                    pass
                else:
                    last_timestamp += timedelta(seconds=60)
                    ts_str = last_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                try:
                    # Parse to handle the gap filling for subsequent missing timestamps
                    # The format specified is ISO8601 like 2023-01-01T10:00:00Z
                    last_timestamp = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    # Fallback if the timestamp format is slightly different but valid
                    pass

            expected_records.append({
                "tx_id": tx_id,
                "timestamp": ts_str,
                "amount": amount,
                "description": description
            })

    actual_records = []
    with open(processed_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON on line {line_num} in {processed_path}")

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} records, got {len(actual_records)}"

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, f"Record mismatch at line {i+1}. Expected {expected}, got {actual}"


def test_adversarial_filter():
    """
    Validates the suspicious_filter script against the clean and evil corpora.
    Clean corpus files should exit with 0.
    Evil corpus files should exit with 1.
    """
    filter_path = "/home/user/suspicious_filter"
    assert os.path.exists(filter_path), f"Missing executable: {filter_path}"
    assert os.access(filter_path, os.X_OK), f"File is not executable: {filter_path}"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.exists(clean_dir), f"Missing directory: {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([filter_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run([filter_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))