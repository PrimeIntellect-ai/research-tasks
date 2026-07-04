# test_final_state.py

import os
import pytest

def test_top_engineers_file():
    file_path = '/home/user/top_engineers.txt'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Eve,100",
        "Charlie,22",
        "Alice,15"
    ]

    assert lines == expected_lines, f"Content of {file_path} does not match the expected top 3 engineers and their out-degrees."

def test_cypher_output_file():
    file_path = '/home/user/cypher_output.cql'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "CREATE (:User {id: 5, name: 'Eve', department: 'Engineering'});",
        "CREATE (:User {id: 3, name: 'Charlie', department: 'Engineering'});",
        "CREATE (:User {id: 1, name: 'Alice', department: 'Engineering'});",
        "MATCH (s:User {id: 5}), (r:User {id: 1}) CREATE (s)-[:MESSAGED {count: 100}]->(r);",
        "MATCH (s:User {id: 3}), (r:User {id: 1}) CREATE (s)-[:MESSAGED {count: 2}]->(r);",
        "MATCH (s:User {id: 3}), (r:User {id: 4}) CREATE (s)-[:MESSAGED {count: 20}]->(r);",
        "MATCH (s:User {id: 1}), (r:User {id: 2}) CREATE (s)-[:MESSAGED {count: 10}]->(r);",
        "MATCH (s:User {id: 1}), (r:User {id: 3}) CREATE (s)-[:MESSAGED {count: 5}]->(r);"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} does not match expected output.\nExpected: {expected}\nActual: {actual}"