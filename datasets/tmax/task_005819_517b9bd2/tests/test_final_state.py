# test_final_state.py
import os
import csv
import json
import pytest

def get_expected_result():
    data_dir = "/home/user/data"

    employees = {}
    reports_map = {}
    with open(os.path.join(data_dir, "employees.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = row["emp_id"]
            employees[emp_id] = row
            manager_id = row["manager_id"]
            if manager_id not in reports_map:
                reports_map[manager_id] = []
            reports_map[manager_id].append(emp_id)

    projects = {}
    with open(os.path.join(data_dir, "projects.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            projects[row["proj_id"]] = row

    deps = {}
    with open(os.path.join(data_dir, "proj_deps.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["proj_id"]
            if pid not in deps:
                deps[pid] = []
            deps[pid].append(row["depends_on_proj_id"])

    target = "PRJ-Omega"
    visited_deps = set()
    queue = deps.get(target, []).copy()
    while queue:
        curr = queue.pop(0)
        if curr not in visited_deps:
            visited_deps.add(curr)
            queue.extend(deps.get(curr, []))

    owners = set()
    for d in visited_deps:
        if d in projects:
            owners.add(projects[d]["owner_emp_id"])

    affected = set()
    queue = list(owners)
    while queue:
        curr = queue.pop(0)
        if curr not in affected:
            affected.add(curr)
            queue.extend(reports_map.get(curr, []))

    affected_employees = [employees[emp_id] for emp_id in affected]
    affected_employees.sort(key=lambda x: x["name"])

    total = len(affected_employees)

    page = 2
    size = 3
    start = (page - 1) * size
    end = start + size
    page_results = affected_employees[start:end]

    return {
        "page": page,
        "total_results": total,
        "results": [{"emp_id": e["emp_id"], "name": e["name"]} for e in page_results]
    }

def test_result_json():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Expected result file at {result_path} not found."

    with open(result_path, "r") as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    expected = get_expected_result()

    assert actual.get("page") == expected["page"], f"Page number mismatch. Expected {expected['page']}, got {actual.get('page')}."
    assert actual.get("total_results") == expected["total_results"], f"Total results mismatch. Expected {expected['total_results']}, got {actual.get('total_results')}."

    actual_results = actual.get("results", [])
    expected_results = expected["results"]

    assert len(actual_results) == len(expected_results), f"Results length mismatch. Expected {len(expected_results)}, got {len(actual_results)}."

    for i, (act, exp) in enumerate(zip(actual_results, expected_results)):
        assert act.get("emp_id") == exp["emp_id"], f"emp_id mismatch at index {i}. Expected {exp['emp_id']}, got {act.get('emp_id')}."
        assert act.get("name") == exp["name"], f"name mismatch at index {i}. Expected {exp['name']}, got {act.get('name')}."