# test_final_state.py

import os
import json
import csv
import sqlite3
import pytest

def test_author_stats_csv():
    csv_path = "/home/user/output/author_stats.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist"

    with open(csv_path, 'r', newline='') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "CSV is empty"

    headers = reader[0]
    expected_headers = ["name", "year", "yearly_papers", "cumulative_papers"]
    assert headers == expected_headers, f"CSV headers {headers} do not match expected {expected_headers}"

    # Compute expected data from SQLite
    db_path = "/home/user/data/research.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.name, p.year, COUNT(p.paper_id) as yearly_papers
        FROM Authors a
        JOIN Author_Paper ap ON a.author_id = ap.author_id
        JOIN Papers p ON ap.paper_id = p.paper_id
        GROUP BY a.name, p.year
        ORDER BY a.name, p.year
    """)
    rows = cursor.fetchall()

    expected_data = []
    cumulative = {}
    for name, year, yearly in rows:
        cumulative[name] = cumulative.get(name, 0) + yearly
        expected_data.append([name, str(year), str(yearly), str(cumulative[name])])

    actual_data = reader[1:]

    # We can sort both to be order-agnostic, though cumulative sum implies order by year
    assert sorted(actual_data) == sorted(expected_data), f"CSV data {actual_data} does not match expected {expected_data}"

def test_tag_aggregation_json():
    json_path = "/home/user/output/tag_aggregation.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("tag_aggregation.json is not valid JSON")

    assert isinstance(data, list), "tag_aggregation.json should be a JSON array"

    # Compute expected aggregation
    jsonl_path = "/home/user/data/metadata.jsonl"
    tag_counts = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            doc = json.loads(line)
            for tag in doc.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    expected_list = [{"tag": k, "count": v} for k, v in tag_counts.items()]
    expected_list.sort(key=lambda x: (-x["count"], x["tag"]))

    assert data == expected_list, f"tag_aggregation.json data {data} does not match expected {expected_list}"

def test_graph_json():
    graph_path = "/home/user/output/graph.json"
    assert os.path.isfile(graph_path), f"File {graph_path} does not exist"

    with open(graph_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("graph.json is not valid JSON")

    assert "nodes" in data, "graph.json missing 'nodes'"
    assert "edges" in data, "graph.json missing 'edges'"

    db_path = "/home/user/data/research.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT author_id, name FROM Authors")
    authors = cursor.fetchall()

    cursor.execute("SELECT paper_id, title FROM Papers")
    papers = cursor.fetchall()

    cursor.execute("SELECT author_id, paper_id FROM Author_Paper")
    author_paper = cursor.fetchall()
    conn.close()

    expected_nodes = []
    for aid, name in authors:
        expected_nodes.append({"id": f"A_{aid}", "type": "Author", "label": name})
    for pid, title in papers:
        expected_nodes.append({"id": f"P_{pid}", "type": "Paper", "label": title})

    expected_edges = []
    for aid, pid in author_paper:
        expected_edges.append({"source": f"A_{aid}", "target": f"P_{pid}", "relation": "AUTHORED"})

    # Sort for comparison
    def sort_node(n): return n["id"]
    def sort_edge(e): return (e["source"], e["target"], e["relation"])

    actual_nodes = sorted(data["nodes"], key=sort_node)
    actual_edges = sorted(data["edges"], key=sort_edge)
    exp_nodes_sorted = sorted(expected_nodes, key=sort_node)
    exp_edges_sorted = sorted(expected_edges, key=sort_edge)

    assert actual_nodes == exp_nodes_sorted, "Graph nodes do not match expected"
    assert actual_edges == exp_edges_sorted, "Graph edges do not match expected"

def test_validation_passed_file():
    passed_path = "/home/user/output/VALIDATION_PASSED"
    assert os.path.isfile(passed_path), f"File {passed_path} does not exist. Schema validation may have failed or script did not create it."