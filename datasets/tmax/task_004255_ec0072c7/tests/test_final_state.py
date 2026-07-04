# test_final_state.py

import os
import pytest
from collections import defaultdict

def compute_expected_report(csv_path):
    adj = defaultdict(set)
    out_degree = defaultdict(int)

    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                u, v = parts
                adj[u].add(v)
                out_degree[u] += 1

    violations = defaultdict(int)
    for a in adj:
        for b in adj[a]:
            for c in adj[b]:
                if c in adj[a]:
                    violations[a] += 1

    if not violations:
        return None

    # Find highest risk entity
    max_violations = -1
    highest_risk_entity = ""

    for entity, count in violations.items():
        if count > max_violations:
            max_violations = count
            highest_risk_entity = entity
        elif count == max_violations:
            if entity < highest_risk_entity:
                highest_risk_entity = entity

    expected_content = (
        f"Highest Risk Entity: {highest_risk_entity}\n"
        f"Violation Count: {max_violations}\n"
        f"Total Out-Degree: {out_degree[highest_risk_entity]}\n"
    )
    return expected_content

def test_compliance_report_exists_and_correct():
    csv_path = '/home/user/audit_logs.csv'
    report_path = '/home/user/compliance_report.txt'

    assert os.path.exists(csv_path), f"Audit logs CSV not found at {csv_path}"
    assert os.path.exists(report_path), f"Compliance report not found at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a file"

    expected_content = compute_expected_report(csv_path)
    assert expected_content is not None, "No violations found in the provided CSV."

    with open(report_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content.strip(), (
        f"Compliance report content does not match expected.\n"
        f"Expected:\n{expected_content.strip()}\n\n"
        f"Actual:\n{actual_content}"
    )