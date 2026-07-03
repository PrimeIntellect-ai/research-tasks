# test_final_state.py

import os
import re
import sqlite3
import pytest

BASE_DIR = "/home/user/ticket4092"
LOG_FILE = os.path.join(BASE_DIR, "service.log")
DB_FILE = os.path.join(BASE_DIR, "market_data.db")
RESOLUTION_FILE = os.path.join(BASE_DIR, "resolution.txt")

def test_resolution_report_exists_and_correct():
    assert os.path.isfile(RESOLUTION_FILE), f"Resolution report {RESOLUTION_FILE} is missing."

    # Extract the requested timestamps from the service log as the source of truth
    # (The log contains the exact URL requested, which matches the pcap)
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} is missing."
    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    match = re.search(r'GET /vwap\?start=([^&]+)&end=([^\s]+)', log_content)
    assert match is not None, "Could not find the original GET request in service.log to determine truth."

    expected_start = match.group(1)
    expected_end = match.group(2)

    # Calculate the mathematically correct VWAP directly from the database
    assert os.path.isfile(DB_FILE), f"Database file {DB_FILE} is missing."
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT price, volume FROM trades WHERE timestamp >= ? AND timestamp <= ?", 
        (expected_start, expected_end)
    )
    rows = cursor.fetchall()
    conn.close()

    total_value = sum(price * volume for price, volume in rows)
    total_volume = sum(volume for price, volume in rows)

    assert total_volume > 0, "No data found for the expected time range in the database."
    expected_vwap = round(total_value / total_volume, 4)

    # Parse the student's resolution report
    with open(RESOLUTION_FILE, "r") as f:
        res_content = f.read()

    start_match = re.search(r'Requested Start:\s*(.+)', res_content)
    end_match = re.search(r'Requested End:\s*(.+)', res_content)
    vwap_match = re.search(r'Correct VWAP:\s*(.+)', res_content)

    assert start_match is not None, "Format error: 'Requested Start: <value>' not found in resolution.txt."
    assert end_match is not None, "Format error: 'Requested End: <value>' not found in resolution.txt."
    assert vwap_match is not None, "Format error: 'Correct VWAP: <value>' not found in resolution.txt."

    actual_start = start_match.group(1).strip()
    actual_end = end_match.group(1).strip()

    try:
        actual_vwap = float(vwap_match.group(1).strip())
    except ValueError:
        pytest.fail("Format error: VWAP value in resolution.txt is not a valid float.")

    assert actual_start == expected_start, f"Requested Start is incorrect. Expected {expected_start}, got {actual_start}."
    assert actual_end == expected_end, f"Requested End is incorrect. Expected {expected_end}, got {actual_end}."
    assert actual_vwap == expected_vwap, f"Correct VWAP is incorrect. Expected {expected_vwap}, got {actual_vwap}."