# test_final_state.py

import os
import pytest

def test_graph_mapper_c_fixed():
    file_path = "/home/user/graph_mapper.c"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, "r") as f:
        content = f.read()

    # Check that some condition was added to filter the cross join
    assert "if" in content and "source_id" in content and "id" in content, \
        "The C program does not appear to contain a conditional check linking source_id and table id."

def test_mapped_graph_txt():
    file_path = "/home/user/mapped_graph.txt"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "(Backup_100)-[:HAS]->(orders)-[:REFERENCES]->(Table_1)",
        "(Backup_100)-[:HAS]->(orders)-[:REFERENCES]->(Table_3)",
        "(Backup_101)-[:HAS]->(orders)-[:REFERENCES]->(Table_4)",
        "(Backup_101)-[:HAS]->(orders)-[:REFERENCES]->(Table_6)",
        "(Backup_101)-[:HAS]->(reviews)-[:REFERENCES]->(Table_4)",
        "(Backup_101)-[:HAS]->(reviews)-[:REFERENCES]->(Table_6)",
        "(Backup_102)-[:HAS]->(orders)-[:REFERENCES]->(Table_8)"
    ]

    assert sorted(expected_lines) == expected_lines, "Expected lines are not sorted."

    assert lines == expected_lines, \
        f"{file_path} does not match the expected output or is not sorted properly."

def test_backup_summary_csv():
    file_path = "/home/user/backup_summary.csv"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "backup_id,fk_count",
        "100,2",
        "101,4",
        "102,1"
    ]

    assert lines == expected_lines, \
        f"{file_path} does not contain the expected summary statistics or is not sorted correctly."