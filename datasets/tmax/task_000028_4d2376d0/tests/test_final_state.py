# test_final_state.py
import os
import json
import sqlite3
import pytest

def get_expected_failures():
    db_path = '/home/user/backups.db'
    if not os.path.exists(db_path):
        return {}

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Get latest backup for each datastore
    c.execute('''
        SELECT d.id, d.name, d.uri, b.status 
        FROM datastores d
        JOIN backups b ON d.id = b.datastore_id
        WHERE b.timestamp = (
            SELECT MAX(timestamp) FROM backups b2 WHERE b2.datastore_id = d.id
        )
    ''')
    latest_backups = c.fetchall()

    failing_datastores = [row for row in latest_backups if row[3] == 'FAILED']

    expected = {}
    for ds_id, name, uri, _ in failing_datastores:
        c.execute("SELECT AVG(size_bytes) FROM backups WHERE datastore_id = ? AND status = 'SUCCESS'", (ds_id,))
        avg = c.fetchone()[0]
        if avg is None:
            avg = 0.0

        expected[name] = {
            "avg_successful_size": float(avg),
            "uri": uri
        }

    conn.close()
    return expected

def test_critical_failures_json():
    json_path = "/home/user/critical_failures.json"
    assert os.path.isfile(json_path), f"Output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_db = get_expected_failures()

    assert set(actual.keys()) == set(expected_db.keys()), f"The set of failing datastores does not match. Expected {list(expected_db.keys())}, got {list(actual.keys())}."

    for ds_name, actual_data in actual.items():
        expected_avg = expected_db[ds_name]["avg_successful_size"]
        assert "avg_successful_size" in actual_data, f"Missing 'avg_successful_size' for {ds_name}"
        assert abs(actual_data["avg_successful_size"] - expected_avg) < 0.1, f"Incorrect average for {ds_name}. Expected {expected_avg}, got {actual_data['avg_successful_size']}"

        assert "impacted_services" in actual_data, f"Missing 'impacted_services' for {ds_name}"
        assert isinstance(actual_data["impacted_services"], list), f"'impacted_services' must be a list for {ds_name}"
        assert actual_data["impacted_services"] == sorted(actual_data["impacted_services"]), f"'impacted_services' must be sorted alphabetically for {ds_name}"

    # Specifically check the graph transitive dependencies based on the architecture.ttl
    if "users_db" in actual:
        expected_users_db_impacted = [
            "http://example.org/AuthService",
            "http://example.org/BillingService",
            "http://example.org/Frontend",
            "http://example.org/ReportingService"
        ]
        assert actual["users_db"]["impacted_services"] == expected_users_db_impacted, f"Incorrect impacted services for users_db. Expected {expected_users_db_impacted}, got {actual['users_db']['impacted_services']}."

    if "logs_db" in actual:
        expected_logs_db_impacted = [
            "http://example.org/Frontend",
            "http://example.org/ReportingService"
        ]
        assert actual["logs_db"]["impacted_services"] == expected_logs_db_impacted, f"Incorrect impacted services for logs_db. Expected {expected_logs_db_impacted}, got {actual['logs_db']['impacted_services']}."