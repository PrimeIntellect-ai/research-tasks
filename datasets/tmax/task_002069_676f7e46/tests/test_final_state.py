# test_final_state.py

import os
import csv
import pytest

OUTPUT_FILE = "/home/user/output_data/processed_combined.csv"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."

def test_output_headers():
    with open(OUTPUT_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

    expected_headers = ['site_id', 'timestamp', 'sensor_name', 'reading', 'rolling_avg', 'notes']
    assert headers == expected_headers, f"Headers are incorrect. Expected {expected_headers}, got {headers}."

def test_rolling_averages_and_data():
    with open(OUTPUT_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output CSV is empty."

    # Find site_1, sensor_alpha, 10:15:00Z
    alpha_row = next((r for r in rows if r['site_id'] == 'site_1' and r['sensor_name'] == 'sensor_alpha' and r['timestamp'] == '2023-01-01T10:15:00Z'), None)
    assert alpha_row is not None, "Missing record for site_1, sensor_alpha at 2023-01-01T10:15:00Z"
    assert float(alpha_row['reading']) == 16.0, f"Expected reading 16.0, got {alpha_row['reading']}"
    assert float(alpha_row['rolling_avg']) == 14.0, f"Expected rolling_avg 14.0, got {alpha_row['rolling_avg']}"

    # Find site_1, sensor_beta, 10:10:00Z
    beta_row = next((r for r in rows if r['site_id'] == 'site_1' and r['sensor_name'] == 'sensor_beta' and r['timestamp'] == '2023-01-01T10:10:00Z'), None)
    assert beta_row is not None, "Missing record for site_1, sensor_beta at 2023-01-01T10:10:00Z"
    assert float(beta_row['reading']) == 22.0, f"Expected reading 22.0, got {beta_row['reading']}"
    assert float(beta_row['rolling_avg']) == 21.0, f"Expected rolling_avg 21.0, got {beta_row['rolling_avg']}"

def test_multiline_notes_preserved():
    with open(OUTPUT_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    multiline_row = next((r for r in rows if r['site_id'] == 'site_1' and r['timestamp'] == '2023-01-01T10:00:00Z'), None)
    assert multiline_row is not None, "Missing record for site_1 at 2023-01-01T10:00:00Z"

    assert "\n" in multiline_row['notes'], "Multiline note did not preserve embedded newlines."