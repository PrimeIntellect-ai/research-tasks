# test_final_state.py

import os
import sqlite3
import json
import pytest
import requests

def test_database_indexes():
    db_path = "/home/user/research_data.db"
    assert os.path.isfile(db_path), f"Database file {db_path} missing."
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all indexes
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()

    # We expect some indexes on interviews and interview_tags to optimize the query.
    indexed_tables = [idx[1] for idx in indexes]
    assert "interviews" in indexed_tables, "No index created on interviews table."
    assert "interview_tags" in indexed_tables, "No index created on interview_tags table."
    conn.close()

def test_export_summary_script_and_json():
    script_path = "/home/user/export_summary.sh"
    json_path = "/home/user/amazonas_summary.json"

    assert os.path.isfile(script_path), f"Script {script_path} missing."
    assert os.path.isfile(json_path), f"JSON file {json_path} missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert isinstance(data, list), "JSON should be a list of objects."

    # Compute expected
    db_path = "/home/user/research_data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.tag_name, SUM(i.duration_seconds)
        FROM interviews i
        JOIN interview_tags it ON i.id = it.interview_id
        JOIN tags t ON it.tag_id = t.id
        WHERE i.location = 'Amazonas'
        GROUP BY t.tag_name
    """)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = {row[0]: row[1] for row in expected_rows}
    actual_data = {item.get("tag"): item.get("total_duration") for item in data if "tag" in item}

    assert actual_data == expected_data, f"Expected summary {expected_data}, got {actual_data}"

def test_transcript_content():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.isfile(transcript_path), f"Transcript file {transcript_path} missing."

    with open(transcript_path, 'r') as f:
        content = f.read().lower()

    keywords = ["canopy density", "region", "survey"]
    for kw in keywords:
        assert kw in content, f"Expected keyword '{kw}' not found in transcript."

def test_http_server_summary():
    try:
        resp = requests.get("http://127.0.0.1:8080/summary", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on /summary: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    assert "application/json" in resp.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    json_path = "/home/user/amazonas_summary.json"
    with open(json_path, 'r') as f:
        expected_json = json.load(f)

    try:
        actual_json = resp.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON.")

    assert actual_json == expected_json, "HTTP response JSON does not match file."

def test_http_server_transcript():
    try:
        resp = requests.get("http://127.0.0.1:8080/transcript", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on /transcript: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    assert "text/plain" in resp.headers.get("Content-Type", ""), "Expected Content-Type: text/plain"

    transcript_path = "/home/user/transcript.txt"
    with open(transcript_path, 'r') as f:
        expected_text = f.read()

    assert resp.text.strip() == expected_text.strip(), "HTTP response text does not match transcript file."