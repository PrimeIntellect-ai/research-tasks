# test_final_state.py

import os
import json
import pytest
from collections import defaultdict

def test_audit_pipeline_script_exists():
    assert os.path.isfile("/home/user/audit_pipeline.py"), "/home/user/audit_pipeline.py does not exist."

def test_flagged_audit_output():
    output_file = "/home/user/flagged_audit.json"
    assert os.path.isfile(output_file), f"{output_file} does not exist. Did you run the script?"

    # Read the output file
    with open(output_file, "r") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} is not valid JSON.")

    # Recompute the expected result from the source data
    emp_file = "/home/user/audit_data/employees.json"
    tx_file = "/home/user/audit_data/transactions.json"

    assert os.path.isfile(emp_file), f"Source file {emp_file} is missing."
    assert os.path.isfile(tx_file), f"Source file {tx_file} is missing."

    with open(emp_file, "r") as f:
        employees = json.load(f)

    with open(tx_file, "r") as f:
        transactions = json.load(f)

    # Build hierarchy graph
    manager_to_direct_reports = defaultdict(list)
    for emp in employees:
        mgr = emp.get("manager_id")
        if mgr:
            manager_to_direct_reports[mgr].append(emp.get("emp_id"))

    # Traverse to find all downstream employees of MGR_042
    target_mgr = "MGR_042"
    downstream_emps = set()
    queue = manager_to_direct_reports[target_mgr].copy()

    while queue:
        current = queue.pop(0)
        downstream_emps.add(current)
        queue.extend(manager_to_direct_reports[current])

    # Aggregate transactions
    emp_totals = defaultdict(float)
    for tx in transactions:
        if tx.get("status") == "COMPLETED" and tx.get("emp_id") in downstream_emps:
            emp_totals[tx["emp_id"]] += float(tx["amount"])

    # Sort descending and limit to top 3
    sorted_totals = sorted(emp_totals.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_totals[:3]

    expected_output = [{"emp_id": emp_id, "total_amount": amt} for emp_id, amt in top_3]

    # Compare
    assert isinstance(output_data, list), f"Expected output to be a JSON array, got {type(output_data).__name__}."
    assert len(output_data) == len(expected_output), f"Expected {len(expected_output)} records, got {len(output_data)}."

    for i, (actual, expected) in enumerate(zip(output_data, expected_output)):
        assert actual.get("emp_id") == expected["emp_id"], f"Record {i+1}: expected emp_id '{expected['emp_id']}', got '{actual.get('emp_id')}'."
        assert actual.get("total_amount") == expected["total_amount"], f"Record {i+1}: expected total_amount {expected['total_amount']}, got {actual.get('total_amount')}."