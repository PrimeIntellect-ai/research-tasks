# test_final_state.py

import os
import subprocess
import csv
import sqlite3
import pytest

def test_compliance_report():
    binary_path = '/home/user/auditor'
    csv_path = '/home/user/compliance_report.csv'

    # Run the agent's binary if it exists, to ensure the CSV is generated/updated
    if os.path.exists(binary_path):
        subprocess.run([binary_path], capture_output=True)

    assert os.path.exists(csv_path), f"Output CSV not found at {csv_path}"

    # Compute ground truth
    try:
        import pymongo
    except ImportError:
        pytest.fail("pymongo is required but not installed.")

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client['corporate']
    collection = db['employees']

    subs = set()
    queue = ["E042"]
    while queue:
        curr = queue.pop(0)
        for c in collection.find({"manager_id": curr}):
            if c['emp_id'] not in subs:
                subs.add(c['emp_id'])
                queue.append(c['emp_id'])

    conn = sqlite3.connect('/home/user/access_logs.db')
    cursor = conn.cursor()
    # Use NOT INDEXED to bypass the corrupted index and force a full table scan
    cursor.execute("SELECT log_id, emp_id FROM logs NOT INDEXED WHERE action = 'EXPORT'")

    expected_logs = set()
    for row in cursor.fetchall():
        log_id, emp_id = row
        if emp_id in subs:
            expected_logs.add(log_id)

    agent_logs = set()
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['log_id', 'emp_id', 'risk_multiplier'], f"Incorrect CSV header: {header}"
        for row in reader:
            if len(row) >= 1:
                agent_logs.add(row[0])

    tp = len(agent_logs.intersection(expected_logs))
    fp = len(agent_logs - expected_logs)
    fn = len(expected_logs - agent_logs)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.99, f"F1 score {f1:.4f} is below threshold 0.99. TP:{tp}, FP:{fp}, FN:{fn}"