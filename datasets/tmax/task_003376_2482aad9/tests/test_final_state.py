# test_final_state.py

import os
import json
import csv
import subprocess
import pytest

def get_data():
    with open("/home/user/users.json", "r") as f:
        users = {u["id"]: u for u in json.load(f)}

    with open("/home/user/systems.json", "r") as f:
        systems = json.load(f)

    managers = {}
    with open("/home/user/org_chart.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                manager_id, employee_id = parts
                managers[employee_id] = manager_id

    logs = []
    with open("/home/user/access_logs.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append({
                "timestamp": int(row["timestamp"]),
                "user_id": row["user_id"],
                "system_id": row["system_id"]
            })

    return users, systems, managers, logs

def compute_expected_violations(system_id):
    users, systems, managers, logs = get_data()
    sys_req = systems.get(system_id)
    if not sys_req:
        return []

    req_dept = sys_req["req_dept"]
    req_clearance = sys_req["req_clearance"]

    violations = []

    for log in logs:
        if log["system_id"] != system_id:
            continue

        uid = log["user_id"]
        user = users.get(uid)
        if not user:
            continue

        clearance_fail = user["clearance"] < req_clearance

        user_dept = user["dept"]
        manager_id = managers.get(uid)
        manager_dept = users.get(manager_id, {}).get("dept") if manager_id else None

        dept_fail = (user_dept != req_dept) and (manager_dept != req_dept)

        if clearance_fail or dept_fail:
            if clearance_fail and dept_fail:
                reason = "Clearance and Department failed"
            elif clearance_fail:
                reason = "Clearance too low"
            else:
                reason = "Department mismatch"

            violations.append({
                "timestamp": log["timestamp"],
                "user_id": uid,
                "user_name": user["name"],
                "violation_reason": reason
            })

    violations.sort(key=lambda x: x["timestamp"], reverse=True)
    return violations[:3]

def test_audit_script_exists_and_executable():
    script_path = "/home/user/audit.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_audit_results_for_sysB():
    results_path = "/home/user/audit_results.json"
    assert os.path.exists(results_path), f"Results file {results_path} does not exist. Did the script run?"

    with open(results_path, "r") as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    expected_results = compute_expected_violations("sysB")

    assert isinstance(actual_results, list), f"Expected JSON array in {results_path}."
    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results, got {len(actual_results)}."

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert actual.get("timestamp") == expected["timestamp"], f"Mismatch in timestamp at index {i}."
        assert actual.get("user_id") == expected["user_id"], f"Mismatch in user_id at index {i}."
        assert actual.get("user_name") == expected["user_name"], f"Mismatch in user_name at index {i}."
        assert actual.get("violation_reason") == expected["violation_reason"], f"Mismatch in violation_reason at index {i}."

def test_audit_script_dynamic_execution():
    script_path = "/home/user/audit.sh"
    results_path = "/home/user/audit_results.json"

    # Run for sysA to ensure it's parameterized correctly
    result = subprocess.run([script_path, "sysA"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed when running for sysA. Error: {result.stderr}"

    assert os.path.exists(results_path), f"Results file {results_path} not found after running script for sysA."

    with open(results_path, "r") as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON after running for sysA.")

    expected_results = compute_expected_violations("sysA")

    assert isinstance(actual_results, list), f"Expected JSON array in {results_path} for sysA."
    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results for sysA, got {len(actual_results)}."

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert actual.get("timestamp") == expected["timestamp"], f"Mismatch in timestamp for sysA at index {i}."
        assert actual.get("user_id") == expected["user_id"], f"Mismatch in user_id for sysA at index {i}."
        assert actual.get("user_name") == expected["user_name"], f"Mismatch in user_name for sysA at index {i}."
        assert actual.get("violation_reason") == expected["violation_reason"], f"Mismatch in violation_reason for sysA at index {i}."