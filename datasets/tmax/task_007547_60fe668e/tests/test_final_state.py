# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_final_output_json():
    json_path = "/home/user/subgraph_ranked.json"
    assert os.path.exists(json_path), f"Output file not found at {json_path}"

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {json_path} is not valid JSON")

    assert isinstance(actual_data, list), "JSON output must be an array of objects"

    db_path = "/home/user/dataset.db"
    assert os.path.exists(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Compute the expected output directly from the database
    query = """
    WITH RECURSIVE
      subgraph(id) AS (
        SELECT 1
        UNION
        SELECT c.target_id
        FROM subgraph s
        JOIN citations c ON s.id = c.source_id
      ),
      citation_counts AS (
        SELECT p.id, COUNT(c.target_id) as total_citations
        FROM papers p
        LEFT JOIN citations c ON p.id = c.target_id
        GROUP BY p.id
      )
    SELECT 
      p.id, 
      p.title, 
      p.domain, 
      cc.total_citations,
      RANK() OVER (PARTITION BY p.domain ORDER BY cc.total_citations DESC, p.id ASC) as domain_rank
    FROM subgraph s
    JOIN papers p ON s.id = p.id
    JOIN citation_counts cc ON p.id = cc.id
    ORDER BY p.id ASC;
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = []
    for row in expected_rows:
        expected_data.append({
            "id": row["id"],
            "title": row["title"],
            "domain": row["domain"],
            "total_citations": row["total_citations"],
            "domain_rank": row["domain_rank"]
        })

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items in JSON array, got {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object"

        for key in ["id", "title", "domain", "total_citations", "domain_rank"]:
            assert key in actual, f"Missing key '{key}' in item at index {i}"
            assert actual[key] == expected[key], f"Mismatch in '{key}' for item at index {i}. Expected {expected[key]}, got {actual[key]}"