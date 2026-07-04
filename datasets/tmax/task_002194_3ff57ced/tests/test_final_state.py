# test_final_state.py

import os
import csv
from collections import defaultdict

def test_process_data_cpp_exists():
    file_path = "/home/user/process_data.cpp"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_summary_csv_correct():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"File {summary_path} is missing."

    employees_path = "/home/user/employees.csv"
    projects_path = "/home/user/projects.csv"

    assert os.path.isfile(employees_path), "Input employees.csv is missing."
    assert os.path.isfile(projects_path), "Input projects.csv is missing."

    # Parse employees and build hierarchy
    employees = {}
    children = defaultdict(list)

    with open(employees_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = int(row["emp_id"])
            manager_id = row["manager_id"].strip()
            employees[emp_id] = {"hours": 0, "cost": 0}
            if manager_id:
                children[int(manager_id)].append(emp_id)

    # Parse projects and accumulate direct hours/costs
    with open(projects_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = int(row["emp_id"])
            if emp_id in employees:
                employees[emp_id]["hours"] += int(row["hours"])
                employees[emp_id]["cost"] += int(row["cost"])

    # Recursive function to calculate rolled-up totals
    def rollup(emp_id):
        total_hours = employees[emp_id]["hours"]
        total_cost = employees[emp_id]["cost"]
        for child in children[emp_id]:
            child_hours, child_cost = rollup(child)
            total_hours += child_hours
            total_cost += child_cost
        return total_hours, total_cost

    # Compute expected results
    expected_results = {}
    for emp_id in employees:
        expected_results[emp_id] = rollup(emp_id)

    # Generate expected CSV content
    expected_rows = ["emp_id,total_hours,total_cost"]
    for emp_id in sorted(expected_results.keys()):
        total_hours, total_cost = expected_results[emp_id]
        expected_rows.append(f"{emp_id},{total_hours},{total_cost}")

    expected_content = "\n".join(expected_rows)

    # Read actual CSV content
    with open(summary_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {summary_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )