# test_final_state.py
import os
import subprocess
import csv
import sqlite3

def test_pipeline_script_exists_and_runs():
    script_path = '/home/user/pipeline.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Run the script to ensure it generates the required files
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.py failed with error:\n{result.stderr}"

def test_analytics_db_exists():
    db_path = '/home/user/analytics.db'
    assert os.path.isfile(db_path), f"Database {db_path} was not created."

    # Verify tables exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    assert cursor.fetchone() is not None, "Table 'users' does not exist in analytics.db."
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
    assert cursor.fetchone() is not None, "Table 'transactions' does not exist in analytics.db."
    conn.close()

def test_query_plan_output():
    plan_path = '/home/user/query_plan.txt'
    assert os.path.isfile(plan_path), f"Query plan output {plan_path} was not created."

    with open(plan_path, 'r') as f:
        content = f.read().upper()

    assert 'USING INDEX' in content or 'USING COVERING INDEX' in content, \
        "The query plan does not indicate that an index was used. Please create appropriate indexes."

def test_top_users_output():
    output_path = '/home/user/top_users.csv'
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    expected_results = [
        ('User_633', 3630.98),
        ('User_379', 3593.45),
        ('User_407', 3543.83),
        ('User_54', 3427.02),
        ('User_666', 3398.70)
    ]

    with open(output_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"File {output_path} is empty."

    header = rows[0]
    assert header == ['name', 'total_spent'], f"Unexpected header in {output_path}: {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 5, f"Expected exactly 5 rows in {output_path}, found {len(data_rows)}."

    for i, (expected_name, expected_spent) in enumerate(expected_results):
        actual_name = data_rows[i][0]
        actual_spent = float(data_rows[i][1])

        assert actual_name == expected_name, f"Row {i+1}: expected name {expected_name}, got {actual_name}."
        assert abs(actual_spent - expected_spent) < 0.01, f"Row {i+1}: expected total_spent {expected_spent}, got {actual_spent}."