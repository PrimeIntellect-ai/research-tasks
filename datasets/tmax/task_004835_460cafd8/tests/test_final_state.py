# test_final_state.py

import os
import csv
import subprocess
import pytest

CSV_PATH = "/home/user/config_ts.csv"

def test_csv_exists_and_content():
    """Verify that the CSV file is generated and contains the correct parsed data."""
    assert os.path.isfile(CSV_PATH), f"CSV file {CSV_PATH} was not created."

    expected_rows = [
        ['timestamp', 'normalized_key', 'value'],
        ['2023-10-01T12:00:00Z', 'network_setup', 'Interface eth0 up'],
        ['2023-10-01T12:05:00Z', 'database_connection', 'Retrying\ntimeout'],
        ['2023-10-01T12:10:00Z', 'firewall_rule', 'Block port 80'],
        ['2023-10-01T12:15:00Z', 'cache_servers', 'flushed\nall\nnodes']
    ]

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    assert len(reader) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, but found {len(reader)}."

    for i, (actual, expected) in enumerate(zip(reader, expected_rows)):
        assert actual == expected, f"Row {i+1} in CSV does not match expected.\nExpected: {expected}\nActual: {actual}"

def test_crontab_configured():
    """Verify that the crontab is configured to run the script every 15 minutes."""
    try:
        cron_out = subprocess.check_output(['crontab', '-l'], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure a crontab is set for the user.")

    lines = cron_out.strip().split('\n')
    found_cron = False
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        # Check if the line runs every 15 minutes
        parts = line.split()
        if len(parts) >= 6:
            minute_field = parts[0]
            is_15_mins = (minute_field == '*/15' or minute_field == '0,15,30,45')
            if is_15_mins and 'extract_ts.py' in line:
                found_cron = True
                break

    assert found_cron, "Could not find a crontab entry running extract_ts.py every 15 minutes (e.g., '*/15 * * * *')."