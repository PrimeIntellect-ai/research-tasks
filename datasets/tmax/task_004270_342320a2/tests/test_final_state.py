# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/activity.db'
ETL_SCRIPT_PATH = '/home/user/etl_graph.py'
GRAPH_JSON_PATH = '/home/user/graph_materialized.json'
TOP_INFLUENCER_PATH = '/home/user/top_influencer.txt'

@pytest.fixture(scope="module")
def db_data():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Compute expected nodes
    c.execute("SELECT user_id, name FROM users ORDER BY user_id")
    nodes = [{"id": row["user_id"], "name": row["name"]} for row in c.fetchall()]

    # Compute expected edges
    query = """
        SELECT c.commenter_id AS source, p.author_id AS target, COUNT(*) AS weight
        FROM comments c
        JOIN posts p ON c.post_id = p.post_id
        WHERE c.commenter_id != p.author_id
        GROUP BY c.commenter_id, p.author_id
    """
    c.execute(query)
    edges = [{"source": row["source"], "target": row["target"], "weight": row["weight"]} for row in c.fetchall()]

    # Compute top influencer
    influencer_query = """
        SELECT p.author_id, COUNT(*) AS total_weight
        FROM comments c
        JOIN posts p ON c.post_id = p.post_id
        WHERE c.commenter_id != p.author_id
        GROUP BY p.author_id
        ORDER BY total_weight DESC, p.author_id ASC
        LIMIT 1
    """
    c.execute(influencer_query)
    top_influencer_row = c.fetchone()
    top_influencer = str(top_influencer_row["author_id"]) if top_influencer_row else None

    conn.close()
    return {"nodes": nodes, "edges": edges, "top_influencer": top_influencer}

def test_etl_script_exists():
    assert os.path.exists(ETL_SCRIPT_PATH), f"ETL script {ETL_SCRIPT_PATH} is missing."
    assert os.path.isfile(ETL_SCRIPT_PATH), f"{ETL_SCRIPT_PATH} is not a file."

def test_indexes_created():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = c.fetchall()
    conn.close()

    assert len(indexes) > 0, "No new indexes were created in the database."
    indexed_tables = {row[1] for row in indexes}
    assert "comments" in indexed_tables or "posts" in indexed_tables, \
        "Expected indexes on 'comments' or 'posts' tables to optimize the query."

def test_graph_materialized(db_data):
    assert os.path.exists(GRAPH_JSON_PATH), f"Output JSON file {GRAPH_JSON_PATH} is missing."

    with open(GRAPH_JSON_PATH, 'r') as f:
        try:
            graph = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {GRAPH_JSON_PATH} is not valid JSON.")

    assert "nodes" in graph, f"Key 'nodes' missing in {GRAPH_JSON_PATH}"
    assert "edges" in graph, f"Key 'edges' missing in {GRAPH_JSON_PATH}"

    # Sort nodes and edges for comparison
    expected_nodes = sorted(db_data["nodes"], key=lambda x: x["id"])
    actual_nodes = sorted(graph["nodes"], key=lambda x: x.get("id", -1))
    assert actual_nodes == expected_nodes, "The 'nodes' array does not match the expected state."

    expected_edges = sorted(db_data["edges"], key=lambda x: (x["source"], x["target"]))
    actual_edges = sorted(graph["edges"], key=lambda x: (x.get("source", -1), x.get("target", -1)))
    assert actual_edges == expected_edges, "The 'edges' array does not match the expected state (weights or connections are incorrect)."

def test_top_influencer(db_data):
    assert os.path.exists(TOP_INFLUENCER_PATH), f"File {TOP_INFLUENCER_PATH} is missing."

    with open(TOP_INFLUENCER_PATH, 'r') as f:
        content = f.read().strip()

    assert content == db_data["top_influencer"], \
        f"Expected top influencer ID '{db_data['top_influencer']}', but found '{content}' in {TOP_INFLUENCER_PATH}."