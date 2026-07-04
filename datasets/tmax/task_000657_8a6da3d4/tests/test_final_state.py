# test_final_state.py

import os
import json
import sqlite3
import pytest

APP_DIR = "/home/user/app"
INPUTS_TXT = os.path.join(APP_DIR, "inputs.txt")
RECOVERED_DB = os.path.join(APP_DIR, "recovered.db")
SUMMARY_JSON = "/home/user/summary.json"

def test_fast_parser_compiled():
    """Check if the fast_parser C extension has been compiled (.so file exists)."""
    so_files = []
    for root, dirs, files in os.walk(APP_DIR):
        for file in files:
            if file.endswith(".so"):
                so_files.append(os.path.join(root, file))

    assert len(so_files) > 0, "Could not find any compiled .so extension in /home/user/app/ or its subdirectories."

def test_recovered_db_valid():
    """Check if the recovered database exists and is valid."""
    assert os.path.isfile(RECOVERED_DB), f"Recovered database {RECOVERED_DB} is missing."

    conn = sqlite3.connect(RECOVERED_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM events;")
        count = cursor.fetchone()[0]
        assert isinstance(count, int), "Could not retrieve the count of records from the 'events' table."
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Recovered database is corrupted or invalid: {e}")
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query the 'events' table in the recovered database: {e}")
    finally:
        conn.close()

def test_summary_json():
    """Check if the summary JSON file is correct based on the inputs and recovered database."""
    assert os.path.isfile(SUMMARY_JSON), f"Summary file {SUMMARY_JSON} is missing."

    # Derive the expected crashing input from inputs.txt
    assert os.path.isfile(INPUTS_TXT), f"Original inputs file {INPUTS_TXT} is missing."
    with open(INPUTS_TXT, "r") as f:
        lines = f.read().splitlines()

    expected_crashing_input = None
    for line in lines:
        if len(line) > 100:
            expected_crashing_input = line
            break

    assert expected_crashing_input is not None, "Could not find a line longer than 100 characters in inputs.txt."

    # Derive the expected recovered records from the recovered database
    assert os.path.isfile(RECOVERED_DB), f"Recovered database {RECOVERED_DB} is missing."
    conn = sqlite3.connect(RECOVERED_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM events;")
        expected_recovered_records = cursor.fetchone()[0]
    except Exception as e:
        pytest.fail(f"Could not read records from recovered database to verify summary: {e}")
    finally:
        conn.close()

    # Read and validate the summary JSON
    with open(SUMMARY_JSON, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Summary file {SUMMARY_JSON} is not valid JSON: {e}")

    assert "crashing_input" in summary, "Summary JSON is missing the 'crashing_input' key."
    assert "recovered_records" in summary, "Summary JSON is missing the 'recovered_records' key."

    assert summary["crashing_input"] == expected_crashing_input, \
        f"Incorrect crashing_input in summary. Expected '{expected_crashing_input}', got '{summary['crashing_input']}'."

    assert summary["recovered_records"] == expected_recovered_records, \
        f"Incorrect recovered_records in summary. Expected {expected_recovered_records}, got {summary['recovered_records']}."