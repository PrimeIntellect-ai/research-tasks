# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    source_file = "/home/user/graph_converter.c"
    assert os.path.exists(source_file), f"C source file {source_file} is missing."
    assert os.path.isfile(source_file), f"Path {source_file} is not a regular file."

def test_executable_exists_and_executable():
    executable = "/home/user/converter"
    assert os.path.exists(executable), f"Compiled executable {executable} is missing."
    assert os.path.isfile(executable), f"Path {executable} is not a regular file."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_cypher_output_correct():
    output_file = "/home/user/import.cypher"
    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(output_file), f"Path {output_file} is not a regular file."

    expected_lines = [
        "MERGE (a:Node {id: 'NodeA'}) MERGE (b:Node {id: 'NodeB'}) MERGE (a)-[r:TRANSFERRED {total_data: 80}]->(b);",
        "MERGE (a:Node {id: 'NodeA'}) MERGE (b:Node {id: 'NodeC'}) MERGE (a)-[r:TRANSFERRED {total_data: 10}]->(b);",
        "MERGE (a:Node {id: 'NodeB'}) MERGE (b:Node {id: 'NodeC'}) MERGE (a)-[r:TRANSFERRED {total_data: 20}]->(b);",
        "MERGE (a:Node {id: 'NodeC'}) MERGE (b:Node {id: 'NodeA'}) MERGE (a)-[r:TRANSFERRED {total_data: 150}]->(b);"
    ]

    with open(output_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"