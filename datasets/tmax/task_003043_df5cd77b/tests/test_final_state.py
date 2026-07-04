# test_final_state.py

import os
import sqlite3
import pytest

def test_graph_db_exists_and_populated():
    """Check if graph.db exists and contains all records from both CSV files."""
    db_path = "/home/user/graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    # Connect to the database and check the edges table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure the edges table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges';")
    assert cursor.fetchone() is not None, "Table 'edges' does not exist in graph.db."

    # Check the total number of rows. 
    # transactions1.csv has 5 rows, transactions2.csv has 6 rows. Total = 11.
    cursor.execute("SELECT COUNT(*) FROM edges;")
    count = cursor.fetchone()[0]
    assert count == 11, f"Expected 11 rows in 'edges' table, found {count}. The ETL pipeline might not have loaded both files successfully."

    conn.close()

def test_process_results_script_exists_and_executable():
    """Check if process_results.sh exists and is executable."""
    script_path = "/home/user/process_results.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_txt_content():
    """Check if report.txt contains the correct aggregated and formatted results."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Node: G, Weight: 110",
        "Node: C, Weight: 100",
        "Node: B, Weight: 90",
        "Total Top 3 Weight: 300"
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, f"Content of {report_path} does not match the expected output.\nExpected:\n{expected_content}\n\nActual:\n{content}"