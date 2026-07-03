# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/warehouse.db"
C_FILE = "/home/user/etl_extract.c"
BIN_FILE = "/home/user/etl_extract"
OUT_FILE = "/home/user/output.json"

def get_expected_data(limit, offset):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = """
        SELECT a.id as article_id, a.title, au.name as author_name, a.views
        FROM articles a
        JOIN authors au ON a.author_id = au.id
        JOIN tags t ON a.id = t.article_id
        WHERE t.tag_name = 'AI' AND au.reputation > 100
        ORDER BY a.views DESC
        LIMIT ? OFFSET ?
    """
    cur.execute(query, (limit, offset))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def test_files_exist():
    assert os.path.isfile(C_FILE), f"Source file {C_FILE} is missing."
    assert os.path.isfile(BIN_FILE), f"Compiled binary {BIN_FILE} is missing."
    assert os.access(BIN_FILE, os.X_OK), f"{BIN_FILE} is not executable."

def test_execution_and_output():
    # Remove output file if it exists to ensure the binary creates it
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    # Run the binary with limit 3, offset 1
    try:
        result = subprocess.run(
            [BIN_FILE, "3", "1"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except Exception as e:
        pytest.fail(f"Failed to execute {BIN_FILE}: {e}")

    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert not result.stdout.strip(), "Program should not output anything to standard output."
    assert os.path.isfile(OUT_FILE), f"Output file {OUT_FILE} was not created by the program."

def test_json_contents():
    assert os.path.isfile(OUT_FILE), f"Output file {OUT_FILE} is missing."

    with open(OUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {OUT_FILE} as JSON: {e}")

    assert isinstance(data, list), "JSON root must be an array."

    expected_data = get_expected_data(3, 1)

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not an object."

        # Check keys and types
        assert "article_id" in actual, f"Missing 'article_id' in item {i}"
        assert isinstance(actual["article_id"], int), f"'article_id' in item {i} must be an integer"

        assert "title" in actual, f"Missing 'title' in item {i}"
        assert isinstance(actual["title"], str), f"'title' in item {i} must be a string"

        assert "author_name" in actual, f"Missing 'author_name' in item {i}"
        assert isinstance(actual["author_name"], str), f"'author_name' in item {i} must be a string"

        assert "views" in actual, f"Missing 'views' in item {i}"
        assert isinstance(actual["views"], int), f"'views' in item {i} must be an integer"

        # Check values
        assert actual["article_id"] == expected["article_id"], f"Incorrect article_id at index {i}"
        assert actual["title"] == expected["title"], f"Incorrect title at index {i}"
        assert actual["author_name"] == expected["author_name"], f"Incorrect author_name at index {i}"
        assert actual["views"] == expected["views"], f"Incorrect views at index {i}"