# test_final_state.py
import os
import json
import csv
import pytest

def get_expected_violations():
    users = {}
    with open('/home/user/audit_data/users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['user_id']] = row['user_name']

    user_roles = {}
    with open('/home/user/audit_data/user_roles.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_roles.setdefault(row['user_id'], set()).add(row['role_id'])

    role_hierarchy = {}
    with open('/home/user/audit_data/role_hierarchy.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            role_hierarchy.setdefault(row['parent_role_id'], set()).add(row['child_role_id'])

    role_permissions = {}
    with open('/home/user/audit_data/role_permissions.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            role_permissions.setdefault(row['role_id'], set()).add(row['permission_name'])

    def get_all_inherited_roles(role_id, visited=None):
        if visited is None:
            visited = set()
        if role_id in visited:
            return visited
        visited.add(role_id)
        for child in role_hierarchy.get(role_id, set()):
            get_all_inherited_roles(child, visited)
        return visited

    violations = []
    for user_id in sorted(users.keys()):
        roles = user_roles.get(user_id, set())
        all_roles = set()
        for r in roles:
            all_roles.update(get_all_inherited_roles(r))

        perms = set()
        for r in all_roles:
            perms.update(role_permissions.get(r, set()))

        if 'FUNDS_INITIATE' in perms and 'FUNDS_APPROVE' in perms:
            violations.append({
                "user_id": user_id,
                "user_name": users[user_id],
                "violation": True
            })

    return violations

def test_go_program_exists():
    assert os.path.isfile("/home/user/audit.go"), "The Go program /home/user/audit.go was not found."

def test_json_output_exists():
    assert os.path.isfile("/home/user/sod_violations.json"), "The output file /home/user/sod_violations.json was not found."

def test_json_output_correctness():
    expected = get_expected_violations()

    with open("/home/user/sod_violations.json", "r") as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/sod_violations.json is not valid JSON.")

    assert isinstance(actual, list), "The JSON output must be a list of objects."

    # Sort both just in case, though the spec requires actual to be sorted
    expected_sorted = sorted(expected, key=lambda x: x.get('user_id', ''))
    actual_sorted = sorted(actual, key=lambda x: x.get('user_id', ''))

    assert actual == expected_sorted, f"The JSON output does not match the expected violations. Expected: {expected_sorted}, Actual: {actual}"

def test_json_output_sorted():
    with open("/home/user/sod_violations.json", "r") as f:
        actual = json.load(f)

    user_ids = [obj.get('user_id') for obj in actual]
    assert user_ids == sorted(user_ids), "The JSON output is not sorted by user_id in ascending order."