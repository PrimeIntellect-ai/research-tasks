# test_final_state.py

import os
import re
import pytest

def test_query_plan():
    query_plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(query_plan_path), f"File {query_plan_path} is missing."

    with open(query_plan_path, 'r') as f:
        content = f.read().upper()

    assert "INDEX" in content, "The query plan does not indicate the use of an INDEX."
    assert "USE TEMP B-TREE FOR ORDER BY" not in content, "The query plan indicates an explicit sort (USE TEMP B-TREE FOR ORDER BY), which means the index was not used properly for the window function."

def test_import_cypher():
    cypher_path = "/home/user/import.cypher"
    assert os.path.isfile(cypher_path), f"File {cypher_path} is missing."

    with open(cypher_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    def normalize_numbers(text):
        # Find all numbers and format them to remove trailing zeros after decimal point
        def repl(match):
            val = float(match.group(0))
            if val.is_integer():
                return str(int(val))
            return str(val)
        return re.sub(r'\b\d+(?:\.\d+)?\b', repl, text)

    normalized_lines = set(normalize_numbers(line) for line in lines)

    expected_lines = [
        "MERGE (s:User {id: 'Alice'}) MERGE (r:User {id: 'Bob'}) CREATE (s)-[:TRANSFERRED {tx_id: 1, amount: 100, running_total: 100, rank: 1}]->(r);",
        "MERGE (s:User {id: 'Alice'}) MERGE (r:User {id: 'Dave'}) CREATE (s)-[:TRANSFERRED {tx_id: 3, amount: 25.5, running_total: 125.5, rank: 2}]->(r);",
        "MERGE (s:User {id: 'Alice'}) MERGE (r:User {id: 'Bob'}) CREATE (s)-[:TRANSFERRED {tx_id: 4, amount: 10, running_total: 135.5, rank: 3}]->(r);",
        "MERGE (s:User {id: 'Bob'}) MERGE (r:User {id: 'Charlie'}) CREATE (s)-[:TRANSFERRED {tx_id: 2, amount: 50, running_total: 50, rank: 1}]->(r);",
        "MERGE (s:User {id: 'Bob'}) MERGE (r:User {id: 'Dave'}) CREATE (s)-[:TRANSFERRED {tx_id: 6, amount: 75, running_total: 125, rank: 2}]->(r);",
        "MERGE (s:User {id: 'Charlie'}) MERGE (r:User {id: 'Alice'}) CREATE (s)-[:TRANSFERRED {tx_id: 5, amount: 200, running_total: 200, rank: 1}]->(r);"
    ]

    normalized_expected = set(normalize_numbers(line) for line in expected_lines)

    missing = normalized_expected - normalized_lines
    extra = normalized_lines - normalized_expected

    assert not missing, f"Missing expected Cypher commands: {missing}"
    assert not extra, f"Found unexpected Cypher commands: {extra}"
    assert len(normalized_lines) == len(expected_lines), "The number of unique Cypher commands does not match the expected count."