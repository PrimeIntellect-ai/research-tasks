# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

SCRIPT_PATH = '/home/user/analyze_graph.sh'
DB_PATH = '/home/user/infra_graph.db'
LOG_PATH = '/home/user/output.log'

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Remove log if it exists to ensure we only check the current run's output
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    # Run the script
    result = subprocess.run([SCRIPT_PATH, DB_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. STDERR:\n{result.stderr}"

    # Check output.log
    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} was not created."
    with open(LOG_PATH, 'r') as f:
        log_content = f.read().strip()

    expected_log = (
        "--- Pattern Match ---\n"
        "AuthService\n"
        "BillingService\n"
        "--- Shortest Path ---\n"
        "2"
    )

    assert log_content == expected_log, f"Content of {LOG_PATH} does not match expected output.\nExpected:\n{expected_log}\nGot:\n{log_content}"

def test_database_changes():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if ServiceDependencyGraph table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ServiceDependencyGraph';")
    assert c.fetchone() is not None, "Table 'ServiceDependencyGraph' was not created."

    # Check the data in ServiceDependencyGraph
    c.execute("SELECT source, target FROM ServiceDependencyGraph ORDER BY source, target;")
    data = c.fetchall()

    expected_data = [
        ('BillingService', 'PaymentProcessor'),
        ('GatewayAPI', 'AuthService'),
        ('GatewayAPI', 'BillingService'),
        ('GatewayAPI', 'InventoryService')
    ]
    assert data == expected_data, "Data in 'ServiceDependencyGraph' does not match the expected projection."

    # Check if an index on 'source' exists for ServiceDependencyGraph
    c.execute("PRAGMA index_list('ServiceDependencyGraph');")
    indexes = c.fetchall()
    assert len(indexes) > 0, "No indexes found on 'ServiceDependencyGraph'."

    has_source_index = False
    for idx in indexes:
        idx_name = idx[1]
        c.execute(f"PRAGMA index_info('{idx_name}');")
        columns = c.fetchall()
        # columns is a list of (seqno, cid, name)
        if columns and columns[0][2] == 'source':
            has_source_index = True
            break

    assert has_source_index, "No index found on the 'source' column of 'ServiceDependencyGraph' to optimize forward traversal."

    conn.close()