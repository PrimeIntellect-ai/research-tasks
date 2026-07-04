# test_final_state.py

import os
import json
import sqlite3
import pytest

def get_expected_summary():
    """
    Dynamically compute the expected summary by reading the database
    and the raw logs, applying the correct join and error handling.
    """
    db_path = "/home/user/log_pipeline/data/metadata.db"
    log_path = "/home/user/log_pipeline/data/raw_logs.jsonl"

    # Recompute the correct mapping
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT servers.ip, regions.name 
        FROM servers 
        JOIN regions ON servers.region_id = regions.id
    """)
    mapping = {row[0]: row[1] for row in c.fetchall()}
    conn.close()

    # Recompute the error counts, skipping invalid JSON
    counts = {}
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("level") == "ERROR":
                    ip = record.get("ip")
                    region = mapping.get(ip, "unknown")
                    counts[region] = counts.get(region, 0) + 1
            except ValueError:
                # Skip corrupted lines
                continue

    return counts

def test_venv_setup():
    """Test that the virtual environment was created and python executable exists."""
    python_path = "/home/user/log_pipeline/venv/bin/python"
    assert os.path.isfile(python_path), (
        f"Virtual environment python executable not found at {python_path}. "
        "Ensure the virtual environment was created in the correct location."
    )

def test_summary_json_exists_and_correct():
    """Test that the output summary.json exists and contains the correct aggregated data."""
    out_path = "/home/user/log_pipeline/output/summary.json"

    assert os.path.isfile(out_path), (
        f"Output file {out_path} is missing. "
        "The pipeline script may have failed or not been run."
    )

    with open(out_path, 'r', encoding='utf-8') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {out_path} does not contain valid JSON.")

    expected_summary = get_expected_summary()

    assert actual_summary == expected_summary, (
        f"The data in {out_path} is incorrect.\n"
        f"Expected: {expected_summary}\n"
        f"Actual: {actual_summary}\n"
        "Check that the SQL query is correctly joining on region_id and "
        "that invalid JSON lines are gracefully skipped."
    )