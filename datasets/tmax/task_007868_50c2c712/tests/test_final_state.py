# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/build_graph.sh"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_deadlock_citations_log():
    log_path = "/home/user/deadlock_citations.log"
    assert os.path.isfile(log_path), f"The file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "PUB1<->PUB2",
        "PUB3<->PUB4"
    ]

    assert content == expected, f"Content of {log_path} does not match the expected deadlocks."

def test_init_cypher_script():
    cypher_path = "/home/user/init.cypher"
    assert os.path.isfile(cypher_path), f"The file {cypher_path} is missing."

    with open(cypher_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "CREATE (:Project {id: 'P1', title: 'AI Research'});",
        "CREATE (:Project {id: 'P2', title: 'DB Systems'});",
        "CREATE (:Publication {id: 'PUB1', citation_count: 2});",
        "CREATE (:Publication {id: 'PUB2', citation_count: 1});",
        "CREATE (:Publication {id: 'PUB3', citation_count: 2});",
        "CREATE (:Publication {id: 'PUB4', citation_count: 2});",
        "CREATE (:Researcher {id: 'R1', name: 'Alice'});",
        "CREATE (:Researcher {id: 'R2', name: 'Bob'});",
        "CREATE (:Researcher {id: 'R3', name: 'Charlie'});",
        "CREATE (P1)-[:PRODUCED]->(PUB1);",
        "CREATE (P1)-[:PRODUCED]->(PUB2);",
        "CREATE (P2)-[:PRODUCED]->(PUB3);",
        "CREATE (P2)-[:PRODUCED]->(PUB4);",
        "CREATE (PUB1)-[:CITES]->(PUB2);",
        "CREATE (PUB1)-[:CITES]->(PUB3);",
        "CREATE (PUB2)-[:CITES]->(PUB1);",
        "CREATE (PUB2)-[:CITES]->(PUB4);",
        "CREATE (PUB3)-[:CITES]->(PUB4);",
        "CREATE (PUB4)-[:CITES]->(PUB1);",
        "CREATE (PUB4)-[:CITES]->(PUB3);",
        "CREATE (R1)-[:WORKS_ON]->(P1);",
        "CREATE (R2)-[:WORKS_ON]->(P2);",
        "CREATE (R3)-[:WORKS_ON]->(P1);"
    ]

    # Sort the content in case the script didn't sort it perfectly but generated the right lines
    # The instructions say "sorted alphabetically by the statement string"
    assert content == sorted(expected), f"Content of {cypher_path} does not match the expected Cypher statements."