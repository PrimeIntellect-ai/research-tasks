# test_final_state.py

import os
import stat
import sqlite3
import csv
from collections import defaultdict, deque
import subprocess

DB_PATH = "/home/user/audit.db"
SCRIPT_PATH = "/home/user/analyze_audit.sh"
CSV_PATH = "/home/user/recent_violations.csv"

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_sqlite3_installed():
    """Check if sqlite3 CLI is installed."""
    try:
        subprocess.run(["sqlite3", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        assert False, "sqlite3 CLI tool is not installed."
    except subprocess.CalledProcessError:
        assert False, "sqlite3 CLI tool is installed but failed to run."

def test_script_contains_reindex():
    """Check if the script contains the REINDEX command."""
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read().upper()
    assert "REINDEX" in content, "Script does not appear to contain a REINDEX command."

def compute_expected_violations():
    """Compute the expected violations directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch all data
    users = {row['user_id']: row['username'] for row in cursor.execute("SELECT * FROM users")}

    user_roles = defaultdict(list)
    for row in cursor.execute("SELECT * FROM user_roles"):
        user_roles[row['user_id']].append(row['role_id'])

    inheritance = defaultdict(list)
    for row in cursor.execute("SELECT * FROM role_inheritance"):
        # Parent inherits all permissions of its child roles
        inheritance[row['parent_role_id']].append(row['child_role_id'])

    role_perms = defaultdict(list)
    for row in cursor.execute("SELECT * FROM role_permissions"):
        role_perms[row['role_id']].append(row['resource_name'])

    logs = [dict(row) for row in cursor.execute("SELECT * FROM access_logs")]
    conn.close()

    # Compute effective permissions per user
    user_effective_perms = defaultdict(set)
    for user_id in users:
        roles_to_process = deque(user_roles[user_id])
        processed_roles = set()

        while roles_to_process:
            current_role = roles_to_process.popleft()
            if current_role in processed_roles:
                continue
            processed_roles.add(current_role)

            # Add permissions for this role
            for perm in role_perms[current_role]:
                user_effective_perms[user_id].add(perm)

            # Add child roles
            for child_role in inheritance[current_role]:
                if child_role not in processed_roles:
                    roles_to_process.append(child_role)

    # Find violations
    violations = []
    for log in logs:
        user_id = log['user_id']
        resource = log['resource_name']
        if resource not in user_effective_perms[user_id]:
            violations.append({
                'username': users[user_id],
                'resource_name': resource,
                'timestamp': log['timestamp']
            })

    # Group by user and take top 2 recent
    user_violations = defaultdict(list)
    for v in violations:
        user_violations[v['username']].append(v)

    final_violations = []
    for username, v_list in user_violations.items():
        # Sort by timestamp descending
        v_list.sort(key=lambda x: x['timestamp'], reverse=True)
        final_violations.extend(v_list[:2])

    # Final sort: username asc, timestamp desc
    final_violations.sort(key=lambda x: (x['username'], -ord(x['timestamp'][0]))) 
    # To properly sort timestamp desc:
    final_violations.sort(key=lambda x: (x['username']))

    # Since we need to sort by username asc, then timestamp desc:
    def sort_key(item):
        return (item['username'], item['timestamp'])

    # Actually, python sort is stable. Sort by timestamp desc first, then username asc.
    final_violations.sort(key=lambda x: x['timestamp'], reverse=True)
    final_violations.sort(key=lambda x: x['username'])

    return final_violations

def test_csv_output():
    """Check if the generated CSV matches the expected output."""
    assert os.path.exists(CSV_PATH), f"Output file {CSV_PATH} does not exist."

    expected_data = compute_expected_violations()

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        actual_data = list(reader)

    assert reader.fieldnames == ['username', 'resource_name', 'timestamp'], \
        f"CSV headers are incorrect. Expected ['username', 'resource_name', 'timestamp'], got {reader.fieldnames}"

    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} rows in CSV, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual['username'] == expected['username'], f"Row {i+1} username mismatch: expected {expected['username']}, got {actual['username']}"
        assert actual['resource_name'] == expected['resource_name'], f"Row {i+1} resource_name mismatch: expected {expected['resource_name']}, got {actual['resource_name']}"
        assert actual['timestamp'] == expected['timestamp'], f"Row {i+1} timestamp mismatch: expected {expected['timestamp']}, got {actual['timestamp']}"