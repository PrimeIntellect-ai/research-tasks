# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/research.db"
OUTPUT_JSON_PATH = "/home/user/path_results.json"
CARGO_PROJECT_PATH = "/home/user/citation_processor"

def test_cargo_project_exists():
    """Test that the Cargo project was created at the specified location."""
    assert os.path.isdir(CARGO_PROJECT_PATH), f"Cargo project directory not found at {CARGO_PROJECT_PATH}"
    cargo_toml = os.path.join(CARGO_PROJECT_PATH, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {CARGO_PROJECT_PATH}"

def test_output_json_exists_and_correct():
    """Test that the output JSON file exists and contains the correct data."""
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Output JSON not found at {OUTPUT_JSON_PATH}"

    with open(OUTPUT_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} does not contain valid JSON.")

    expected = [
        {"id": 1, "title": "Origin Paper", "year": 2020, "score": 10.5, "year_rank": 3},
        {"id": 4, "title": "Shortcut Paper", "year": 2021, "score": 9.5, "year_rank": 1},
        {"id": 5, "title": "Target Paper", "year": 2022, "score": 15.0, "year_rank": 1}
    ]

    assert data == expected, f"JSON output does not match expected. Got: {data}"

def test_database_unaltered():
    """Test that the original database was not modified."""
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check papers table
    cursor.execute("SELECT id, title, year, score FROM papers ORDER BY id;")
    papers_rows = cursor.fetchall()
    expected_papers = [
        (1, 'Origin Paper', 2020, 10.5),
        (2, 'Second Paper', 2020, 12.0),
        (3, 'Third Paper', 2021, 8.0),
        (4, 'Shortcut Paper', 2021, 9.5),
        (5, 'Target Paper', 2022, 15.0),
        (6, 'Noise Paper', 2020, 15.0)
    ]
    assert papers_rows == expected_papers, "The 'papers' table was modified."

    # Check citations table
    cursor.execute("SELECT source_id, target_id FROM citations ORDER BY source_id, target_id;")
    citations_rows = cursor.fetchall()
    expected_citations = [
        (1, 2),
        (1, 4),
        (2, 3),
        (3, 5),
        (4, 5)
    ]
    assert citations_rows == expected_citations, "The 'citations' table was modified."

    conn.close()