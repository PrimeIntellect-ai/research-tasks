# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/research_data.db"
JSON_PATH = "/home/user/metrics_output.json"
CYPHER_PATH = "/home/user/graph_setup.cypher"

def compute_expected_metrics():
    """Computes the expected metrics directly from the SQLite database."""
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    WITH AuthorCitations AS (
        SELECT 
            a.id AS author_id, 
            a.name AS author_name, 
            i.name AS institution_name, 
            COUNT(c.cited_paper_id) AS total_citations
        FROM authors a
        JOIN institutions i ON a.institution_id = i.id
        LEFT JOIN authorships ash ON a.id = ash.author_id
        LEFT JOIN citations c ON ash.paper_id = c.cited_paper_id
        GROUP BY a.id, a.name, i.name
    )
    SELECT 
        author_id, 
        author_name, 
        institution_name, 
        total_citations,
        RANK() OVER (PARTITION BY institution_name ORDER BY total_citations DESC) AS institution_rank
    FROM AuthorCitations
    ORDER BY total_citations DESC, author_id ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected_json = []
    for row in rows:
        expected_json.append({
            "author_id": row[0],
            "author_name": row[1],
            "institution_name": row[2],
            "total_citations": row[3],
            "institution_rank": row[4]
        })

    return expected_json

def test_json_output_correctness():
    assert os.path.exists(JSON_PATH), f"JSON output file missing at {JSON_PATH}"

    with open(JSON_PATH, "r") as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    expected_json = compute_expected_metrics()

    assert isinstance(actual_json, list), "JSON output must be a list of objects."
    assert len(actual_json) == len(expected_json), f"Expected {len(expected_json)} authors in JSON, found {len(actual_json)}."

    for i, (actual, expected) in enumerate(zip(actual_json, expected_json)):
        assert actual.get("author_id") == expected["author_id"], f"Mismatch at index {i}: expected author_id {expected['author_id']}, got {actual.get('author_id')}"
        assert actual.get("author_name") == expected["author_name"], f"Mismatch at index {i}: expected author_name {expected['author_name']}, got {actual.get('author_name')}"
        assert actual.get("institution_name") == expected["institution_name"], f"Mismatch at index {i}: expected institution_name {expected['institution_name']}, got {actual.get('institution_name')}"
        assert actual.get("total_citations") == expected["total_citations"], f"Mismatch at index {i}: expected total_citations {expected['total_citations']}, got {actual.get('total_citations')}"
        assert actual.get("institution_rank") == expected["institution_rank"], f"Mismatch at index {i}: expected institution_rank {expected['institution_rank']}, got {actual.get('institution_rank')}"

def test_cypher_output_correctness():
    assert os.path.exists(CYPHER_PATH), f"Cypher output file missing at {CYPHER_PATH}"

    expected_metrics = compute_expected_metrics()
    top_authors = [m for m in expected_metrics if m["institution_rank"] == 1]

    with open(CYPHER_PATH, "r") as f:
        cypher_content = f.read()

    # Check that each top author and their institution is mentioned in the Cypher script
    for author in top_authors:
        assert author["author_name"] in cypher_content, f"Missing author {author['author_name']} in Cypher script."
        assert author["institution_name"] in cypher_content, f"Missing institution {author['institution_name']} in Cypher script."
        assert str(author["total_citations"]) in cypher_content, f"Missing total_citations {author['total_citations']} for {author['author_name']} in Cypher script."

    # Ensure no rank > 1 authors are in the script
    non_top_authors = [m for m in expected_metrics if m["institution_rank"] > 1]
    for author in non_top_authors:
        assert author["author_name"] not in cypher_content, f"Author {author['author_name']} has rank {author['institution_rank']} but was found in Cypher script."

    # Basic structural checks for CREATE and MERGE
    assert "MERGE " in cypher_content.upper() or "CREATE " in cypher_content.upper(), "Cypher script lacks MERGE or CREATE statements."
    assert "WORKS_AT" in cypher_content, "Cypher script lacks WORKS_AT relationship."