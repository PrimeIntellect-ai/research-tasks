# test_final_state.py

import os
import csv
import pytest

def test_results_file_correctness():
    log_path = "/home/user/access_log.csv"
    results_path = "/home/user/results.txt"

    assert os.path.exists(log_path), f"File {log_path} is missing."
    assert os.path.exists(results_path), f"File {results_path} is missing. Did you run the C++ program?"

    user_roles = {}
    role_resources = {}

    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = int(row['user_id'].strip())
            role = row['role'].strip()
            resource = row['resource'].strip()

            user_roles[uid] = role
            if role not in role_resources:
                role_resources[role] = set()
            role_resources[role].add(resource)

    # Find roles that grant access to PROD_DB
    prod_roles = {role for role, resources in role_resources.items() if 'PROD_DB' in resources}

    # Find all users with those roles
    prod_users = [uid for uid, role in user_roles.items() if role in prod_roles]

    # Sort DESC, skip 2, limit 3
    prod_users.sort(reverse=True)
    expected_uids = prod_users[2:5]

    expected_lines = [f"USER_ID: {uid}" for uid in expected_uids]

    with open(results_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {results_path} do not match the expected output. "
        f"Expected: {expected_lines}, but got: {actual_lines}"
    )

def test_cypher_query_contents():
    query_path = "/home/user/query.cypher"
    assert os.path.exists(query_path), f"File {query_path} is missing."

    with open(query_path, 'r') as f:
        content = f.read().upper()

    required_keywords = [
        "MATCH",
        "SKIP 2",
        "LIMIT 3",
        "DESC",
        "PROD_DB",
        "HAS_ROLE",
        "CAN_ACCESS"
    ]

    for keyword in required_keywords:
        assert keyword in content, f"Expected keyword/phrase '{keyword}' missing in {query_path}"