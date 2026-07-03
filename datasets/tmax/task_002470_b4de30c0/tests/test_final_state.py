# test_final_state.py

import os
import json
import csv
import pytest

def test_jaccard_similarity_of_edges():
    agent_csv_path = "/home/user/projected_edges.csv"
    data_path = "/home/user/data/entities.jsonl"

    assert os.path.exists(agent_csv_path), f"Agent output file not found at {agent_csv_path}"
    assert os.path.exists(data_path), f"Data file not found at {data_path}"

    # Re-derive expected edges from the source data
    expected_edges = set()
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            doc = json.loads(line)

            # Extract Company ID
            company_id = str(doc.get("id", ""))

            # Extract Employees and Projects
            employees = doc.get("employees", [])
            for emp in employees:
                emp_id = str(emp.get("id", ""))
                if company_id and emp_id:
                    expected_edges.add((company_id, emp_id, "EMPLOYS"))

                projects = emp.get("projects", [])
                for proj in projects:
                    proj_id = str(proj)
                    if emp_id and proj_id:
                        expected_edges.add((emp_id, proj_id, "WORKS_ON"))

    assert len(expected_edges) > 0, "Failed to parse expected edges from source data."

    # Read agent's edges
    agent_edges = set()
    with open(agent_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert "source_id" in reader.fieldnames, "Missing 'source_id' column in CSV header."
        assert "target_id" in reader.fieldnames, "Missing 'target_id' column in CSV header."
        assert "edge_type" in reader.fieldnames, "Missing 'edge_type' column in CSV header."

        for row in reader:
            agent_edges.add((str(row["source_id"]), str(row["target_id"]), str(row["edge_type"])))

    # Calculate Jaccard similarity
    intersection = agent_edges.intersection(expected_edges)
    union = agent_edges.union(expected_edges)

    jaccard = len(intersection) / len(union) if len(union) > 0 else 0.0

    assert jaccard >= 0.99, (
        f"Jaccard similarity {jaccard:.4f} is below threshold 0.99. "
        f"Agent produced {len(agent_edges)} edges, expected {len(expected_edges)} edges. "
        f"Intersection: {len(intersection)}."
    )