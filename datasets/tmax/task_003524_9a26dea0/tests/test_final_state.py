# test_final_state.py

import os
import csv
import pytest

OUTPUT_FILE = '/home/user/output/clean_aggregates.csv'

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist. Did the ETL script run successfully?"

def test_output_headers():
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

    expected_headers = ['sensor_id', 'timestamp_utc', 'temp_rolling_avg']
    assert headers == expected_headers, f"Headers do not match. Expected {expected_headers}, got {headers}"

def test_output_row_count():
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        rows = list(reader)

    assert len(rows) == 11, f"Expected exactly 11 deduplicated records, but got {len(rows)}."

def test_output_sorting():
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        rows = list(reader)

    # Check if the rows are sorted by sensor_id, then timestamp_utc
    sorted_rows = sorted(rows, key=lambda x: (x[0], x[1]))
    assert rows == sorted_rows, "The output CSV is not sorted primarily by sensor_id and secondarily by timestamp_utc."

def test_output_values_and_formatting():
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Check specific values
    # Alpha 10:10:00 avg should be ~21.17
    alpha_10_10 = next((r for r in rows if r['sensor_id'] == 'alpha' and r['timestamp_utc'] == '2023-10-01 10:10:00'), None)
    assert alpha_10_10 is not None, "Missing alpha record for 2023-10-01 10:10:00"
    assert alpha_10_10['temp_rolling_avg'] == '21.17', f"Expected alpha rolling avg 21.17, got {alpha_10_10['temp_rolling_avg']}"

    # Beta 10:15:00 avg should be ~16.17
    beta_10_15 = next((r for r in rows if r['sensor_id'] == 'beta' and r['timestamp_utc'] == '2023-10-01 10:15:00'), None)
    assert beta_10_15 is not None, "Missing beta record for 2023-10-01 10:15:00"
    assert beta_10_15['temp_rolling_avg'] == '16.17', f"Expected beta rolling avg 16.17, got {beta_10_15['temp_rolling_avg']}"

    # Gamma 10:05:00 avg should be ~30.50
    gamma_10_05 = next((r for r in rows if r['sensor_id'] == 'gamma' and r['timestamp_utc'] == '2023-10-01 10:05:00'), None)
    assert gamma_10_05 is not None, "Missing gamma record for 2023-10-01 10:05:00"
    assert gamma_10_05['temp_rolling_avg'] in ('30.5', '30.50'), f"Expected gamma rolling avg 30.50, got {gamma_10_05['temp_rolling_avg']}"

    # Verify formatting of timestamps
    import re
    timestamp_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    for row in rows:
        assert timestamp_pattern.match(row['timestamp_utc']), f"Timestamp {row['timestamp_utc']} is not in %Y-%m-%d %H:%M:%S format."

        # Verify rounding to 2 decimal places
        avg_str = row['temp_rolling_avg']
        assert '.' in avg_str and len(avg_str.split('.')[1]) <= 2, f"Value {avg_str} is not rounded to 2 decimal places."