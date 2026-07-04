# test_final_state.py

import os
import stat
import csv
import json
import pytest

SCRIPT_PATH = "/home/user/find_anomalies.sh"
OUTPUT_JSON = "/home/user/anomalies.json"
DATA_DIR = "/home/user/data"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable by the user."

def test_anomalies_json_correct():
    assert os.path.isfile(OUTPUT_JSON), f"Output file {OUTPUT_JSON} does not exist. Did you run the script?"

    # 1. Recompute the expected anomalies directly from the CSV files
    employees = {}
    emp_file = os.path.join(DATA_DIR, "employees.csv")
    with open(emp_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = row["emp_id"]
            version = int(row["version"])
            if emp_id not in employees or version > employees[emp_id]["version"]:
                employees[emp_id] = {
                    "name": row["name"],
                    "dept_id": row["dept_id"],
                    "version": version
                }

    projects = {}
    proj_file = os.path.join(DATA_DIR, "projects.csv")
    with open(proj_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            proj_id = row["proj_id"]
            version = int(row["version"])
            if proj_id not in projects or version > projects[proj_id]["version"]:
                projects[proj_id] = {
                    "proj_name": row["proj_name"],
                    "dept_id": row["dept_id"],
                    "version": version
                }

    works_on = {}
    works_file = os.path.join(DATA_DIR, "works_on.csv")
    with open(works_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = row["emp_id"]
            version = int(row["version"])
            # Deduplicate by emp_id assuming 1 active project per employee
            if emp_id not in works_on or version > works_on[emp_id]["version"]:
                works_on[emp_id] = {
                    "proj_id": row["proj_id"],
                    "version": version
                }

    expected_anomalies = []
    for emp_id, work in works_on.items():
        emp = employees.get(emp_id)
        proj = projects.get(work["proj_id"])
        if emp and proj:
            # Anomaly: Employee works on a project belonging to a different department
            if emp["dept_id"] != proj["dept_id"]:
                expected_anomalies.append({
                    "emp_name": emp["name"],
                    "proj_name": proj["proj_name"]
                })

    # Sort alphabetically by employee name as requested
    expected_anomalies.sort(key=lambda x: x["emp_name"])

    # 2. Read and validate the actual output
    with open(OUTPUT_JSON, "r") as f:
        try:
            actual_anomalies = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON} is not a valid JSON file.")

    assert isinstance(actual_anomalies, list), f"Expected {OUTPUT_JSON} to contain a JSON array."
    assert len(actual_anomalies) == len(expected_anomalies), (
        f"Expected {len(expected_anomalies)} anomalies, but found {len(actual_anomalies)}."
    )

    # 3. Compare the elements exactly
    for i, (actual, expected) in enumerate(zip(actual_anomalies, expected_anomalies)):
        assert "emp_name" in actual, f"Object at index {i} is missing 'emp_name' key."
        assert "proj_name" in actual, f"Object at index {i} is missing 'proj_name' key."

        assert actual["emp_name"] == expected["emp_name"], (
            f"Mismatch at index {i}: Expected emp_name '{expected['emp_name']}', got '{actual['emp_name']}'"
        )
        assert actual["proj_name"] == expected["proj_name"], (
            f"Mismatch at index {i}: Expected proj_name '{expected['proj_name']}', got '{actual['proj_name']}'"
        )