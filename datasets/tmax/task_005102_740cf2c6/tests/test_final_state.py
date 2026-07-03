# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/backups.db"
REPORT_PATH = "/home/user/lineage_report.json"

def test_index_exists():
    assert os.path.isfile(DB_PATH), f"Database file missing: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_jobs_parent';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Index 'idx_jobs_parent' does not exist in the database."
    assert result[0] == 'idx_jobs_parent', "Index name mismatch."

def test_json_report_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"JSON report missing: {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file lineage_report.json does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output should be a list of dictionaries."
    assert len(data) == 5, f"Should contain exactly 5 jobs in the lineage, found {len(data)}."

    expected_cumulative = {
        'BKP-001': 1000,
        'BKP-002': 1500,
        'BKP-003': 2250,
        'BKP-004': 2450,
        'BKP-005': 2550
    }

    found_ids = set()
    for row in data:
        assert isinstance(row, dict), "Each item in the JSON array must be an object/dictionary."
        assert 'id' in row, "Missing 'id' in row."
        assert 'cumulative_size_bytes' in row, f"Missing 'cumulative_size_bytes' in row for id {row['id']}."

        job_id = row['id']
        found_ids.add(job_id)

        assert job_id in expected_cumulative, f"Unexpected job id {job_id} found in the report."
        assert row['cumulative_size_bytes'] == expected_cumulative[job_id], \
            f"Incorrect cumulative_size_bytes for {job_id}. Expected {expected_cumulative[job_id]}, got {row['cumulative_size_bytes']}."

    assert found_ids == set(expected_cumulative.keys()), "Not all expected jobs were found in the report."