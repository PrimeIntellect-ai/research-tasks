# test_final_state.py
import os
import sqlite3
import ast

def test_process_results_parameterized():
    script_path = '/home/user/process_results.py'
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

    with open(script_path, 'r') as f:
        source = f.read()

    # The script should not use .format for the query
    assert ".format(" not in source, "The script still contains .format(), which is not allowed for SQL queries."

    tree = ast.parse(source)
    execute_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                execute_calls += 1
                assert len(node.args) == 2, "cursor.execute() must be called with exactly two arguments: the query and the parameters."
                assert not isinstance(node.args[0], ast.JoinedStr), "f-strings must not be used in cursor.execute()."

    assert execute_calls >= 2, "Expected at least two cursor.execute() calls in the script."

def test_database_indexes():
    db_path = '/home/user/sensor_data.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name IN ('idx_sensor_time', 'idx_batch');")
    indexes = {row[0] for row in c.fetchall()}
    conn.close()

    assert 'idx_sensor_time' in indexes, "Index 'idx_sensor_time' is missing from the database."
    assert 'idx_batch' in indexes, "Index 'idx_batch' is missing from the database."

def test_query_plans_file():
    plans_path = '/home/user/query_plans.txt'
    assert os.path.isfile(plans_path), f"Query plans file {plans_path} does not exist."

    with open(plans_path, 'r') as f:
        content = f.read()

    assert "USING INDEX idx_sensor_time" in content or "USING INDEX 'idx_sensor_time'" in content or "USING INDEX `idx_sensor_time`" in content or "USING INDEX \"idx_sensor_time\"" in content or "USING COVERING INDEX idx_sensor_time" in content, "The query_plans.txt does not show usage of 'idx_sensor_time'."
    assert "USING INDEX idx_batch" in content or "USING INDEX 'idx_batch'" in content or "USING INDEX `idx_batch`" in content or "USING INDEX \"idx_batch\"" in content or "USING COVERING INDEX idx_batch" in content, "The query_plans.txt does not show usage of 'idx_batch'."