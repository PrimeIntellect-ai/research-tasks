# test_final_state.py

import os
import subprocess
import sqlite3
import pytest

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Sanitizer script not found at {sanitizer_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus dir missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus dir missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["python3", sanitizer_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["python3", sanitizer_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not clean_failed and not evil_failed, " | ".join(error_msg)


def test_fix_query_sql():
    sql_path = "/home/user/fix_query.sql"
    assert os.path.isfile(sql_path), f"Fixed query SQL not found at {sql_path}"

    with open(sql_path, "r") as f:
        query = f.read()

    # Setup in-memory sqlite to test the query
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create schema
    cursor.execute("""
    CREATE TABLE users (
        user_id TEXT PRIMARY KEY,
        name TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE transactions (
        tx_id TEXT PRIMARY KEY,
        user_id TEXT,
        amount DECIMAL,
        transaction_date TIMESTAMP
    );
    """)

    # Insert dummy data
    cursor.execute("INSERT INTO users VALUES ('u1', 'Alice')")
    cursor.execute("INSERT INTO users VALUES ('u2', 'Bob')")

    cursor.execute("INSERT INTO transactions VALUES ('t1', 'u1', 100, '2023-01-01 10:00:00')")
    cursor.execute("INSERT INTO transactions VALUES ('t2', 'u1', 200, '2023-01-02 10:00:00')")
    cursor.execute("INSERT INTO transactions VALUES ('t3', 'u2', 50, '2023-01-01 10:00:00')")

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        pytest.fail(f"Execution of fix_query.sql failed: {e}")

    # Expected results: Alice with 200 (latest), Bob with 50
    assert len(results) == 2, "Query should return exactly one transaction per user."

    alice_res = [r for r in results if r[0] == 'Alice']
    bob_res = [r for r in results if r[0] == 'Bob']

    assert len(alice_res) == 1, "Alice should have exactly one record."
    assert alice_res[0][1] == 200, "Alice's record should be the most recent transaction (amount 200)."

    assert len(bob_res) == 1, "Bob should have exactly one record."
    assert bob_res[0][1] == 50, "Bob's record should be his only transaction (amount 50)."


def test_graph_path_script():
    script_path = "/home/user/graph_path.py"
    assert os.path.isfile(script_path), f"Graph path script not found at {script_path}"

    # Test path A -> F
    res = subprocess.run(["python3", script_path, "A", "F"], capture_output=True, text=True)
    assert res.returncode == 0, "graph_path.py failed to execute for A -> F"
    output = res.stdout.strip()
    assert output == "A,C,F", f"Expected path A,C,F but got {output}"

    # Test path A -> G (could be A,C,E,G or A,B,D,G)
    res2 = subprocess.run(["python3", script_path, "A", "G"], capture_output=True, text=True)
    assert res2.returncode == 0, "graph_path.py failed to execute for A -> G"
    output2 = res2.stdout.strip()
    assert output2 in ["A,C,E,G", "A,B,D,G"], f"Expected shortest path A->G but got {output2}"

    # Test no path F -> A
    res3 = subprocess.run(["python3", script_path, "F", "A"], capture_output=True, text=True)
    assert res3.returncode == 0, "graph_path.py failed to execute for F -> A"
    output3 = res3.stdout.strip()
    assert output3 == "NONE", f"Expected NONE but got {output3}"