# test_final_state.py

import os
import stat
import json
import csv
import pytest

CSV_PATH = "/home/user/legacy_users.csv"
ENVS = ["staging", "prod"]

def get_expected_data():
    assert os.path.exists(CSV_PATH), f"{CSV_PATH} does not exist."
    users = []
    departments = set()
    roles = {}

    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row["username"])
            departments.add(row["department"])
            role = row["role"]
            if role not in roles:
                roles[role] = []
            roles[role].append(row["username"])

    for role in roles:
        roles[role].sort()

    return {
        "num_users": len(users),
        "num_departments": len(departments),
        "departments": list(departments),
        "roles": roles
    }

def test_directories_and_files():
    data = get_expected_data()
    departments = data["departments"]

    for env in ENVS:
        base_dir = f"/home/user/cloud_deployment/{env}"
        assert os.path.isdir(base_dir), f"Base directory {base_dir} is missing."

        for dept in departments:
            dept_dir = os.path.join(base_dir, dept)
            assert os.path.isdir(dept_dir), f"Department directory {dept_dir} is missing."

            # Check directory permissions (755)
            st = os.stat(dept_dir)
            mode = stat.S_IMODE(st.st_mode)
            assert mode == 0o755, f"Permissions for {dept_dir} are {oct(mode)}, expected 0o755."

            # Check files and permissions (644)
            for file_name in ["__init__.py", "settings.conf"]:
                file_path = os.path.join(dept_dir, file_name)
                assert os.path.isfile(file_path), f"File {file_path} is missing."
                st_file = os.stat(file_path)
                file_mode = stat.S_IMODE(st_file.st_mode)
                assert file_mode == 0o644, f"Permissions for {file_path} are {oct(file_mode)}, expected 0o644."

def test_rbac_json():
    data = get_expected_data()
    expected_roles = data["roles"]

    for env in ENVS:
        rbac_path = f"/home/user/cloud_deployment/{env}/rbac.json"
        assert os.path.isfile(rbac_path), f"RBAC file {rbac_path} is missing."

        with open(rbac_path, "r") as f:
            try:
                rbac_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"File {rbac_path} is not valid JSON.")

        assert rbac_data == expected_roles, f"Content of {rbac_path} does not match expected RBAC configuration."

def test_log_files():
    data = get_expected_data()
    num_users = data["num_users"]
    num_depts = data["num_departments"]

    for env in ENVS:
        log_path = f"/home/user/migration_summary_{env}.log"
        assert os.path.isfile(log_path), f"Log file {log_path} is missing."

        expected_log = f"[{env}] Deployment ready. Migrated {num_users} users across {num_depts} departments."

        with open(log_path, "r") as f:
            log_content = f.read().strip()

        assert log_content == expected_log, f"Log content in {log_path} is incorrect. Expected: '{expected_log}', Got: '{log_content}'"