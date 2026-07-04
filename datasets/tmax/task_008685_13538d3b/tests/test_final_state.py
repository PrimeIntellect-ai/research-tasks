# test_final_state.py

import os
import json
import pytest
from collections import defaultdict

def test_bottleneck_chain_output():
    json_path = "/home/user/employees.json"
    output_path = "/home/user/bottleneck_chain.txt"

    assert os.path.isfile(json_path), f"Input file {json_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(json_path, "r") as f:
        try:
            employees = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    # Compute the expected chain dynamically based on the current JSON contents
    reports_count = defaultdict(int)
    emp_dict = {}
    ceo_id = None

    for emp in employees:
        emp_dict[emp["emp_id"]] = emp
        if emp["manager_id"] is None:
            ceo_id = emp["emp_id"]
        else:
            reports_count[emp["manager_id"]] += 1

    assert ceo_id is not None, "No CEO (manager_id = null) found in the dataset."
    assert reports_count, "No reports found in the dataset."

    # Find the bottleneck manager
    # max reports, tie-breaker lowest emp_id
    bottleneck_id = None
    max_reports = -1

    for mgr_id, count in reports_count.items():
        if count > max_reports:
            max_reports = count
            bottleneck_id = mgr_id
        elif count == max_reports:
            if bottleneck_id is None or mgr_id < bottleneck_id:
                bottleneck_id = mgr_id

    assert bottleneck_id is not None, "Could not identify a bottleneck manager."

    # Trace path from CEO to bottleneck manager
    # We will trace bottom-up from bottleneck_id to ceo_id, then reverse
    path = []
    current_id = bottleneck_id

    # Safety against infinite loops in case of malformed data
    visited = set()
    while current_id is not None:
        if current_id in visited:
            pytest.fail("Cycle detected in the management chain.")
        visited.add(current_id)

        emp = emp_dict.get(current_id)
        assert emp is not None, f"Employee ID {current_id} not found."
        path.append(emp["name"])

        if current_id == ceo_id:
            break

        current_id = emp["manager_id"]

    path.reverse()
    expected_output = " -> ".join(path)

    # Read the actual output
    with open(output_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Output in {output_path} is incorrect.\n"
        f"Expected: '{expected_output}'\n"
        f"Actual:   '{actual_output}'"
    )