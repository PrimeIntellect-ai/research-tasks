# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/graph.db'
SCRIPT_PATH = '/home/user/extract_patterns.py'
OUTPUT_PATH = '/home/user/triangles.json'

def get_expected_triangles(db_path):
    """Dynamically compute the expected triangles from the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT a.src, b.src, c.src
        FROM entity_links a
        JOIN entity_links b ON a.dst = b.src
        JOIN entity_links c ON b.dst = c.src AND c.dst = a.src
        WHERE a.rel = 'friend' AND b.rel = 'friend' AND c.rel = 'friend'
    ''')
    triangles = set()
    for row in c.fetchall():
        triangles.add(tuple(sorted(row)))
    conn.close()

    # Convert to list of lists and sort lexicographically
    return sorted([list(t) for t in triangles])

def test_script_exists():
    """Check if the Python script was created."""
    assert os.path.exists(SCRIPT_PATH), f"Script file {SCRIPT_PATH} is missing."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."

def test_output_json_exists():
    """Check if the JSON output file was created."""
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."
    assert os.path.isfile(OUTPUT_PATH), f"Path {OUTPUT_PATH} is not a file."

def test_output_json_content():
    """Check if the JSON output contains the correct triangle patterns."""
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON.")

    expected_data = get_expected_triangles(DB_PATH)

    assert isinstance(data, list), "Outer JSON structure must be a list."
    for item in data:
        assert isinstance(item, list), "Inner elements must be lists."
        assert all(isinstance(x, int) for x in item), "Inner list elements must be integers."

    assert data == expected_data, f"JSON content does not match expected output. Expected {expected_data}, got {data}."