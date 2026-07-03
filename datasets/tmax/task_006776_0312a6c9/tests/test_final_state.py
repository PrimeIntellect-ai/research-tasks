# test_final_state.py
import os
import csv
import json
import pytest

def test_audit_script_exists():
    script_path = "/home/user/audit_script.py"
    assert os.path.exists(script_path), f"Expected script at {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_compliance_report_correctness():
    graph_path = "/home/user/audit_graph.json"
    report_path = "/home/user/compliance_report.csv"

    assert os.path.exists(graph_path), f"Input graph at {graph_path} is missing."
    assert os.path.exists(report_path), f"Output report at {report_path} was not generated."

    with open(graph_path, "r") as f:
        data = json.load(f)

    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]

    # Identify PII databases
    pii_dbs = {n["id"] for n in nodes.values() if n.get("type") == "Database" and n.get("contains_pii") is True}

    # Identify HR and Compliance departments
    allowed_depts = {n["id"] for n in nodes.values() if n.get("type") == "Department" and n.get("name") in ("HR", "Compliance")}

    # Map relationships
    employee_depts = {}
    employee_roles = {}
    role_dbs = {}

    for edge in edges:
        src, tgt, rel = edge["source"], edge["target"], edge["relationship"]
        if rel == "WORKS_IN":
            employee_depts.setdefault(src, set()).add(tgt)
        elif rel == "HAS_ROLE":
            employee_roles.setdefault(src, set()).add(tgt)
        elif rel == "CAN_ACCESS":
            role_dbs.setdefault(src, set()).add(tgt)

    # Calculate violations
    violations = []
    for node_id, node in nodes.items():
        if node.get("type") == "Employee":
            depts = employee_depts.get(node_id, set())
            if not depts.intersection(allowed_depts):
                # Check DB access
                roles = employee_roles.get(node_id, set())
                accessible_dbs = set()
                for r in roles:
                    accessible_dbs.update(role_dbs.get(r, set()))

                unauthorized_pii_dbs = accessible_dbs.intersection(pii_dbs)
                if unauthorized_pii_dbs:
                    violations.append({
                        "employee_id": node_id,
                        "employee_name": node["name"],
                        "unauthorized_db_count": len(unauthorized_pii_dbs)
                    })

    # Sort descending by count, ascending by name
    violations.sort(key=lambda x: (-x["unauthorized_db_count"], x["employee_name"]))
    expected_top_3 = violations[:3]

    # Read output CSV
    with open(report_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["employee_id", "employee_name", "unauthorized_db_count"], \
            "CSV header does not match the exact required format."

        rows = list(reader)

    assert len(rows) == len(expected_top_3), f"Expected {len(expected_top_3)} rows in CSV, found {len(rows)}."

    for i, (row, expected) in enumerate(zip(rows, expected_top_3)):
        assert row[0] == expected["employee_id"], f"Row {i+1}: expected employee_id {expected['employee_id']}, got {row[0]}"
        assert row[1] == expected["employee_name"], f"Row {i+1}: expected employee_name {expected['employee_name']}, got {row[1]}"
        assert row[2] == str(expected["unauthorized_db_count"]), f"Row {i+1}: expected unauthorized_db_count {expected['unauthorized_db_count']}, got {row[2]}"