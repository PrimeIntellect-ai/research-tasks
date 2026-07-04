# test_final_state.py
import os
import json
import csv
import pytest

RAW_DATA_DIR = '/home/user/raw_data'
OUTPUT_FILE = '/home/user/output/clean_data.jsonl'

def read_csv_robust(filepath):
    """Attempt to read a CSV file using multiple encodings."""
    encodings = ['utf-8', 'utf-16', 'iso-8859-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                text = f.read()
                # If reading succeeds and we find expected headers, return parsed rows
                if 'transaction_id' in text:
                    reader = csv.DictReader(text.splitlines())
                    return list(reader)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode or find headers in {filepath}")

def compute_expected_data():
    """Derive the expected output directly from the raw data files."""
    all_records = []
    for filename in os.listdir(RAW_DATA_DIR):
        if filename.endswith('.csv'):
            filepath = os.path.join(RAW_DATA_DIR, filename)
            all_records.extend(read_csv_robust(filepath))

    # Deduplicate by transaction_id, keeping the most recent timestamp
    deduped = {}
    for record in all_records:
        tid = record['transaction_id']
        if tid not in deduped:
            deduped[tid] = record
        else:
            # Compare timestamps string-wise (YYYY-MM-DD HH:MM:SS allows this)
            if record['timestamp'] > deduped[tid]['timestamp']:
                deduped[tid] = record

    # Masking
    for tid, record in deduped.items():
        # Mask email
        email = record['email']
        if '@' in email:
            domain = email.split('@', 1)[1]
            record['email'] = f"***@{domain}"

        # Mask SSN
        ssn = record['ssn']
        if len(ssn) >= 11 and ssn[3] == '-' and ssn[6] == '-':
            record['ssn'] = f"***-**-{ssn[-4:]}"

    # Sort by transaction_id
    sorted_records = sorted(deduped.values(), key=lambda x: x['transaction_id'])
    return sorted_records

def test_output_file_exists():
    """Ensure the output JSONL file exists."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

def test_output_format_and_content():
    """Verify the output file is valid JSONL and matches the expected derived data."""
    assert os.path.isfile(OUTPUT_FILE), "Cannot verify content: output file is missing."

    expected_data = compute_expected_data()

    actual_data = []
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                actual_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {line_num} in {OUTPUT_FILE} is not valid JSON: {e}")

    # Check sorting and counts
    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} records, but found {len(actual_data)} in output."

    actual_tids = [r.get('transaction_id') for r in actual_data]
    expected_tids = [r['transaction_id'] for r in expected_data]
    assert actual_tids == expected_tids, "Output is not correctly sorted by transaction_id or has incorrect IDs."

    # Check exact content
    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        for key in ['transaction_id', 'customer_name', 'email', 'ssn', 'amount', 'timestamp']:
            assert key in actual, f"Record {i} is missing key '{key}'"
            assert actual[key] == expected[key], \
                f"Mismatch in record {i} for key '{key}'. Expected '{expected[key]}', got '{actual[key]}'"