# test_final_state.py
import os
import json
import sqlite3
import ast

def test_log_processor_fixed():
    script_path = "/home/user/log_processor.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for parameterized queries
    assert "?" in content or ":username" in content or "%s" in content, \
        "The script does not seem to use parameterized queries."
    assert "f\"SELECT" not in content and "f'SELECT" not in content, \
        "The script still appears to use f-strings for the SQL query."

    # Check for threading synchronization
    assert "Lock" in content, "The script does not seem to use threading.Lock for synchronization."

def test_fuzz_test_exists_and_valid():
    fuzz_path = "/home/user/fuzz_test.py"
    assert os.path.exists(fuzz_path), f"Fuzz testing script {fuzz_path} does not exist."

    with open(fuzz_path, "r") as f:
        content = f.read()

    # Check for assert statement
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        assert False, f"Syntax error in fuzz_test.py: {e}"

    has_assert = any(isinstance(node, ast.Assert) for node in ast.walk(tree))
    assert has_assert, "fuzz_test.py does not contain any assert statements to validate the counts."

def test_final_counts_json():
    json_path = "/home/user/final_counts.json"
    assert os.path.exists(json_path), f"Final output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            actual_counts = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    # Dynamically compute expected counts from the test_logs and users.db
    db_path = "/home/user/users.db"
    assert os.path.exists(db_path), f"Database {db_path} missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    user_roles = dict(cursor.fetchall())
    conn.close()

    log_dir = "/home/user/test_logs"
    assert os.path.exists(log_dir), f"Log directory {log_dir} missing."

    expected_counts = {}
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            with open(os.path.join(log_dir, filename), "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(' ')
                    if len(parts) >= 3:
                        username = parts[1]
                        role = user_roles.get(username, "unknown")
                        expected_counts[role] = expected_counts.get(role, 0) + 1

    assert actual_counts == expected_counts, \
        f"Final counts in {json_path} do not match the expected counts. Expected: {expected_counts}, Got: {actual_counts}"