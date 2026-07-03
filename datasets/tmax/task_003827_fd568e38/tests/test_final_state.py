# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/graph_parser.c"
    assert os.path.isfile(path), f"Expected C source file {path} does not exist."

def test_queries_cypher_content():
    path = "/home/user/queries.cypher"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    expected_lines = [
        "MERGE (a:Paper {id: 'P1'})-[:CITES]->(b:Paper {id: 'P2'});",
        "MERGE (a:Author {id: 'A1'})-[:WROTE]->(b:Paper {id: 'P1'});",
        "MERGE (a:Author {id: 'A2'})-[:AFFILIATED_WITH]->(b:Institution {id: 'I1'});",
        "MERGE (a:Author {id: 'A3'})-[:WROTE]->(b:Paper {id: 'P3'});"
    ]

    with open(path, 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {path} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_invalid_rows_log_content():
    path = "/home/user/invalid_rows.log"
    assert os.path.isfile(path), f"Expected error log file {path} does not exist."

    expected_lines = [
        "P2,Paper,A1,Author,CITES",
        "A1,Author,P2,Paper,READS",
        "I1,Institution,P1,Paper,WROTE"
    ]

    with open(path, 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {path} does not match expected invalid rows.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )