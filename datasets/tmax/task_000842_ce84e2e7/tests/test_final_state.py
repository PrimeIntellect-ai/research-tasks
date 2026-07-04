# test_final_state.py

import os
import json
import pytest

def test_cjson_files_exist():
    assert os.path.isfile("/home/user/cJSON.h"), "cJSON.h is missing from /home/user/"
    assert os.path.isfile("/home/user/cJSON.c"), "cJSON.c is missing from /home/user/"

def test_c_program_files_exist():
    assert os.path.isfile("/home/user/graph_processor.c"), "graph_processor.c is missing"
    assert os.path.isfile("/home/user/graph_processor"), "graph_processor executable is missing"
    assert os.access("/home/user/graph_processor", os.X_OK), "graph_processor is not executable"

def test_active_subgraph_cypher():
    cypher_path = "/home/user/active_subgraph.cypher"
    assert os.path.isfile(cypher_path), f"{cypher_path} is missing"

    with open(cypher_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        'CREATE (n1:User {id: "1", status: "active"});',
        'CREATE (n3:Group {id: "3", status: "active"});',
        'CREATE (n4:Group {id: "4", status: "active"});',
        'CREATE (n5:Resource {id: "5", status: "active"});',
        'CREATE (n7:User {id: "7", status: "active"});',
        'MATCH (a {id: "1"}), (b {id: "3"}) CREATE (a)-[:MEMBER_OF {weight: 15}]->(b);',
        'MATCH (a {id: "3"}), (b {id: "4"}) CREATE (a)-[:PARENT_OF {weight: 50}]->(b);',
        'MATCH (a {id: "3"}), (b {id: "5"}) CREATE (a)-[:HAS_ACCESS {weight: 10}]->(b);',
        'MATCH (a {id: "7"}), (b {id: "3"}) CREATE (a)-[:MEMBER_OF {weight: 12}]->(b);'
    ]

    assert lines == expected_lines, "The contents of active_subgraph.cypher do not match the expected output exactly."

def test_edge_aggregation_json():
    json_path = "/home/user/edge_aggregation.json"
    assert os.path.isfile(json_path), f"{json_path} is missing"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse JSON from {json_path}")

    expected_data = {
        "MEMBER_OF": 52,
        "PARENT_OF": 50,
        "HAS_ACCESS": 43
    }

    assert data == expected_data, "The contents of edge_aggregation.json do not match the expected aggregation."