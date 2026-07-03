# test_final_state.py

import os
import json
import sqlite3
import pytest

RESULTS_PATH = '/home/user/optimized_results.json'
DB_PATH = '/home/user/company.db'
QUERIES_PATH = '/home/user/queries.sql'
SCHEMA_PATH = '/home/user/schema.json'

def test_results_file_exists_and_valid_json():
    assert os.path.isfile(RESULTS_PATH), f"Expected results file not found at {RESULTS_PATH}"

    with open(RESULTS_PATH, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON: {e}")

    assert isinstance(results, list), "JSON root must be an array"
    assert len(results) == 3, f"Expected exactly 3 query results, but got {len(results)}"

def test_results_schema_conformance():
    with open(RESULTS_PATH, 'r') as f:
        results = json.load(f)

    for i, res in enumerate(results):
        assert isinstance(res, dict), f"Item at index {i} is not a JSON object"

        expected_keys = {"query_id", "row_count", "execution_time_ms"}
        assert set(res.keys()) == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {set(res.keys())}"

        assert isinstance(res["query_id"], str), f"query_id must be a string in item {i}"
        assert res["query_id"] == f"query_{i+1}", f"Expected query_id 'query_{i+1}', got '{res['query_id']}'"

        assert isinstance(res["row_count"], int) and not isinstance(res["row_count"], bool), f"row_count must be an integer in item {i}"
        assert res["row_count"] >= 0, f"row_count must be >= 0 in item {i}"

        assert isinstance(res["execution_time_ms"], (int, float)) and not isinstance(res["execution_time_ms"], bool), f"execution_time_ms must be a number in item {i}"
        assert res["execution_time_ms"] >= 0, f"execution_time_ms must be >= 0 in item {i}"

def test_results_row_counts_match_db():
    assert os.path.isfile(DB_PATH), f"Database file missing: {DB_PATH}"
    assert os.path.isfile(QUERIES_PATH), f"Queries file missing: {QUERIES_PATH}"

    with open(RESULTS_PATH, 'r') as f:
        results = json.load(f)

    with open(QUERIES_PATH, 'r') as f:
        queries_content = f.read()

    queries = [q.strip() for q in queries_content.split(';') if q.strip()]
    assert len(queries) == 3, "Expected 3 queries in queries.sql"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for i, q in enumerate(queries):
        c.execute(q)
        actual_rows = len(c.fetchall())
        expected_rows = results[i]["row_count"]

        assert expected_rows == actual_rows, f"Row count mismatch for query_{i+1}. Expected {actual_rows} based on DB execution, got {expected_rows} in JSON"

    conn.close()

def test_indexes_created():
    assert os.path.isfile(DB_PATH), f"Database file missing: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = c.fetchall()

    conn.close()

    assert len(indexes) >= 2, f"Expected at least 2 custom indexes created for optimization, found {len(indexes)}: {indexes}"