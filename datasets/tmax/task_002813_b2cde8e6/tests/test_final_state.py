# test_final_state.py

import os
import json
import glob
import pytest

OUTPUT_FILE = "/home/user/cleaned_logs.jsonl"
LOGS_DIR = "/home/user/logs"

def get_expected_records():
    """
    Derives the expected output by reading the original log files,
    handling encoding errors, deduplicating, and sorting.
    """
    log_files = glob.glob(os.path.join(LOGS_DIR, "etl_retry_*.log"))
    assert log_files, "Original log files are missing; cannot compute expected state."

    records_by_event = {}

    for filepath in log_files:
        with open(filepath, 'rb') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Decode replacing invalid bytes with \ufffd
                decoded_line = line.decode('utf-8', errors='replace')
                record = json.loads(decoded_line)

                event_id = record['event_id']
                retry_count = record['retry_count']

                if event_id not in records_by_event:
                    records_by_event[event_id] = record
                else:
                    if retry_count > records_by_event[event_id]['retry_count']:
                        records_by_event[event_id] = record

    # Sort by timestamp, then by event_id
    expected_records = sorted(
        records_by_event.values(),
        key=lambda r: (r['timestamp'], r['event_id'])
    )

    return expected_records

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

def test_output_content_and_deduplication():
    assert os.path.exists(OUTPUT_FILE), "Output file missing."

    expected_records = get_expected_records()

    actual_records = []
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_records.append(json.loads(line))
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in output file: {e}")

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records after deduplication, "
        f"but got {len(actual_records)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, (
            f"Record at index {i} does not match expected.\n"
            f"Actual: {actual}\nExpected: {expected}"
        )

def test_output_keys_are_sorted():
    assert os.path.exists(OUTPUT_FILE), "Output file missing."

    def verify_key_order(pairs):
        keys = [k for k, v in pairs]
        assert keys == sorted(keys), f"JSON keys are not sorted alphabetically: {keys}"
        return dict(pairs)

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            json.loads(line, object_pairs_hook=verify_key_order)