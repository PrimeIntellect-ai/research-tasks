# test_final_state.py

import os
import pytest

def test_report_csv_content():
    report_path = "/home/user/report.csv"
    assert os.path.isfile(report_path), f"Output file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_records = set()
    for line in lines:
        parts = line.split(",")
        assert len(parts) == 4, f"Invalid line format in report.csv: {line}"
        emp_id, name, score, rank = parts
        parsed_records.add((int(emp_id), name, int(score), int(rank)))

    expected_records = {
        (1, "Alice", 6, 1),
        (2, "Bob", 5, 2),
        (3, "Charlie", 2, 3),
        (6, "Frank", 2, 3)
    }

    # We check if the expected records are present
    for record in expected_records:
        assert record in parsed_records, f"Expected record {record} not found in {report_path}."

    # Ensure no extra records
    assert len(parsed_records) == len(expected_records), f"Found unexpected records in {report_path}."

def test_import_cypher_content():
    cypher_path = "/home/user/import.cypher"
    assert os.path.isfile(cypher_path), f"Output file {cypher_path} is missing."

    with open(cypher_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_nodes = {
        "CREATE (:Employee {emp_id: 1, name: 'Alice'});",
        "CREATE (:Employee {emp_id: 2, name: 'Bob'});",
        "CREATE (:Employee {emp_id: 3, name: 'Charlie'});",
        "CREATE (:Employee {emp_id: 4, name: 'David'});",
        "CREATE (:Employee {emp_id: 5, name: 'Eve'});",
        "CREATE (:Employee {emp_id: 6, name: 'Frank'});"
    }

    expected_reports = {
        "MATCH (sub:Employee {emp_id: 2}), (mgr:Employee {emp_id: 1}) CREATE (sub)-[:REPORTS_TO]->(mgr);",
        "MATCH (sub:Employee {emp_id: 3}), (mgr:Employee {emp_id: 1}) CREATE (sub)-[:REPORTS_TO]->(mgr);",
        "MATCH (sub:Employee {emp_id: 4}), (mgr:Employee {emp_id: 2}) CREATE (sub)-[:REPORTS_TO]->(mgr);",
        "MATCH (sub:Employee {emp_id: 5}), (mgr:Employee {emp_id: 2}) CREATE (sub)-[:REPORTS_TO]->(mgr);",
        "MATCH (sub:Employee {emp_id: 6}), (mgr:Employee {emp_id: 3}) CREATE (sub)-[:REPORTS_TO]->(mgr);"
    }

    expected_communications = {
        "MATCH (s:Employee {emp_id: 1}), (r:Employee {emp_id: 2}) CREATE (s)-[:COMMUNICATED_WITH]->(r);",
        "MATCH (s:Employee {emp_id: 2}), (r:Employee {emp_id: 3}) CREATE (s)-[:COMMUNICATED_WITH]->(r);",
        "MATCH (s:Employee {emp_id: 1}), (r:Employee {emp_id: 4}) CREATE (s)-[:COMMUNICATED_WITH]->(r);",
        "MATCH (s:Employee {emp_id: 5}), (r:Employee {emp_id: 1}) CREATE (s)-[:COMMUNICATED_WITH]->(r);",
        "MATCH (s:Employee {emp_id: 6}), (r:Employee {emp_id: 5}) CREATE (s)-[:COMMUNICATED_WITH]->(r);",
        "MATCH (s:Employee {emp_id: 6}), (r:Employee {emp_id: 4}) CREATE (s)-[:COMMUNICATED_WITH]->(r);"
    }

    # Verify grouping: nodes first, then reports, then communications
    node_indices = []
    report_indices = []
    comm_indices = []

    for i, line in enumerate(lines):
        if line in expected_nodes:
            node_indices.append(i)
        elif line in expected_reports:
            report_indices.append(i)
        elif line in expected_communications:
            comm_indices.append(i)
        else:
            pytest.fail(f"Unexpected or incorrectly formatted statement in {cypher_path}: {line}")

    assert len(node_indices) == len(expected_nodes), "Missing some Employee node creation statements."
    assert len(report_indices) == len(expected_reports), "Missing some REPORTS_TO relationship creation statements."
    assert len(comm_indices) == len(expected_communications), "Missing some COMMUNICATED_WITH relationship creation statements."

    # Verify order
    max_node_idx = max(node_indices)
    min_report_idx = min(report_indices)
    max_report_idx = max(report_indices)
    min_comm_idx = min(comm_indices)

    assert max_node_idx < min_report_idx, "Employee node creations must appear before REPORTS_TO creations."
    assert max_report_idx < min_comm_idx, "REPORTS_TO creations must appear before COMMUNICATED_WITH creations."