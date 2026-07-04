# test_final_state.py
import os
import json
import sqlite3
import pytest

def get_expected_users():
    """Derive the expected users dynamically from the database and policies."""
    policies_path = '/home/user/policies.json'
    db_path = '/home/user/iam.db'

    assert os.path.exists(policies_path), f"Missing {policies_path}"
    assert os.path.exists(db_path), f"Missing {db_path}"

    with open(policies_path, 'r') as f:
        policies = json.load(f)

    allowed_groups = policies.get("DOC-77X", {}).get("allowed_groups", [])
    if not allowed_groups:
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    placeholders = ','.join(['?'] * len(allowed_groups))
    cursor.execute(f"SELECT id FROM groups WHERE group_name IN ({placeholders})", allowed_groups)
    group_ids = [row[0] for row in cursor.fetchall()]

    visited_groups = set()
    queue = list(group_ids)
    user_ids = set()

    # BFS to resolve nested groups and collect user IDs
    while queue:
        current_group = queue.pop(0)
        if current_group in visited_groups:
            continue
        visited_groups.add(current_group)

        cursor.execute("SELECT member_user_id, member_group_id FROM group_members WHERE group_id = ?", (current_group,))
        for u_id, g_id in cursor.fetchall():
            if u_id is not None:
                user_ids.add(u_id)
            if g_id is not None and g_id not in visited_groups:
                queue.append(g_id)

    if not user_ids:
        conn.close()
        return []

    u_placeholders = ','.join(['?'] * len(user_ids))
    cursor.execute(f"SELECT username FROM users WHERE id IN ({u_placeholders})", list(user_ids))
    usernames = sorted([row[0] for row in cursor.fetchall()])

    conn.close()
    return usernames

def test_audit_result_correctness():
    """Verify that the generated audit_result.json matches the expected schema and derived truth."""
    result_path = '/home/user/audit_result.json'
    assert os.path.exists(result_path), f"The output file {result_path} was not created."

    with open(result_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {result_path} does not contain valid JSON.")

    assert "document" in result, "The key 'document' is missing from the JSON output."
    assert result["document"] == "DOC-77X", f"Expected document 'DOC-77X', but got '{result['document']}'."

    assert "authorized_users" in result, "The key 'authorized_users' is missing from the JSON output."
    actual_users = result["authorized_users"]

    assert isinstance(actual_users, list), "'authorized_users' should be a list."

    # Check sorting and duplicates
    assert actual_users == sorted(actual_users), "The 'authorized_users' list is not sorted alphabetically."
    assert len(actual_users) == len(set(actual_users)), "The 'authorized_users' list contains duplicate usernames."

    # Compare with derived truth
    expected_users = get_expected_users()
    assert actual_users == expected_users, f"Authorized users mismatch. Expected {expected_users}, but got {actual_users}."