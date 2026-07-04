# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/dataset.db"
JSON_PATH = "/home/user/top_researchers.json"

def get_expected_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT 
        r.id AS researcher_id,
        r.full_name,
        COUNT(DISTINCT a.publication_id) AS total_publications,
        COALESCE(SUM(c.citations), 0) AS total_citations
    FROM researchers r
    JOIN authorship a ON r.id = a.researcher_id
    LEFT JOIN (
        SELECT target_pub_id, COUNT(*) as citations
        FROM references_tbl
        GROUP BY target_pub_id
    ) c ON a.publication_id = c.target_pub_id
    GROUP BY r.id, r.full_name
    ORDER BY total_citations DESC, r.full_name ASC
    LIMIT 5;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected = []
    for row in rows:
        expected.append({
            "researcher_id": row[0],
            "full_name": row[1],
            "total_publications": row[2],
            "total_citations": row[3]
        })
    return expected

def test_json_file_exists():
    assert os.path.isfile(JSON_PATH), f"The expected output file {JSON_PATH} does not exist."

def test_json_content_matches_expected():
    assert os.path.isfile(JSON_PATH), f"Cannot verify content because {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    assert isinstance(actual_data, list), f"Expected the JSON output to be a list, but got {type(actual_data).__name__}."

    expected_data = get_expected_results()

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Expected record at index {i} to be a dictionary."

        assert actual.get("researcher_id") == expected["researcher_id"], \
            f"Record {i} mismatch: expected researcher_id {expected['researcher_id']}, got {actual.get('researcher_id')}."

        assert actual.get("full_name") == expected["full_name"], \
            f"Record {i} mismatch: expected full_name '{expected['full_name']}', got '{actual.get('full_name')}'."

        assert actual.get("total_publications") == expected["total_publications"], \
            f"Record {i} mismatch for '{expected['full_name']}': expected total_publications {expected['total_publications']}, got {actual.get('total_publications')}."

        assert actual.get("total_citations") == expected["total_citations"], \
            f"Record {i} mismatch for '{expected['full_name']}': expected total_citations {expected['total_citations']}, got {actual.get('total_citations')}."