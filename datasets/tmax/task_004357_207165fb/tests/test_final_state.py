# test_final_state.py

import os
import pytest

def test_relationships_cypher_exists_and_correct():
    out_path = "/home/user/relationships.cypher"
    assert os.path.isfile(out_path), f"The output file {out_path} was not generated."

    with open(out_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 valid relationships, but found {len(lines)}. The cross join bug might not be fully fixed."

    expected_relationships = [
        "MATCH (u:User {user_id: 1}), (p:Purchase {purchase_id: 101}) CREATE (u)-[:BOUGHT]->(p);",
        "MATCH (u:User {user_id: 1}), (p:Purchase {purchase_id: 102}) CREATE (u)-[:BOUGHT]->(p);",
        "MATCH (u:User {user_id: 2}), (p:Purchase {purchase_id: 103}) CREATE (u)-[:BOUGHT]->(p);",
        "MATCH (u:User {user_id: 4}), (p:Purchase {purchase_id: 104}) CREATE (u)-[:BOUGHT]->(p);",
        "MATCH (u:User {user_id: 4}), (p:Purchase {purchase_id: 105}) CREATE (u)-[:BOUGHT]->(p);"
    ]

    for expected in expected_relationships:
        assert expected in lines, f"Missing expected relationship in output: {expected}"

    # Ensure no incorrect relationships exist (e.g. user 1 buying purchase 103)
    invalid_relationship = "MATCH (u:User {user_id: 1}), (p:Purchase {purchase_id: 103}) CREATE (u)-[:BOUGHT]->(p);"
    assert invalid_relationship not in lines, "Found an invalid relationship in the output file. The cross join bug is still present."

def test_python_script_modified():
    script_path = "/home/user/generate_cypher.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."