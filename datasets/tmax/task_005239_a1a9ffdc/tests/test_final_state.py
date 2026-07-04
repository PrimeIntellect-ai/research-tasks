# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/ecommerce.db"
SQL_PATH = "/home/user/schema_optimization.sql"
SCRIPT_PATH = "/home/user/generate_report.py"
REPORT_PATH = "/home/user/report.json"

def test_schema_optimization_sql():
    assert os.path.exists(SQL_PATH), f"SQL file {SQL_PATH} does not exist."
    with open(SQL_PATH, 'r') as f:
        content = f.read().lower()

    index_count = content.count("create index")
    assert index_count >= 3, f"Expected at least 3 CREATE INDEX statements in {SQL_PATH}, found {index_count}."

def test_database_indexes():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) >= 3, f"Expected at least 3 custom indexes in the database, found {len(indexes)}."

def test_python_script_updated():
    assert os.path.exists(SCRIPT_PATH), f"Python script {SCRIPT_PATH} does not exist."
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    assert "(SELECT SUM(oi.quantity * p.price)" not in content, "The script still contains the inefficient correlated subquery."
    assert "GROUP BY" in content.upper(), "The script does not seem to use GROUP BY as requested."

def test_report_json_output():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, 'r') as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    # Compute expected report
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''
    SELECT u.id, u.name, SUM(oi.quantity * p.price) as total_spend
    FROM users u
    JOIN orders o ON u.id = o.user_id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE p.category = ?
    GROUP BY u.id, u.name
    HAVING total_spend > 0
    ORDER BY total_spend DESC
    LIMIT 5;
    '''
    cursor.execute(query, ("Electronics",))
    results = cursor.fetchall()
    conn.close()

    expected_report = [{"user_id": row[0], "name": row[1], "total_spend": round(row[2], 2)} for row in results]

    assert len(actual_report) == 5, f"Expected 5 results in {REPORT_PATH}, found {len(actual_report)}."

    for i in range(5):
        assert actual_report[i]["user_id"] == expected_report[i]["user_id"], f"Mismatch in user_id at rank {i+1}. Expected {expected_report[i]['user_id']}, got {actual_report[i]['user_id']}."
        assert actual_report[i]["name"] == expected_report[i]["name"], f"Mismatch in name at rank {i+1}. Expected {expected_report[i]['name']}, got {actual_report[i]['name']}."
        assert abs(actual_report[i]["total_spend"] - expected_report[i]["total_spend"]) < 0.01, f"Mismatch in total_spend at rank {i+1}. Expected {expected_report[i]['total_spend']}, got {actual_report[i]['total_spend']}."