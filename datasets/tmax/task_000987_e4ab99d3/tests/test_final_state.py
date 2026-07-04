# test_final_state.py

import os
import subprocess
import sqlite3
import pytest

def test_etl_filter_clean_corpus():
    script_path = "/home/user/etl_filter.py"
    clean_dir = "/app/corpus/clean"

    assert os.path.isfile(script_path), f"ETL filter script not found at {script_path}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert len(clean_files) > 0, "No JSON files found in clean corpus"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ACCEPT":
            failed_files.append((os.path.basename(filepath), output))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. "
                    f"Offending files (showing up to 5): {failed_files[:5]}")

def test_etl_filter_evil_corpus():
    script_path = "/home/user/etl_filter.py"
    evil_dir = "/app/corpus/evil"

    assert os.path.isfile(script_path), f"ETL filter script not found at {script_path}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert len(evil_files) > 0, "No JSON files found in evil corpus"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "REJECT":
            failed_files.append((os.path.basename(filepath), output))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. "
                    f"Offending files (showing up to 5): {failed_files[:5]}")

def test_graph_analytics_output():
    db_path = "/app/warehouse.db"
    output_path = "/home/user/top_users.txt"

    assert os.path.isfile(db_path), f"Database not found at {db_path}"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    # Compute expected top 3 users dynamically
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT target_user, COUNT(*) as in_degree
        FROM transactions
        WHERE timestamp >= 1685000000
        GROUP BY target_user
        ORDER BY in_degree DESC, target_user ASC
        LIMIT 3
    """)
    rows = cursor.fetchall()
    conn.close()

    expected_users = [row[0] for row in rows]
    expected_content = ",".join(expected_users)

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, \
        f"Expected top users '{expected_content}', but got '{actual_content}'"